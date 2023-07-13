from django.shortcuts import render
import json

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from django.db import IntegrityError
 
from garageApp.models import GarageApp, VehicleStatus, VehicleInfo, UserVehicles, SharedVehicleData, SharedVehicleOwnerData
from garageApp.serializers import GarageSerializer, GarageDeserializer, VehicleStatusSerializer, VehicleInfoSerializer, vehicleInfoDeserilizer, GarageUpdater, SharedVehicleDataSerializer, SharedVehicleOwnerDataSerializer, sharedVehicleOwnerDataDeserializer
from rest_framework.decorators import api_view

from datetime import datetime
from django.http import HttpResponse
def index(request):
        now = datetime.now()
        html = f'''
        <html>
            <body>
                <h1>Hello from Vercel!</h1>
                <p>The current time is { now }.</p>
            </body>
        </html>
        '''
        return HttpResponse(html)


@api_view(['GET', 'POST', 'DELETE'])
def garage_list(request):
    # GET list of garage, POST a new garage, DELETE all garages
    if request.method == 'GET':
        garage = GarageApp.objects.all()
        
        garage_deserializer = GarageDeserializer(garage, many=True)
        garage_data = garage_deserializer.data
        
        def get_model_fields(model):
            return [field.name for field in model._meta.get_fields() if field.name != 'garage']

        for garage in garage_data:
            vehicle_id = garage['vehicle_id']
            
            # obtaining instance in DB
            vehicle_status_model = VehicleStatus
            # retrieving information/fields about that instance
            vehicle_status_fields = get_model_fields(vehicle_status_model)
            # filtering out the correct information/field
            vehicle_status_values = vehicle_status_model.objects.filter(garage_id=vehicle_id).values(*vehicle_status_fields).first()
            # setting its 'vehicle_status' field
            garage['vehicle_status'] = vehicle_status_values
            
            vehicle_info_model = VehicleInfo
            vehicle_info_fields = get_model_fields(vehicle_info_model)
            vehicle_info_values = vehicle_info_model.objects.filter(garage_id=vehicle_id).values(*vehicle_info_fields).first()
            nested_vehicle_info_values = vehicleInfoDeserilizer(vehicle_info_values)
            garage['vehicle_info'] = nested_vehicle_info_values
            
            shared_vehicle_data_model = SharedVehicleData
            shared_vehicle_data_fields = get_model_fields(shared_vehicle_data_model)
            shared_vehicle_data_values = shared_vehicle_data_model.objects.filter(garage_id=vehicle_id).values(*shared_vehicle_data_fields).first()
            garage['shared_vehicle_data'] = shared_vehicle_data_values
            
            shared_vehicle_owner_data_model = SharedVehicleOwnerData
            shared_vehicle_owner_data_fields = get_model_fields(shared_vehicle_owner_data_model)
            shared_vehicle_owner_data_values = shared_vehicle_owner_data_model.objects.filter(garage_id=vehicle_id).values(*shared_vehicle_owner_data_fields).first()
            nested_shared_vehicle_owner_data_values = sharedVehicleOwnerDataDeserializer(shared_vehicle_owner_data_values)
            print(nested_shared_vehicle_owner_data_values)
            print(shared_vehicle_owner_data_values)
            garage['shared_vehicle_owner_data'] = nested_shared_vehicle_owner_data_values
            
        # 'safe=False' for objects serialization
        count = len(garage_data)
        success_message = f"GET Succesful. {count} vehicles found in the global garage."
        return JsonResponse(
            {"response": success_message,
             "vehicles": garage_data},
            safe=False)

    elif request.method == 'POST':
        garage_data = JSONParser().parse(request)
        garage_serializer = GarageSerializer(data=garage_data)
            
        if garage_serializer.is_valid():
            vehicle_status_data = garage_data.get("vehicle_status")
            vehicle_info_data = garage_data.get("vehicle_info")
            shared_vehicle_data = garage_data.get('shared_vehicle_data')
            shared_vehicle_owner_data = garage_data.get('shared_vehicle_owner_data')
            
            vehicle_status_serializer = VehicleStatusSerializer(data=vehicle_status_data)
            vehicle_info_serializer = VehicleInfoSerializer(data=vehicle_info_data)
            shared_vehicle_data_serializer = SharedVehicleDataSerializer(data=shared_vehicle_data)
            shared_vehicle_owner_data_serializer = SharedVehicleOwnerDataSerializer(data=shared_vehicle_owner_data)
            
            if vehicle_status_serializer.is_valid() & vehicle_info_serializer.is_valid() & shared_vehicle_data_serializer.is_valid() & shared_vehicle_owner_data_serializer.is_valid(): 
                # ONLY save garage_serializer since other sub-serializers are handled within garage_serializer
                garage_serializer.save()
                return JsonResponse(garage_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse(vehicle_status_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(garage_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    elif request.method == 'DELETE':
        count = GarageApp.objects.all().count()
        GarageApp.objects.all().delete()     
        
        if count > 0: 
            success_message = 'Found and deleted {} vehicle(s) successfully!'.format(count)
        else:
            success_message = 'There are no vehicles in the garage.'
            
        return JsonResponse(
            {'response': success_message},
            status=status.HTTP_204_NO_CONTENT)            
            
@api_view(['GET', 'POST', 'DELETE'])
def garage_detail(request, pk):
    # find garage by pk (id)
    filtered_garage = GarageApp.objects.filter(vehicle_id=pk)
    particle_id_filtered_garage = GarageApp.objects.filter(particle_id=pk)
    
    if (not filtered_garage and not particle_id_filtered_garage):
        error_message = f"Vehicle '{pk}' does not exist."
        return JsonResponse(
            {"response": error_message}, 
            status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET': 
        garage_deserializer = GarageDeserializer(particle_id_filtered_garage, many=True)
        garage_data = garage_deserializer.data
        
        # For now assuming > 1 garage with same vehicle_id, to remove in the future
        def get_model_fields(model):
            return [field.name for field in model._meta.get_fields() if field.name != 'garage']

        for garage in garage_data:
            vehicle_id = garage['vehicle_id']
            
            # for explanation search the top GET method
            vehicle_status_model = VehicleStatus
            vehicle_status_fields = get_model_fields(vehicle_status_model)
            vehicle_status_values = vehicle_status_model.objects.filter(garage_id=vehicle_id).values(*vehicle_status_fields).first()
            garage['vehicle_status'] = vehicle_status_values
            
            vehicle_info_model = VehicleInfo
            vehicle_info_fields = get_model_fields(vehicle_info_model)
            vehicle_info_values = vehicle_info_model.objects.filter(garage_id=vehicle_id).values(*vehicle_info_fields).first()
            garage['vehicle_info'] = vehicle_info_values
            
            shared_vehicle_data_model = SharedVehicleData
            shared_vehicle_data_fields = get_model_fields(shared_vehicle_data_model)
            shared_vehicle_data_values = shared_vehicle_data_model.objects.filter(garage_id=vehicle_id).values(*shared_vehicle_data_fields).first()
            garage['shared_vehicle_data'] = shared_vehicle_data_values
            
            shared_vehicle_owner_data_model = SharedVehicleOwnerData
            shared_vehicle_owner_data_fields = get_model_fields(shared_vehicle_owner_data_model)
            shared_vehicle_owner_data_values = shared_vehicle_owner_data_model.objects.filter(garage_id=vehicle_id).values(*shared_vehicle_owner_data_fields).first()
            garage['shared_vehicle_owner_data'] = shared_vehicle_owner_data_values
            
        # 'safe=False' for objects serialization
        success_message = f"GET Succesful. Found vehicle with Particle ID={pk}."
        return JsonResponse(
            {"response": success_message,
             "vehicles": garage_data},
            safe=False)
    
    elif request.method == 'POST':
        try:
            garage_instance = GarageApp.objects.get(vehicle_id=pk)
            vehicle_status_instance = VehicleStatus.objects.get(garage_id=pk)
            vehicle_info_instance = VehicleInfo.objects.get(garage_id=pk)
            shared_vehicle_data_instance = SharedVehicleData.objects.get(garage_id=pk)
            shared_vehicle_owner_data_instance = SharedVehicleOwnerData.objects.get(garage_id=pk)
            
        except GarageApp.DoesNotExist:
            error_message = f"Vehicle '{pk}' does not exist."
            return JsonResponse(
                {"response": error_message}, 
                status=status.HTTP_404_NOT_FOUND)
        
        garage_data = JSONParser().parse(request)
        vehicle_status_data = garage_data.get("vehicle_status")
        vehicle_info_data = garage_data.get("vehicle_info")
        shared_vehicle_data = garage_data.get("shared_vehicle_data")
        shared_vehicle_owner_data = garage_data.get("shared_vehicle_owner_data")
            
        garage_serializer = GarageUpdater(garage_instance, data=garage_data, partial=True)
        vehicle_status_serializer = VehicleStatusSerializer()
        vehicle_info_serializer = VehicleInfoSerializer()
        shared_vehicle_data_serializer = SharedVehicleDataSerializer()
        shared_vehicle_owner_data_serializer = SharedVehicleOwnerDataSerializer()

        if garage_serializer.is_valid():
            garage_serializer.save()
            
            success_message = f"Vehicle {pk} updated successfully"
            
            if vehicle_status_data:
                vehicle_status_serializer.update(vehicle_status_instance, vehicle_status_data)

            if vehicle_info_data:
                vehicle_info_serializer.update(vehicle_info_instance, vehicle_info_data)

            if shared_vehicle_data:
                shared_vehicle_data_serializer.update(shared_vehicle_data_instance, shared_vehicle_data)

            if shared_vehicle_owner_data:
                shared_vehicle_owner_data_serializer.update(shared_vehicle_owner_data_instance, shared_vehicle_owner_data)

            response_data = {
                "response": success_message,
                "changes": garage_data
            }
            
            return JsonResponse(response_data)
        
        return JsonResponse(garage_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE': 
        filtered_garage.delete()
        
        success_message = f"Vehicle {pk} deleted successfully"
        return JsonResponse(
            {'response': success_message},
            status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'DELETE'])
def user_vehicles(request, user_id, id):
    try:
        if request.method == 'GET':
            binded_vehicles = UserVehicles.objects.filter(userID=user_id, vehicle_id=id)
            vehicle_ids = binded_vehicles.values_list('vehicle_id', flat=True)
            
            filtered_garage = GarageApp.objects.filter(vehicle_id__in=vehicle_ids)
            garage_deserializer = GarageDeserializer(filtered_garage, many=True)
            garage_data = garage_deserializer.data
            
            def get_model_fields(model):
                return [field.name for field in model._meta.get_fields() if field.name != 'garage']

            for garage in garage_data:
                vehicle_id = garage['vehicle_id']
                
                # for explanation search the top GET method
                vehicle_status_model = VehicleStatus
                vehicle_status_fields = get_model_fields(vehicle_status_model)
                vehicle_status_values = vehicle_status_model.objects.filter(garage_id=vehicle_id).values(*vehicle_status_fields).first()
                garage['vehicle_status'] = vehicle_status_values
                
                vehicle_info_model = VehicleInfo
                vehicle_info_fields = get_model_fields(vehicle_info_model)
                vehicle_info_values = vehicle_info_model.objects.filter(garage_id=vehicle_id).values(*vehicle_info_fields).first()
                garage['vehicle_info'] = vehicle_info_values
                
                shared_vehicle_data_model = SharedVehicleData
                shared_vehicle_data_fields = get_model_fields(shared_vehicle_data_model)
                shared_vehicle_data_values = shared_vehicle_data_model.objects.filter(garage_id=vehicle_id).values(*shared_vehicle_data_fields).first()
                garage['shared_vehicle_data'] = shared_vehicle_data_values
                
                shared_vehicle_owner_data_model = SharedVehicleOwnerData
                shared_vehicle_owner_data_fields = get_model_fields(shared_vehicle_owner_data_model)
                shared_vehicle_owner_data_values = shared_vehicle_owner_data_model.objects.filter(garage_id=vehicle_id).values(*shared_vehicle_owner_data_fields).first()
                garage['shared_vehicle_owner_data'] = shared_vehicle_owner_data_values
                
            # 'safe=False' for objects serialization
            success_message = f"Found {len(garage_data)} vehicle(s) with ID={id} for user {user_id}"
            return JsonResponse(
                {"response": success_message,
                 "data": garage_data},
                safe=False)
        
        elif request.method == 'POST':
            # try:
                user_info_instance = UserVehicles.objects.create(userID=user_id, vehicle_id=id)
                if(user_info_instance):
                    success_message = f"Vehicle with ID={id} is succesfully binded to user with ID={user_id}"
                    return JsonResponse(
                        {"message": success_message})
                else:
                    return JsonResponse({"message": "fail"})
            # except ValueError:
            #     error_message = f"Vehicle with ID={id} not found, please enter a valid vehicle ID"
            #     return JsonResponse(
            #         {"message": error_message})              
            
        elif request.method == 'DELETE':
            filtered_user_vehicles = UserVehicles.objects.filter(userID=user_id, vehicle_id=id)
            if (filtered_user_vehicles):
                filtered_user_vehicles.delete()
                
                success_message = f"Vehicle with ID={id} is no longer binded to user with ID={user_id}"
                return JsonResponse(
                    {"response": success_message},
                    status=status.HTTP_201_CREATED)
            else:
                error_message = f"Binded pair of Vehicle ID={id} and User ID={user_id} not found"
                return JsonResponse(
                    {"response": error_message},
                    status=status.HTTP_400_BAD_REQUEST)
            
    except IntegrityError:
        error_message = f"Vehicle with ID={id} has already been binded to user with ID={user_id}"
        return JsonResponse(
            {"error": error_message},
            status=400)     
        
@api_view(['GET', 'DELETE'])
def user(request, user_id):
    if request.method == 'GET':
        binded_vehicles = UserVehicles.objects.filter(userID=user_id)
        vehicle_ids = binded_vehicles.values_list('vehicle_id', flat=True)
        
        filtered_garage = GarageApp.objects.filter(vehicle_id__in=vehicle_ids)
        garage_deserializer = GarageDeserializer(filtered_garage, many=True)
        garage_data = garage_deserializer.data
        
        def get_model_fields(model):
            return [field.name for field in model._meta.get_fields() if field.name != 'garage']

        for garage in garage_data:
            vehicle_id = garage['vehicle_id']
            
            # for explanation search the top GET method
            vehicle_status_model = VehicleStatus
            vehicle_status_fields = get_model_fields(vehicle_status_model)
            vehicle_status_values = vehicle_status_model.objects.filter(garage_id=vehicle_id).values(*vehicle_status_fields).first()
            garage['vehicle_status'] = vehicle_status_values
            
            vehicle_info_model = VehicleInfo
            vehicle_info_fields = get_model_fields(vehicle_info_model)
            vehicle_info_values = vehicle_info_model.objects.filter(garage_id=vehicle_id).values(*vehicle_info_fields).first()
            garage['vehicle_info'] = vehicle_info_values
            
            
            
        # 'safe=False' for objects serialization
        success_message = f"Found {len(garage_data)} vehicles for user {user_id}"
        return JsonResponse(
            {"response": success_message,
                "data": garage_data},
            safe=False)
        
    elif request.method == 'DELETE':
        filtered_user = UserVehicles.objects.filter(userID=user_id)
        if (filtered_user):
            filtered_user.delete()
            
            success_message = f"User with ID={user_id} is no longer binded to any vehicles"
            return JsonResponse(
                {"response": success_message},
                status=status.HTTP_201_CREATED)
        else:
            error_message = f"User with ID={user_id} is not found"
            return JsonResponse(
                {"response": error_message},
                status=status.HTTP_400_BAD_REQUEST)
            
# TODO: add random data