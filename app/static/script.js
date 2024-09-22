// Check user authentication status
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
document.getElementById('login-btn')?.addEventListener('click', function() {
    window.location.href = '/login';
});

// Handle logout
document.getElementById('logout-btn')?.addEventListener('click', function() {
    window.location.href = '/logout';
});

// Health conditions and allergies data
const healthConditions = medical_conditions = [
    "Lung cancer",
    "Breast cancer",
    "Prostate cancer",
    "Colorectal cancer",
    "Bladder cancer",
    "Non-Hodgkin lymphoma",
    "Melanoma",
    "Kidney cancer",
    "Endometrial cancer",
    "Leukemia",
    "Pancreatic cancer",
    "Liver cancer",
    "Thyroid cancer",
    "Oral cancer",
    "Ovarian cancer",
    "Testicular cancer",
    "Hypertension",
    "Diabetes",
    "Chronic Obstructive Pulmonary Disease",
    "Asthma",
    "Chronic kidney disease",
    "Alzheimer’s disease",
    "Arthritis",
    "Heart disease",
    "Multiple sclerosis",
    "Parkinson’s disease",
    "HIV/AIDS",
    "Lupus",
    "Cystic fibrosis",
    "Irritable Bowel Syndrome",
    "Inflammatory Bowel Disease",
    "Fibromyalgia",
    "Chronic fatigue syndrome",
    "Psoriasis",
    "Sickle cell disease"
]; // Add more conditions
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

        // Show the suggestion box only when there is input
        if (query.trim() !== "") {
            const suggestions = filterSuggestions(query, list);

            suggestionsDiv.innerHTML = '';  // Clear previous suggestions
            suggestionsDiv.style.display = 'block';  // Show suggestion box

            suggestions.forEach(suggestion => {
                const suggestionItem = document.createElement('div');
                suggestionItem.textContent = suggestion;
                suggestionItem.classList.add('suggestion-item');
                
                // Add to the list only if the entry doesn't already exist
                suggestionItem.addEventListener('click', () => addToList(suggestion, listId));
                
                suggestionsDiv.appendChild(suggestionItem);
            });
        } else {
            suggestionsDiv.style.display = 'none';  // Hide the suggestion box if there's no input
        }
    });
}

// Function to add a selected item (condition or allergy) to the list, ensuring no duplicates
function addToList(item, listId) {
    const list = document.getElementById(listId);
    const existingItems = Array.from(list.getElementsByTagName('li')).map(li => li.textContent.trim().replace('x', ''));

    // Only add the item if it doesn't already exist in the list
    if (!existingItems.includes(item)) {
        const chip = document.createElement('li'); // Create a list item for the selected item
        chip.textContent = item;
        
        const removeButton = document.createElement('button');
        removeButton.textContent = 'x';
        removeButton.classList.add('remove-chip');
        
        // Remove item on click
        removeButton.addEventListener('click', () => chip.remove());
        
        chip.appendChild(removeButton);
        list.appendChild(chip);  // Add the item to the list
    }
}

// Initialize suggestions for conditions and allergies
displaySuggestions('condition-input', 'condition-suggestions', healthConditions, 'conditions-list');
displaySuggestions('allergies-input', 'allergy-suggestions', allergiesList, 'allergies-list');

// Handle form submission
document.getElementById('user-form').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent default form submission
    
    const financial = document.getElementById('financial').value;
    const selectedConditions = Array.from(document.getElementById('conditions-list').getElementsByTagName('li')).map(li => li.textContent.replace('x', ''));
    const selectedAllergies = Array.from(document.getElementById('allergies-list').getElementsByTagName('li')).map(li => li.textContent.replace('x', ''));

    // Ensure the Auth0 User ID is included (from the script injected in the HTML)
    const userData = {
        financial,
        conditions: selectedConditions,
        allergies: selectedAllergies,
        auth0_user_id: auth0UserId  // Use the dynamically injected Auth0 User ID
    };

    console.log("Submitting user data:", userData);  // Log the data before sending

    // Send POST request to the backend
    fetch('/add_or_update_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // Display results dynamically
        document.getElementById('results').innerHTML = `
            <p>Conditions: ${selectedConditions.join(', ')}</p>
            <p>Allergies: ${selectedAllergies.join(', ')}</p>
            <p>Financial Standing: $${financial}</p>
        `;
    })
    .catch(error => console.error('Error submitting form:', error));
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

// Call authentication check
checkAuthStatus();
