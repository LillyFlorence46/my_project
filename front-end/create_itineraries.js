document.getElementById('itinerary-form').addEventListener('submit', function(event) {
    event.preventDefault(); 
    var formData = new FormData(this);

    fetch('http://127.0.0.1:5000/createitinerary', {
        method: 'POST',
        body: formData,
        
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = './view-itinerary.html'; // Redirect to the view-itinerary page
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
