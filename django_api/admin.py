from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db.models import Q, ManyToManyField
from django.utils.safestring import mark_safe

from django_api.forms import RockFaceAdminForm, AreaAdminForm
from django_api.models import Area, RockFace, Route, Parking, ClubAdmin, Club
from django.contrib.auth.models import User, Group
from django.contrib.admin import AdminSite
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


class MyAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = 'Crag finder admin'

    # Text to put in each page's <h1>.
    site_header = 'Crag finder admin'

    # Text to put at the top of the admin index page.
    index_title = mark_safe(
        '1. Skapa ett område först och lägg in vilka klippor som finns på platsen och namnen på dem där. <br>'
        '2. Gå in under klippor och lägg in mer information och leder på varje klippa.')

    def has_permission(self, request):
        """
        Removed check for is_staff.
        """
        return request.user.is_active


cragfinder_admin_site = MyAdminSite(name='cragfinderadmin')


class RoutesInline(admin.TabularInline):
    model = Route
    fields = ('name', 'grade', 'type', 'short_description', 'length', 'first_ascent_name', 'first_ascent_year')

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
    inlines = [RoutesInline]
    list_display = ('name',)
    list_display_links = ('name',)
    readonly_fields = ['area']

    actions = [delete_model]

    def get_actions(self, request):
        actions = super(RockFaceAdmin, self).get_actions(request)
        if not request.user.is_superuser:
            del actions['delete_selected']
        return actions

    fieldsets = (
        (None, {
            'fields': ('area', 'name', 'short_description', 'long_description',)
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
        js = ("django_api/gmaps_admin.js", )

    def has_module_permission(self, request):
        return request.user.is_superuser or in_any_club(request.user)

    def has_add_permission(self, request):
        return request.user.is_superuser

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
    fields = ['name']
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
    list_display = ('name',)
    filter = ('name',)
    formfield_overrides = {ManyToManyField: {'widget': FilteredSelectMultiple(
        "", is_stacked=False)}, }
    inlines = [RockFaceInline,]  # TODO: add parking inline
    form = AreaAdminForm
    actions = [delete_model]
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
    list_display = ('name',)
    filter = ('name',)
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


cragfinder_admin_site.register(Group)
cragfinder_admin_site.register(User)
cragfinder_admin_site.register(Area, AreaAdmin)
cragfinder_admin_site.register(RockFace, RockFaceAdmin)
cragfinder_admin_site.register(Club, AdminClub)
