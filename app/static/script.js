function checkAuthStatus() {
    fetch('/check-auth')
    .then(response => response.json())
    .then(data => {
        if (data.is_authenticated) {
            // User is logged in, show main content and logout button
            document.getElementById('main-content').style.display = 'block';
            document.getElementById('logout-btn').style.display = 'block';
            document.getElementById('login-btn').style.display = 'none';
        } else {
            // User is not logged in, show login button and hide main content
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

const healthConditions = ["Asthma", "Diabetes", "Hypertension", "Allergies", "COPD", "Cancer"]; // Add more conditions
const allergiesList = ["Pollen", "Peanuts", "Dust", "Gluten", "Lactose", "Pet dander"]; // Add more allergies

// Function to filter suggestions based on input
function filterSuggestions(input, list) {
    return list.filter(item => item.toLowerCase().includes(input.toLowerCase()));
}

// Function to display suggestions
function displaySuggestions(inputId, suggestionsDivId, list, listId) {
    const input = document.getElementById(inputId);
    const suggestionsDiv = document.getElementById(suggestionsDivId);

    input.addEventListener('input', () => {
        const query = input.value;
        const suggestions = filterSuggestions(query, list);
        
        suggestionsDiv.innerHTML = '';
        suggestions.forEach(suggestion => {
            const suggestionItem = document.createElement('div');
            suggestionItem.textContent = suggestion;
            suggestionItem.classList.add('suggestion-item');
            suggestionItem.addEventListener('click', () => addToList(suggestion, listId));
            suggestionsDiv.appendChild(suggestionItem);
        });
    });
}

function addToList(item, listId) {
    const list = document.getElementById(listId);
    const chip = document.createElement('li'); // Create an 'li' for each chip
    chip.textContent = item;
    
    const removeButton = document.createElement('button');
    removeButton.textContent = 'x';
    removeButton.classList.add('remove-chip');
    
    // Remove chip on click
    removeButton.addEventListener('click', () => chip.remove());
    
    chip.appendChild(removeButton);
    list.appendChild(chip); // Add the chip to the correct list
}

// Initialize suggestions for conditions and allergies
displaySuggestions('condition-input', 'condition-suggestions', healthConditions, 'conditions-list');
displaySuggestions('allergies-input', 'allergy-suggestions', allergiesList, 'allergies-list');

// Handle form submission
document.getElementById('user-form')?.addEventListener('submit', function(event) {
    event.preventDefault();
    
    const allergies = document.getElementById('allergies')?.value;
    const financial = document.getElementById('financial').value;

    // Submit the data to your backend here

    // Display results (for now, simulate results)
    document.getElementById('results').innerHTML = `
        <p>Allergies: ${allergies}</p>
        <p>Financial Standing: $${financial}</p>
    `;
});

// Handle health condition selection
document.getElementById('condition-select')?.addEventListener('change', function() {
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

// Call authentication check (bypassed for testing)
checkAuthStatus();
