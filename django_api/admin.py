from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Q, ManyToManyField
from django.utils.safestring import mark_safe

from django_api.forms import RockFaceAdminForm, AreaAdminForm
from django_api.models import Area, RockFace, Route, Parking, Club, AreaImage, RockFaceImage, BEING_REVIEWED_CHANGE, \
BEING_REVIEWED_NEW, BEING_REVIEWED_DELETE, APPROVED
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from reversion.admin import VersionAdmin


def is_trusted(user):
    try:
        return user.is_trusted
    except:
        return False


def delete_model(modeladmin, request, queryset):
    if request.user.is_superuser or \
            ((str(modeladmin) == "django_api.{:}".format(str(AreaAdmin.__name__)) or
              str(modeladmin) == "django_api.{:}".format(str(RockFaceAdmin.__name__))
              ) and is_trusted(request.user)):
        for obj in queryset:
            obj.delete()
    else:
        for obj in queryset:
            obj.status = BEING_REVIEWED_DELETE
            obj.save()


delete_model.short_description = "Ta bort markerade"

admin.site.site_title = 'Crag finder admin'
admin.site.site_header = 'Crag finder admin'

# Text to put at the top of the admin index page.
admin.site.index_title = mark_safe(
        '1. Skapa ett område först och lägg in vilka klippor som finns på platsen och namnen på dem där. <br>'
        '2. Gå in under klippor och lägg in mer information och leder på varje klippa.')

DjangoUserAdmin.list_display += ('is_trusted',)  # don't forget the commas
DjangoUserAdmin.list_filter += ('is_trusted',)
DjangoUserAdmin.fieldsets += (('CragFinder', {'fields': ('is_trusted', )}),)  # Monkey patching at its finest.


class UserAdmin(DjangoUserAdmin):
    def save_model(self, request, obj, form, change):
        obj.is_staff = True
        obj.save()


class BaseImageInline(admin.TabularInline):

    def image_tag(self, obj):
        return '<img src="{:}" style="max-width: 100%"/>'.format(obj.image.url)

    image_tag.short_description = 'Uppladdad bild'
    image_tag.allow_tags = True
    readonly_fields = ('image_tag',)
    fields = ('image', 'image_tag')
    extra = 1
    max_num = None

    def has_module_permission(self, request):
        return True

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        raise True


class AreaImageInline(BaseImageInline):
    model = AreaImage
    max_num = 10


class RockFaceImageInline(BaseImageInline):
    model = RockFaceImage
    max_num = None
    fields = ('image', 'image_tag', 'name', 'description')


class RoutesInline(admin.TabularInline):
    model = Route
    fields = ('route_nr', 'name', 'grade', 'type', 'short_description', 'length', 'nr_of_bolts', 'first_ascent_name',
              'first_ascent_year', 'image')
    extra = 0

    def has_module_permission(self, request):
        return True

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
        return request.user.is_superuser or is_trusted(request.user)


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
        return True

    def has_add_permission(self, request):
        return False


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
        return True


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
        return True

    def has_add_permission(self, request):
        return True


class AdminClub(VersionAdmin):
    # TODO: Add warning about current pending changes.
    def areas(self):
        return ', '.join(['<a href="{url}">{name}</a>'.format(
            url=reverse('admin:{:}_{:}_change'.format(x._meta.app_label, x._meta.model_name), args=(x.pk,)),
            name=x.name) for x in self.area_set.all()])

    areas.allow_tags = True
    areas.short_description = 'Områden'

    search_fields = ['name', 'area__name']
    list_display = ('name', 'status', 'replacing', areas)
    list_filter = ('name',)
    fields = ('name', 'address', 'email', 'info')
    readonly_fields = ('replacing',)
    actions = [delete_model]

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        if request.user.is_superuser or request.user.is_trusted:
            if change and obj.replacing:
                tmp_pk = obj.pk
                obj.pk = obj.replacing.pk
                obj.replacing = None
                obj.status = APPROVED
                obj.save()
                Club.objects.get(pk=tmp_pk).delete()
            else:
                obj.status = APPROVED
                obj.save()
        elif change:
            tmp_pk = obj.pk
            obj.pk = None
            obj.status = BEING_REVIEWED_CHANGE
            obj.save()
            obj.replacing = Club.objects.get(pk=tmp_pk)
            obj.save()
        else:
            obj.status = BEING_REVIEWED_NEW
            obj.save()

    def delete_model(self, request, obj):
        if request.user.is_superuser or request.user.is_trusted:
            obj.delete()
        else:
            obj.status = BEING_REVIEWED_DELETE
            obj.save()

    def has_module_permission(self, request):
        # stupid check django performs to not get 403 when clicking on app label
        return True

    def get_actions(self, request):
        actions = super(AdminClub, self).get_actions(request)
        if not request.user.is_superuser:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def get_queryset(self, request):
        if request.user.is_superuser or request.user.is_trusted:
            return super(AdminClub, self).get_queryset(request)
        else:
            return super(AdminClub, self).get_queryset(request).filter(Q(status=APPROVED) | Q(status=BEING_REVIEWED_DELETE))
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(RockFace, RockFaceAdmin)
admin.site.register(Club, AdminClub)

