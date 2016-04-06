from django.contrib import admin
from django_api.models import Area, RockFace, Route, Parking, ClubAdmin, Club
from django.contrib.auth.models import User, Group
from django.contrib.admin import AdminSite


class MyAdminSite(AdminSite):
    def has_permission(self, request):
        """
        Removed check for is_staff.
        """
        return request.user.is_active

cragfinder_admin_site = MyAdminSite(name='cragfinderadmin')

class RoutesInline(admin.TabularInline):
    model = Route
    fields = ('name', 'grade', 'type', 'short_description', 'length', 'first_ascent_name', 'first_ascent_year')


class ParkingInline(admin.TabularInline):
    model = Parking
    fields = ('position',)
    extra = 1


class RockFaceAdmin(admin.ModelAdmin):
    model = RockFace
    inlines = [RoutesInline]
    list_display = ('name',)
    list_display_links = ('name',)

    class Media:
        css = {
            "all": ("django_api/gmaps_admin.css", )
        }
        js = ("django_api/gmaps_admin.js", )


class RockFaceInline(admin.StackedInline):
    model = RockFace
    extra = 0


class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'faces', 'routes')
    filter = ('name',)
    readonly_fields = ('faces', 'routes')
    inlines = [RockFaceInline, ParkingInline]


class RentalAdmin(admin.ModelAdmin):
    pass

cragfinder_admin_site.register(Group)
cragfinder_admin_site.register(User)
cragfinder_admin_site.register(Area)
cragfinder_admin_site.register(RockFace, RockFaceAdmin)
cragfinder_admin_site.register(Route)

cragfinder_admin_site.register(Club)
cragfinder_admin_site.register(ClubAdmin)
