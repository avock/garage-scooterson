from django.contrib import admin
from django import forms

# Register your models here.
from .models import GarageApp, VehicleStatus, VehicleInfo, UserVehicles, SharedVehicleData, SharedVehicleOwnerData
        
admin.site.register(GarageApp) 
admin.site.register(VehicleStatus)
admin.site.register(VehicleInfo)
admin.site.register(UserVehicles)
admin.site.register(SharedVehicleData)
admin.site.register(SharedVehicleOwnerData)