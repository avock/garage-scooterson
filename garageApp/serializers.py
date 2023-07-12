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
        # vehicle_info_data = validated_data.pop('vehicle_info', {})
        vehicle_status_data = validated_data.pop('vehicle_status', {})
        
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
        
class VehicleInfoDeserializer(serializers.Serializer):
    model = serializers.CharField()
    type = serializers.CharField()
    manufacture = serializers.CharField()
    model_year = serializers.IntegerField()
    color = serializers.CharField()
    width=serializers.IntegerField()
    height=serializers.IntegerField()
    length=serializers.IntegerField()
    top_speed = serializers.IntegerField()
    mileage = serializers.IntegerField()
    power = serializers.IntegerField()
    sn = serializers.CharField()
    motor = serializers.CharField()
    ecu = serializers.CharField()
    gsm = serializers.CharField()
    gps = serializers.CharField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        dimensions = {
            'width': representation.pop('width'),
            'height': representation.pop('height'),
            'length': representation.pop('length'),
        }
        parameters = {
            'top_speed': representation.pop('top_speed'),
            'mileage': representation.pop('mileage'),
            'power': representation.pop('power')
        }
        configuration = {
            'sn': representation.pop('sn'),
            'motor': representation.pop('motor'),
            'ecu': representation.pop('ecu'),
            'gsm': representation.pop('gsm'),
            'gps': representation.pop('gps')
        }
        representation['dimensions'] = dimensions
        representation['parameters'] = parameters
        representation['configuration'] = configuration
        return representation