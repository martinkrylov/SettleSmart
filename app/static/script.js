// Function to check if the user is authenticated
function checkAuthStatus() {
    fetch('/check-auth')
    .then(response => response.json())
    .then(data => {
        if (data.is_authenticated) {
            document.getElementById('main-content').style.display = 'block';
            document.getElementById('logout-btn').style.display = 'block';
            document.getElementById('login-btn').style.display = 'none';
        } else {
            document.getElementById('main-content').style.display = 'none';
            document.getElementById('login-btn').style.display = 'block';
            document.getElementById('logout-btn').style.display = 'none';
        }
    })
    .catch(error => console.error('Error checking auth status:', error));
}

// Handle login
document.getElementById('login-btn').addEventListener('click', function() {
    window.location.href = '/login';
});

// Handle logout
document.getElementById('logout-btn').addEventListener('click', function() {
    window.location.href = '/logout';
});

// Handle form submission
document.getElementById('user-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const allergies = document.getElementById('allergies').value;
    const financial = document.getElementById('financial').value;

    // Submit the data to your backend here

    // Display results (for now, simulate results)
    document.getElementById('results').innerHTML = `
        <p>Allergies: ${allergies}</p>
        <p>Financial Standing: $${financial}</p>
    `;
});

// Handle health condition selection
document.getElementById('condition-select').addEventListener('change', function() {
    const selectedConditions = Array.from(this.selectedOptions).map(option => option.value);
    const conditionsList = document.getElementById('conditions-list');
    conditionsList.innerHTML = ''; // Clear previous list

    selectedConditions.forEach(condition => {
        const li = document.createElement('li');
        li.textContent = condition;
        conditionsList.appendChild(li);
    });
});

// Initialize Google Maps
function initMap() {
    const map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: -34.397, lng: 150.644 },
        zoom: 8
    });

    // Get user's current location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            const pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            map.setCenter(pos);
            new google.maps.Marker({
                position: pos,
                map: map,
                title: "Current Location"
            });
        }, function() {
            console.error("Geolocation failed.");
        });
    }
}

// Load the map on window load
window.onload = initMap;

// Check authentication status on page load
checkAuthStatus();
