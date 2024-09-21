// Function to check if the user is authenticated
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
    // Redirect to Flask login route
    window.location.href = '/login';
});

// Handle logout
document.getElementById('logout-btn').addEventListener('click', function() {
    // Redirect to Flask logout route
    window.location.href = '/logout';
});

// Handle form submission
document.getElementById('search-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const condition = document.getElementById('condition').value;

    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ condition: condition })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('results').innerHTML = `
            <p>Recommended City: ${data.city}</p>
            <p>Average Cost of Living: $${data.cost}</p>
            <p>Number of Hospitals: ${data.hospitals}</p>
        `;
    })
    .catch(error => console.error('Error:', error));
});

// Check authentication status on page load
checkAuthStatus();
