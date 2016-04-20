from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.urlresolvers import reverse
from django.db.models import Q, ManyToManyField
from django.utils.safestring import mark_safe

from django_api.forms import RockFaceAdminForm, AreaAdminForm
from django_api.models import Area, RockFace, Route, Parking, ClubAdmin, Club, AreaImage, BaseImage, RockFaceImage
from reversion.admin import VersionAdmin


def in_any_club(user):
    if user.pk in ClubAdmin.objects.all().values_list('user_id', flat=True):
        return True
    return False


def in_club(clubs, user):
    for club in clubs:
        if user.pk in ClubAdmin.objects.filter(club=club).values_list('user_id', flat=True):
            return True
    return False


def delete_model(modeladmin, request, queryset):
    if request.user.is_superuser:
        for obj in queryset:
            obj.delete()
    elif str(modeladmin) == "django_api.{:}".format(str(AreaAdmin.__name__)):
        for obj in queryset:
            if obj and in_club(obj.clubs.all(), request.user):
                obj.delete()
    elif str(modeladmin) == "django_api.{:}".format(str(RockFaceAdmin.__name__)):
        for obj in queryset:
            if obj and in_club(obj.area.clubs.all(), request.user):
                obj.delete()
delete_model.short_description = "Ta bort markerade"

admin.site.site_title = 'Crag finder admin'
admin.site.site_header = 'Crag finder admin'

# Text to put at the top of the admin index page.
admin.site.index_title = mark_safe(
        '1. Skapa ett område först och lägg in vilka klippor som finns på platsen och namnen på dem där. <br>'
        '2. Gå in under klippor och lägg in mer information och leder på varje klippa.')


def modified_has_permission(request):
    """
    Removed check for is_staff.
    """
    return True

setattr(admin.site, 'has_permission', modified_has_permission)


class BaseImageInline(admin.TabularInline):
    model = BaseImage

    def image_tag(self, obj):
        return '<img src="{:}" style="max-width: 100%"/>'.format(obj.image.url)

    image_tag.short_description = 'Uppladdad bild'
    image_tag.allow_tags = True
    readonly_fields = ('image_tag',)
    fields = ('image', 'image_tag')
    extra = 1
    max_num = None

    def has_module_permission(self, request):
        return request.user.is_superuser or in_any_club(request.user)

    def has_add_permission(self, request):
        return request.user.is_superuser or in_any_club(request.user)

    def has_change_permission(self, request, obj=None):
        raise NotImplementedError("Implement this method!")


class AreaImageInline(BaseImageInline):
    model = AreaImage
    max_num = 10

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return in_club(obj.clubs.all(), request.user)
        return in_any_club(request.user)


class RockFaceImageInline(BaseImageInline):
    model = RockFaceImage
    max_num = None
    fields = ('image', 'image_tag', 'name', 'description')

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return in_club(obj.area.clubs.all(), request.user)
        return in_any_club(request.user)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return in_club(obj.area.clubs.all(), request.user)
        return False


class RoutesInline(admin.TabularInline):
    model = Route
    fields = ('route_nr', 'name', 'grade', 'type', 'short_description', 'length', 'nr_of_bolts', 'first_ascent_name',
              'first_ascent_year', 'image')
    extra = 0

    def has_module_permission(self, request):
        return request.user.is_superuser or in_any_club(request.user)

    def has_add_permission(self, request):
        return request.user.is_superuser or in_any_club(request.user)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return in_club(obj.area.clubs.all(), request.user)
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return in_club(obj.area.clubs.all(), request.user)
        return in_any_club(request.user) or request.user.is_superuser

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        db = kwargs.get('using')
        if 'queryset' not in kwargs:
            queryset = self.get_field_queryset(db, db_field, request)
            if queryset is not None:
                kwargs['queryset'] = queryset

        # I feel obligated to apologize for the next line but i'm stuck after trying 4 different approaches.
        rockface_pk = int(request.path.split('rockface/')[1].split('/')[0])
        if str(db_field) == "django_api.Route.image":
            kwargs['queryset'] = RockFaceImage.objects.filter(rockface=rockface_pk)
        return db_field.formfield(**kwargs)


class ParkingInline(admin.TabularInline):
    model = Parking
    fields = ('position',)
    extra = 0

    def has_module_permission(self, request):

        return request.user.is_superuser or in_any_club(request.user)

    def has_add_permission(self, request):
        return request.user.is_superuser or in_any_club(request.user)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return in_club(obj.clubs.all(), request.user)
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return in_club(obj.clubs.all(), request.user)
        return in_any_club(request.user)


class RockFaceAdmin(VersionAdmin):
    model = RockFace

    def clubs(self):
        return ', '.join(['<a href="{url}">{name}</a>'.format(
            url=reverse('admin:{:}_{:}_change'.format(x._meta.app_label, x._meta.model_name), args=(x.pk,)),
            name=x.name) for x in self.area.clubs.all().order_by('name')])

    clubs.allow_tags = True
    clubs.short_description = 'Klubbar'

    def area_list_link(self):
        return '<a href="{url}">{name}</a>'.format(
            url=reverse('admin:{:}_{:}_change'.format(self.area._meta.app_label, self.area._meta.model_name), args=(self.area.pk,)),
            name=self.area)

    area_list_link.allow_tags = True
    area_list_link.short_description = 'Område'

    def area_link(self, instance):
        if instance.id:
            url = reverse('admin:{:}_{:}_change'.format(instance.area._meta.app_label, instance.area._meta.model_name),
                          args=(instance.area.id,))
            return mark_safe(
                '<a target="_blank" href="{:}">{:}</a>'.format(url, instance.area.name))
        else:
            return '-'
    """
    <div class="submit-row">
        <input type="submit" value="Spara och fortsätt redigera" name="_continue">
    </div>
    """
    area_link.short_description = 'Area'
    area_link.allow_tags = True
    inlines = [RockFaceImageInline, RoutesInline]
    list_display = ('name', area_list_link, clubs)
    list_filter = ('area__clubs', 'area')
    list_display_links = ('name',)
    readonly_fields = ['area', 'area_link']
    search_fields = ['name', 'area__clubs__name', 'area__name']
    actions = [delete_model]

    def get_actions(self, request):
        actions = super(RockFaceAdmin, self).get_actions(request)
        if not request.user.is_superuser:
            del actions['delete_selected']
        return actions

    fieldsets = (
        (None, {
            'fields': ('area_link', 'name', 'short_description', 'long_description',)
        }),
        ('Karta', {
            'fields': ('geo_data',),
        }),
    )
    form = RockFaceAdminForm

    class Media:
        css = {
            "all": ("django_api/gmaps_admin.css", )
        }
        js = ("django_api/gmaps_admin.js", "django_api/save_buttons.js",)

    def has_module_permission(self, request):
        return request.user.is_superuser or in_any_club(request.user)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return in_club(obj.area.clubs.all(), request.user)
        return in_any_club(request.user)

    def get_queryset(self, request):
        qs = super(RockFaceAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(
            Q(area__clubs__id__in=ClubAdmin.objects.filter(user_id=request.user.pk).values_list('club_id', flat=True)))


class RockFaceInline(admin.StackedInline):
    model = RockFace

    def admin_link(self, instance):
        if instance.id:
            url = reverse('admin:{:}_{:}_change'.format(instance._meta.app_label, instance._meta.model_name), args=(instance.id,))
            return mark_safe('<a target="_blank" href="{:}">Lägg till information, leder karta, bilder etc.</a>'.format(url))
        else:
            return 'Tryck "Spara och fortsätt redigera" för att kunna administrera klippan.'

    admin_link.short_description = 'Admin länk'
    admin_link.allow_tags = True
    readonly_fields = ('admin_link',)
    fields = ['name', 'admin_link']
    extra = 0

    def has_module_permission(self, request):
        return request.user.is_superuser or in_any_club(request.user)

    def has_add_permission(self, request):
        return request.user.is_superuser or in_any_club(request.user)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return in_club(obj.clubs.all(), request.user)
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return in_club(obj.clubs.all(), request.user)
        return in_any_club(request.user)


class AreaAdmin(VersionAdmin):
    def clubs(self):
        return ', '.join(['<a href="{url}">{name}</a>'.format(
            url=reverse('admin:{:}_{:}_change'.format(x._meta.app_label, x._meta.model_name), args=(x.pk,)),
            name=x.name) for x in self.clubs.all().order_by('name')])

    clubs.allow_tags = True
    clubs.short_description = 'Klubbar'

    def crags(self):
        return ', '.join(['<a href="{url}">{name}</a>'.format(
            url=reverse('admin:{:}_{:}_change'.format(x._meta.app_label, x._meta.model_name), args=(x.pk,)),
            name=x.name) for x in self.rockfaces.all()])

    crags.allow_tags = True
    crags.short_description = 'Klippor'

    list_display = ('name', clubs, crags)
    list_filter = ('clubs',)
    search_fields = ['name', 'clubs__name', 'rockfaces__name']
    formfield_overrides = {ManyToManyField: {'widget': FilteredSelectMultiple(
        "", is_stacked=False)}, }
    inlines = [AreaImageInline, RockFaceInline,]  # TODO: add parking inline
    form = AreaAdminForm
    actions = [delete_model]

    def image_tag(self, obj):
        return '<img src="{:}" />'.format(obj.image.image.url)

    image_tag.short_description = 'Uppladdad bild'
    image_tag.allow_tags = True
    readonly_fields = ('image_tag',)
    fieldsets = (
        (None, {
            'fields': ('name', 'short_description', 'long_description', 'road_description', )
        }),
        ('KLUBB/KLUBBAR', {
            'fields': ('clubs',),
        }),
    )

    def get_actions(self, request):
        actions = super(AreaAdmin, self).get_actions(request)
        if not request.user.is_superuser:
            del actions['delete_selected']
        return actions

    def has_module_permission(self, request):
        return request.user.is_superuser or in_any_club(request.user)

    def has_add_permission(self, request):
        return request.user.is_superuser or in_any_club(request.user)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return in_club(obj.clubs.all(), request.user)
        return in_any_club(request.user)

    def get_queryset(self, request):
        qs = super(AreaAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(
            Q(clubs__id__in=ClubAdmin.objects.filter(user_id=request.user.pk).values_list('club_id', flat=True)))


class AddClubAdminInline(admin.TabularInline):
    model = ClubAdmin
    fields = ('user',)
    extra = 1


class AdminClub(VersionAdmin):
    def areas(self):
        return ', '.join(['<a href="{url}">{name}</a>'.format(
            url=reverse('admin:{:}_{:}_change'.format(x._meta.app_label, x._meta.model_name), args=(x.pk,)),
            name=x.name) for x in self.area_set.all()])

    areas.allow_tags = True
    areas.short_description = 'Områden'

    search_fields = ['name', 'area__name']
    list_display = ('name', areas)
    list_filter = ('name',)
    inlines = [AddClubAdminInline]

    def has_module_permission(self, request):
        # stupid check django performs to not get 403 when clicking on app label
        return in_any_club(request.user) or request.user.is_superuser

    def get_actions(self, request):
        actions = super(AdminClub, self).get_actions(request)
        if not request.user.is_superuser:
            return None
        return actions

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return obj.pk in ClubAdmin.objects.filter(user_id=request.user.pk).values_list('club_id', flat=True)
        return in_any_club(request.user)

    def get_queryset(self, request):
        qs = super(AdminClub, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(
            Q(pk__in=ClubAdmin.objects.filter(user_id=request.user.pk).values_list('club_id', flat=True)))


admin.site.register(Area, AreaAdmin)
admin.site.register(RockFace, RockFaceAdmin)
admin.site.register(Club, AdminClub)
