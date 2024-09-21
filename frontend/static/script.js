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
