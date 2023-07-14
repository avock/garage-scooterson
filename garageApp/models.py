from django.db import models
import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model

class GarageApp(models.Model):
    vehicle_name = models.CharField(max_length=100)
    vehicle_id = models.CharField(primary_key=True, blank=False, null=False, max_length=100, error_messages={'unique':"This vehicle has already been registered."})
    vehicle_owner_id = models.IntegerField()
    vehicle_uuid = models.CharField(max_length=100)
    vehicle_pub_key = models.CharField(max_length=100)
    particle_id = models.CharField(max_length=100)
    particle_serial = models.CharField(max_length=100)
    particle_name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Garage"

    def save(self, *args, **kwargs):
        if not self.vehicle_id:
            last_vehicle = GarageApp.objects.order_by('vehicle_id').first()
            if last_vehicle:
                last_id = last_vehicle.vehicle_id
                next_id = self.increment_vehicle_id(last_id)
                self.vehicle_id = next_id
            else:
                self.vehicle_id = "0001"
        super().save(*args, **kwargs)

    def increment_vehicle_id(self, vehicle_id):
        # Helper method to increment the vehicle ID
        if vehicle_id == "ZZZZ":
            return "0001"
        else:
            chars = list(vehicle_id)
            for i in range(len(chars) - 1, -1, -1):
                if chars[i] != "Z":
                    chars[i] = self.increment_char(chars[i])
                    break
                else:
                    chars[i] = "0"
            return "".join(chars)

    def increment_char(self, char):
        # Helper method to increment a single character
        if char == "Z":
            return "0"
        elif char == "9":
            return "A"
        elif char.isdigit():
            return chr(ord(char) + 1)

class VehicleStatus(models.Model):
    garage = models.OneToOneField(GarageApp ,on_delete=models.CASCADE ,primary_key=True , related_name='vehicle_status')

    battery_percentage = models.IntegerField()
    power_on = models.BooleanField()
    sharing_on = models.BooleanField()
    alarm_on = models.BooleanField()
    last_sync = models.TimeField(default=datetime.time(0, 0))
    is_occupied = models.BooleanField()
    odo_meter = models.IntegerField()
    trip_meter = models.IntegerField()
    gear_mode = models.IntegerField()
    
    class Meta:
        verbose_name_plural = "Vehicle Status"
    
class VehicleInfo(models.Model):
    
    COLOR_CHOICES = [
        'Blue',
        'White',
        'Yellow',
        'Orange',
        'Cyan',
        'Red',
        'Purple',
        'Black',
        'Green',
        'Neon Green',
        'Neon Pink',
        'Neon Yellow',
        'Neon Red',
        'Neon Orange',
        'Neon Purple',
        'Carbon Fiber Black',
    ]

    MODEL_CHOICES = [
        'Rolley',
        'Rolley Plus',
        'Icon',
    ]
    
    garage = models.OneToOneField(GarageApp, on_delete=models.CASCADE, primary_key=True, related_name='vehicle_info')
    
    model = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    manufacture = models.CharField(max_length=100)
    model_year = models.IntegerField()
    model = models.CharField(max_length=20, choices=[(choice, choice) for choice in MODEL_CHOICES])
    color = models.CharField(max_length=20, choices=[(choice, choice) for choice in COLOR_CHOICES])
    width = models.IntegerField()
    height = models.IntegerField()
    length = models.IntegerField()
    top_speed = models.IntegerField()
    mileage = models.IntegerField()
    power = models.IntegerField()
    sn = models.CharField(max_length=100)
    motor = models.CharField(max_length=100)
    ecu = models.CharField(max_length=100)
    gsm = models.CharField(max_length=100)
    gps = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Vehicle Info"
    
class SharedVehicleData(models.Model):
    garage = models.OneToOneField(GarageApp, on_delete=models.CASCADE, primary_key=True, related_name='shared_vehicle_data')
    
    is_occupied = models.BooleanField()
    sharing_enabled = models.BooleanField()
    is_request_pending = models.BooleanField()
    idle_time_option = models.IntegerField()
    max_assist_level = models.IntegerField()
    
    class Meta:
        verbose_name_plural = "Shared Vehicle Data"
    
class SharedVehicleOwnerData(models.Model):
    garage = models.OneToOneField(GarageApp, on_delete=models.CASCADE, primary_key=True, related_name='shared_vehicle_owner_data')
    
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=10)
    email = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_id = models.IntegerField()
    birth_date = models.DateField()
    gender = models.CharField(max_length=10)
    weight = models.IntegerField()
    profile_pic_url_string = models.CharField(max_length=255)
    profile_image = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    weight_in_kg = models.CharField(max_length=255)
    email_verified = models.BooleanField()
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)
    
    class Meta:
        verbose_name_plural = "Shared Vehicle Owner Data"
    
class UserVehicles(models.Model):
    userID = models.IntegerField()
    vehicle_id = models.ForeignKey(
        GarageApp,
        on_delete=models.CASCADE,
        to_field='vehicle_id',
        related_name='user_vehicles'
    )