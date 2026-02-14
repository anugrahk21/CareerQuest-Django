from django.contrib import admin
from .models import CareerApp

# Register your models here.
@admin.register(CareerApp)
class CareerAppAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'role', 'type', 'package', 'status', 'date', 'notes')
