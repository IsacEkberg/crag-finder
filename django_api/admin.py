from django.contrib import admin
from django_api.models import Rental


class RentalAdmin(admin.ModelAdmin):
    pass

admin.site.register(Rental, RentalAdmin)
