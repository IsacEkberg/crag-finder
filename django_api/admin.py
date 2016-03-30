from django.contrib import admin
from django_api.models import Rental, Area, RockFace, Route, Parking


class RoutesInline(admin.TabularInline):
    model = Route
    fields = ('name', 'grade', 'type')


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


admin.site.register(Area)
admin.site.register(RockFace, RockFaceAdmin)
admin.site.register(Route)
admin.site.register(Rental)
