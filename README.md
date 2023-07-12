# API Documentation
### Created by Chun Khai on 04/07/2023

This document provides an overview of the available endpoints in the Scooterson Garage API.
(temporary) try it out on http://localhost:8080/\
UPDATE: try it out on https://garage-scooterson.vercel.app/

Please read the ```projectSetup.md``` file to setup your coding environment.

To run, go into the ```garage``` sub-directory and run ```python3 manage.py runserver```

## Global Garage Endpoints

### Get List of Vehicles in Global Garage

- Endpoint: `/garage`
- Method: GET
- Description: Retrieves a list of all vehicles.

### Get Specific Vehicle in Global Garage

- Endpoint: `/garage/{vehicle_id}`
- Method: GET
- Description: Retrieves details of a specific vehicle.
- Path Parameters:jsut le 
  - `vehicle_id`: Unique identifier of the vehicle.

### Add Vehicle to Global Garage

- Endpoint: `/garage`
- Method: POST
- Description: Adds a vehicle to the global garage
- Request Body: Vehicle object data.

### Delete Specific Vehicle from Global Garage 

- Endpoint: `/garage/{pk}`
- Method: DELETE
- Description: Deletes a specific vehicle from the global garage.
- Path Parameters:
  - `pk`: Unique identifier of the vehicle.

## User Garage Endpoints

### Get All User Vehicles

- Endpoint: `/user/{user_id}`
- Method: GET
- Description: Retrieves a list of vehicles bonded to the user 
- Path Parameters:
  - `user_id`: Unique identifier of the user.

  ### Delete All User Vehicles

- Endpoint: `/user/{user_id}`
- Method: DELETE
- Description: Deletes all vehicles bonded to the user 
- Path Parameters:
  - `user_id`: Unique identifier of the user.
  - `vehicle_id`: Unique identifier of the vehicle.

### Get Specific User Vehicles
- Endpoint: `/user/{user_id}/{vehicle_id}`
- Method: GET
- Description: Retrieves specific vehicles bonded to the user 
- Path Parameters:
  - `user_id`: Unique identifier of the user.
  - `vehicle_id`: Unique identifier of the vehicle.

### Update Specific User Vehicles
- Endpoint: `/user/{user_id}/{vehicle_id}`
- Method: POST
- Description: Bounds vehicle to a user 
- Path Parameters:
  - `user_id`: Unique identifier of the user.
  - `vehicle_id`: Unique identifier of the vehicle.

### Delete Specific User Vehicles
- Endpoint: `/user/{user_id}/{vehicle_id}`
- Method: DELETE 
- Description: Deletes specific vehicles bonded to the user 
- Path Parameters:
  - `user_id`: Unique identifier of the user.
  - `vehicle_id`: Unique identifier of the vehicle.
