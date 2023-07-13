from rest_framework import serializers
from .models import GarageApp, VehicleStatus, VehicleInfo, SharedVehicleData, SharedVehicleOwnerData

# helper serializers
class VehicleStatusSerializer(serializers.ModelSerializer):
    garage = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
            model = VehicleStatus
            fields = (
                "garage",
                "battery_percentage",
                "power_on",
                "sharing_on",
                "alarm_on",
                "last_sync",
                "is_occupied",
                "odo_meter",
                "trip_meter",
                "gear_mode",
            )
            
    def update(self, instance, validated_data):
        # vehicle_info_data = validated_data.pop('vehicle_info', {})
        vehicle_status_data = validated_data.pop('vehicle_status', {})
        
        for field in validated_data.keys():
            new_field = validated_data.get(field, getattr(instance, field))
            setattr(instance, field, new_field)
    
        instance.save()
        
        return instance
    
class SharedVehicleDataSerializer(serializers.ModelSerializer):
    garage = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
            model = SharedVehicleData
            fields = (
                "garage",
                "is_occupied",
                "sharing_enabled",
                "is_request_pending",
                "idle_time_option",
                "max_assist_level"
            )
            
    def update(self, instance, validated_data):
        shared_vehicle_data = validated_data.pop('shared_vehicle_data', {})
        
        for field in validated_data.keys():
            new_field = validated_data.get(field, getattr(instance, field))
            setattr(instance, field, new_field)
    
        instance.save()
        
        return instance
    
class SharedVehicleOwnerDataSerializer(serializers.ModelSerializer):
    garage = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.DictField()
    user_address = serializers.DictField()
    
    class Meta:
            model = SharedVehicleOwnerData
            fields = (
                "garage",
                "address_line1",
                "address_line2",
                "city",
                "state",
                "zipcode",
                "email",
                "mobile_number",
                "name",
                "user_id",
                "birth_date",
                "gender",
                "weight",
                "profile_pic_url_string",
                "profile_image",
                "email_verified",
                "full_name",
                "address",
                "weight_in_kg",
                "user_address"
            )

class VehicleInfoSerializer(serializers.ModelSerializer):
    garage = serializers.PrimaryKeyRelatedField(read_only=True)
    dimension = serializers.DictField()
    parameters = serializers.DictField()
    configuration = serializers.DictField()

    class Meta:
        model = VehicleInfo
        fields = (
            "garage",
            "model",
            "type",
            "manufacture",
            "model_year",
            "color",
            "dimension",
            "parameters",
            "configuration",
        )

class GarageSerializer(serializers.ModelSerializer):
    vehicle_info = VehicleInfoSerializer(many=False)
    vehicle_status = VehicleStatusSerializer(many=False)
    shared_vehicle_data = SharedVehicleDataSerializer(many=False)
    shared_vehicle_owner_data = SharedVehicleOwnerDataSerializer(many=False)

    class Meta:
        model = GarageApp
        fields = [            
            'vehicle_name',
            'vehicle_id',
            'vehicle_owner_id',
            'vehicle_uuid',
            'vehicle_pub_key',
            'particle_id',
            'particle_serial',
            'particle_name',
            'shared_vehicle_data',
            'shared_vehicle_owner_data',
            'vehicle_info',
            'vehicle_status',
        ]
    
    def create(self, validated_data):
        # pop
        shared_vehicle_data = validated_data.pop('shared_vehicle_data')
        shared_vehicle_owner_data_input = validated_data.pop('shared_vehicle_owner_data')
        vehicle_status_data = validated_data.pop('vehicle_status')
        vehicle_info_data = validated_data.pop('vehicle_info')
        
        # handling nested json objects for vehicle_info
        configuration_data = vehicle_info_data.pop('configuration')
        dimension_data = vehicle_info_data.pop('dimension')
        parameters_data = vehicle_info_data.pop('parameters')
        
        # handling nested json objects for shared_vehicle_owner_data
        name_data = shared_vehicle_owner_data_input.pop('name')
        user_address_data = shared_vehicle_owner_data_input.pop('user_address')
        
        garage = GarageApp.objects.create(**validated_data)
        
        shared_vehicle_data = SharedVehicleData.objects.create(garage=garage, **shared_vehicle_data)
        
        vehicle_status = VehicleStatus.objects.create(garage=garage, **vehicle_status_data)
        
        vehicle_info_data.update(configuration_data)
        vehicle_info_data.update(dimension_data)
        vehicle_info_data.update(parameters_data)
        vehicle_info = VehicleInfo.objects.create(garage=garage, **vehicle_info_data)
        
        # save required as the configuration field of vehicle_info is being updated
        vehicle_info.configuration = configuration_data
        vehicle_info.dimension = dimension_data
        vehicle_info.parameters = parameters_data
        vehicle_info.save()
        
        shared_vehicle_owner_data_input.update(name_data)
        shared_vehicle_owner_data_input.update(user_address_data)
        shared_vehicle_owner_data = SharedVehicleOwnerData.objects.create(garage=garage, **shared_vehicle_owner_data_input)
        
        shared_vehicle_owner_data.name = name_data
        shared_vehicle_owner_data.user_address = user_address_data
        shared_vehicle_owner_data.save()
        
        garage.shared_vehicle_data = shared_vehicle_data
        garage.shared_vehicle_owner_data = shared_vehicle_owner_data
        garage.vehicle_status = vehicle_status
        garage.vehicle_info = vehicle_info

        return garage

class GarageUpdater(serializers.ModelSerializer):

    class Meta:
        model = GarageApp
        fields = [            
            'vehicle_name',
            'vehicle_id',
            'vehicle_owner_id',
            'vehicle_uuid',
            'vehicle_pub_key',
            'particle_id',
            'particle_serial',
            'particle_name'
        ]
    
    def update(self, instance, validated_data):
        
        for field in validated_data.keys():
            if field not in ['vehicle_status', 'vehicle_info', 'shared_vehicle_data', 'shared_vehicle_owner_data']:
                new_field = validated_data.get(field, getattr(instance, field))
                setattr(instance, field, new_field)
        
        instance.save()
        
        return instance
    
# Deserializers
class GarageDeserializer(serializers.ModelSerializer):
    class Meta:
        model = GarageApp
        fields = [            
            'vehicle_name',
            'vehicle_id',
            'vehicle_owner_id',
            'vehicle_uuid',
            'vehicle_pub_key',
            'particle_id',
            'particle_serial',
            'particle_name',
        ]
        
def vehicleInfoDeserilizer(vehicle_info_values):
        nested_vehicle_info_values = {
            "model": vehicle_info_values['model'],
            "type": vehicle_info_values['type'],
            "manufacture": vehicle_info_values['manufacture'],
            "model_year": vehicle_info_values['model_year'],
            "color": vehicle_info_values['color'],
            "dimension": {
                "width": vehicle_info_values['width'],
                "height": vehicle_info_values['height'],
                "length": vehicle_info_values['length']
            },
            "parameters": {
                "top_speed": vehicle_info_values['top_speed'],
                "mileage": vehicle_info_values['mileage'],
                "power": vehicle_info_values['power']
            },
            "configuration": {
                "sn": vehicle_info_values['sn'],
                "motor": vehicle_info_values['motor'],
                "ecu": vehicle_info_values['ecu'],
                "gsm": vehicle_info_values['gsm'],
                "gps": vehicle_info_values['gps']
            }
        }
        return nested_vehicle_info_values
    
def sharedVehicleOwnerDataDeserializer(shared_vehicle_owner_data):
        nested_shared_vehicle_owner_data = {
            "address_line1": shared_vehicle_owner_data["address_line1"],
            "address_line2": shared_vehicle_owner_data['address_line2'],
            "city": shared_vehicle_owner_data['city'],
            "state": shared_vehicle_owner_data['state'],
            "zipcode": shared_vehicle_owner_data['zipcode'],
            "email": shared_vehicle_owner_data['email'],
            "mobile_number": shared_vehicle_owner_data['mobile_number'],
            "name": {
                "first_name": shared_vehicle_owner_data['first_name'],
                "last_name": shared_vehicle_owner_data['last_name']
            },
            "user_id": shared_vehicle_owner_data['user_id'],
            "birth_date": shared_vehicle_owner_data['birth_date'],
            "gender": shared_vehicle_owner_data['gender'],
            "weight": shared_vehicle_owner_data['weight'],
            "profile_pic_url_string": shared_vehicle_owner_data['profile_pic_url_string'],
            "profile_image": shared_vehicle_owner_data['profile_image'],
            "email_verified": shared_vehicle_owner_data['email_verified'],
            # "full_name": shared_vehicle_owner_data['full_name'],
            # "address": shared_vehicle_owner_data['address'],
            # "weight_in_kg": shared_vehicle_owner_data['weight_in_kg'],
            "user_address": {
                "latitude": shared_vehicle_owner_data['latitude'],
                "longitude": shared_vehicle_owner_data['longitude']
            },
        }
        return nested_shared_vehicle_owner_data