let vehicleArray = []

document.getElementById('add-vehicle').addEventListener('click', function(event) {
    event.preventDefault();
    var vehicleName = document.getElementById('newVehicleName').value;
    var vehicleUUID = document.getElementById('newVehicleUUID').value;
    var vehiclePubKey = document.getElementById('newVehiclePubKey').value;
    var particle_id = document.getElementById('newParticleID').value;
    var particle_serial = document.getElementById('newParticleSerial').value;
    var particle_name = document.getElementById('newParticleName').value;

    if (!particle_name) particle_name = 'Yogurt'

    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    myHeaders.append("X-API-Key", "{{token}}");

    var raw = JSON.stringify({
        "vehicle_name": vehicleName,
        "vehicle_owner_id": "1",
        "vehicle_uuid": vehicleUUID,
        "vehicle_pub_key": vehiclePubKey,
        "particle_id": particle_id,
        "particle_serial": particle_serial,
        "particle_name": particle_name,
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
    
    displayAdding();
    let response_status;
    fetch("https://garage-scooterson.vercel.app/garage", requestOptions)
        .then(response =>{
          console.log(response)
          response_status = response.status
        })
        .then(result => {
          hideAdding()
          clearAddForm
          const addResponse = document.getElementById('addVehicleResponse')
          if (response_status === 400) {
            addResponse.textContent = 'Vehicle Name and Owner ID must not be left blank.'

          } else if (response_status === 201) {
            addResponse.textContent = 'Vehicle added succesfully.'

          } else {
            addResponse.textContent = 'Something went wrong, please refresh.'
          }
        })
        .catch(error => {
          const addResponse = document.getElementById('addVehicleResponse')
          // addResponse.textContent = error
          console.log('error', error)
        });
});

document.getElementById('refresh-vehicles').addEventListener('click', function() {
    clearUpdateForm();
    fetchVehicles();
});

document.getElementById('update-vehicle').addEventListener('click', function() {

    const updateVehicleButton = document.getElementById('update-vehicle')
    const vehicleSelect = document.getElementById('vehicleSelect');
    const selectedVehicleId = vehicleSelect.value;

    const updateResponse = document.getElementById('updateVehicleResponse')

    const selectedVehicleData = vehicleArray.find(vehicle => vehicle.vehicle_id === selectedVehicleId);    // obtaining user input

    // Perform POST request to localhost:8000/garage/selectedVehicleId
    displayUpdating()
    // if vehicle-to-update is selected
    if (selectedVehicleData) {
      // target-vehicle is selected, proceed to fetch required data
      const newVehicleID = document.getElementById('vehicleID').value;
      const newVehicleUUID = document.getElementById('vehicleUUID').value;
      const newVehicleName = document.getElementById('vehicleName').value;
  
      // updating vehicle_data
      selectedVehicleData.vehicle_name = newVehicleName;
      selectedVehicleData.vehicle_id = newVehicleID;
      selectedVehicleData.vehicle_uuid = newVehicleUUID;

      fetch(`https://garage-scooterson.vercel.app/garage/${selectedVehicleId}`, {
        // fetch(`http://localhost:8000/garage/${selectedVehicleId}`, {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify(selectedVehicleData)
        })
            .then(response => response.json())
            .then(data => {
              hideUpdating()
              
            })
            .catch(error => {
              console.log('test')
            });
    } else {
      hideUpdating()
      updateResponse.textContent = 'Please select a vehicle to update.'
    }
});

// Event listener for vehicle selection
document.getElementById('vehicleSelect').addEventListener('change', function() {
    updateForm();
});  

// Fetch vehicles from localhost:8000/garage and populate vehicleArray
function fetchVehicles() {
    displayLoading();
    const updateResponse = document.getElementById('updateVehicleResponse')

    fetch('https://garage-scooterson.vercel.app/garage')
    // fetch('http://localhost:8000/garage')
      .then(response => response.json())
      .then(data => {
        hideLoading()
        vehicleArray = data.vehicles
        populateVehicleDropdown()
        updateForm()
        if (vehicleArray) {
          updateResponse.textContent = data.response
      
        } else {
          updateResponse.textContent = 'Something went wrong, please refresh.'
        }
      })        
      .catch(error => {
        console.log(error)
      });
}
  
  // Populate the dropdown with vehicle IDs
  function populateVehicleDropdown() {
    const vehicleSelect = document.getElementById('vehicleSelect');
    vehicleArray.forEach(vehicle => {
      const option = document.createElement('option');
      option.value = vehicle.vehicle_id;
      option.text = vehicle.vehicle_id;
      vehicleSelect.appendChild(option);
    });
  }
  
  // Update the form with vehicle details based on the selected vehicle ID
  function updateForm() {
    const vehicleSelect = document.getElementById('vehicleSelect');
    const selectedVehicleId = vehicleSelect.value;
    const selectedVehicle = vehicleArray.find(vehicle => vehicle.vehicle_id === selectedVehicleId);
    if (selectedVehicle) {
      document.getElementById('vehicleName').value = selectedVehicle.vehicle_name;
      document.getElementById('vehicleID').value = selectedVehicle.vehicle_id;
      document.getElementById('vehicleUUID').value = selectedVehicle.vehicle_uuid;
    } else {
      clearUpdateForm();
    }
  }
  
  // Clear the form fields
  function clearUpdateForm() {
    document.getElementById('vehicleName').value = '';
    document.getElementById('vehicleID').value = '';
    document.getElementById('vehicleUUID').value = '';
  }

  function clearAddForm() {
    document.getElementById('newVehicleName').value = '';
    document.getElementById('newVehicleUUID').value = '';
    document.getElementById('newVehiclePubKey').value = '';
    document.getElementById('newParticleID').value = '';
    document.getElementById('newParticleSerial').value = '';
    document.getElementById('newParticleName').value = '';
  }

  function displayLoading() {
    const refreshVehiclesButton = document.getElementById('refresh-vehicles')
    refreshVehiclesButton.classList.add('button--loading')
    refreshVehiclesButton.textContent = ' '
  }

  function displayAdding() {
    const addVehicleButton = document.getElementById('add-vehicle')
    addVehicleButton.classList.add('button--loading')
    addVehicleButton.textContent = ' '
  }

  function displayUpdating() {
    const addVehicleButton = document.getElementById('update-vehicle')
    addVehicleButton.classList.add('button--loading')
    addVehicleButton.textContent = ' '
  }

  function hideLoading() {
    const refreshVehiclesButton = document.getElementById('refresh-vehicles')
    refreshVehiclesButton.classList.remove('button--loading')
    refreshVehiclesButton.textContent = 'Refresh Vehicle List'
  }

  function hideAdding() {
    const addVehicleButton = document.getElementById('add-vehicle')
    addVehicleButton.classList.remove('button--loading')
    addVehicleButton.textContent = 'Add Vehicle'
  }

  function hideUpdating() {
    const addVehicleButton = document.getElementById('update-vehicle')
    addVehicleButton.classList.remove('button--loading')
    addVehicleButton.textContent = 'Update Vehicle'
  }