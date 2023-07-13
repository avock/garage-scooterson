document.getElementById('form-generate').addEventListener('submit', function(event) {
    event.preventDefault();
    var vehicleId = document.getElementById('vehicleId').value;
    var ownerId = document.getElementById('ownerId').value;

    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    myHeaders.append("X-API-Key", "{{token}}");

    var raw = JSON.stringify({
        "vehicle_name": "A-Orange",
        "vehicle_id": vehicleId,
        "vehicle_owner_id": ownerId,
        "vehicle_uuid": "0818a87e-1f2a-486b-be0b-a1481a18476d",
        "vehicle_pub_key": "wveFrDR9TsaNSoDdZvh8qYG1GTW/UQpzYtuRXMyhHXk=",
        "particle_id": "12345",
        "particle_serial": "12345",
        "particle_name": "yogurt",
        "shared_vehicle_data": {
            "is_occupied": false,
            "sharing_enabled": true,
            "is_request_pending": false,
            "idle_time_option": 2,
            "max_assist_level": 2
        },
        "shared_vehicle_owner_data": {
            "address_line1": "789 Elm Street",
            "address_line2": "Unit 12-34",
            "city": "Singapore",
            "state": "",
            "zipcode": "123456",
            "email": "john.doe@example.com",
            "mobile_number": "+65 9123 4567",
            "name": {
            "first_name": "Deepansh",
            "last_name": "Jain"
            },
            "user_id": 456,
            "birth_date": "1990-06-15",
            "gender": "male",
            "weight": 70,
            "profile_pic_url_string": "https://i1.sndcdn.com/artworks-000128560053-3cpc8a-t500x500.jpg",
            "profile_image": "image.jpg",
            "email_verified": true,
            "user_address": {
            "latitude": "1.3521",
            "longitude": "103.8198"
            },
            "full_name": "Deepansh Jain",
            "address": "789 Elm Street Unit 12-34",
            "weight_in_kg": 70
        },
        "vehicle_info": {
            "model": "Rolley Plus",
            "type": "Scooter",
            "manufacture": "Scooterson",
            "model_year": 2023,
            "color": "Orange",
            "dimension": {
            "width": 700,
            "height": 1040,
            "length": 1620
            },
            "parameters": {
            "top_speed": 30,
            "mileage": 80,
            "power": 2
            },
            "configuration": {
            "sn": "2323232121",
            "motor": "pleasjsak",
            "ecu": "sds23232232",
            "gsm": "323242422",
            "gps": "255:255:255.0"
            }
        },
        "vehicle_status": {
            "battery_percentage": 100,
            "power_on": false,
            "sharing_on": false,
            "alarm_on": true,
            "last_sync": "12:40:31",
            "is_occupied": false,
            "odo_meter": 324,
            "trip_meter": 109,
            "gear_mode": 16
        }
    });

    var requestOptions = {
        method: 'POST',
        body: raw,
    };
    
    fetch("https://garage-scooterson.vercel.app/garage", requestOptions)
        .then(response => response.text())
        .then(result => console.log(result))
        .catch(error => console.log('error', error));

});

document.getElementById('form-update').addEventListener('submit', function(event) {
    event.preventDefault();

    fetch('http://localhost:8000/garage')
        .then(response => response.json())
        .then(data => {
            vehicle_array = data.vehicles
            console.log(vehicle_array[0].vehicle_id)
            console.log(vehicle_array[1])
            console.log(vehicle_array[1].shared_vehicle_owner_data.user_address)
        })

})

function refreshVehicleList() {
    var vehicleSelector = document.getElementById("vehicleSelector");
    vehicleSelector.innerHTML = ""; // Clear existing dropdown options

    vehicles.forEach(vehicle => {
      var option = document.createElement("option");
      option.value = vehicle.vehicle_id;
      option.textContent = "Vehicle ID " + vehicle.vehicle_id;
      vehicleSelector.appendChild(option);
    })
}


