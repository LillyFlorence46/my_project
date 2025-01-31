document.getElementById('loginForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent default form submission

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    console.log(8)
    fetch('http://127.0.0.1:5000/userlogin', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email:email, user_password: password })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.message || 'Login failed');
            });
        }
        return response.json();
    })
    .then(data => {
        console.log(data.message)
        // console.log('login success')
        location.href='index.html'
        if (data.access_token) {
            localStorage.setItem('access_token', data.access_token); // Store token
            showSuccessMessage(); // Show success message before redirecting
        }
    })
    .catch(error => {
        alert('Error: ' + error.message); // Display error message
        console.error('Error:', error);
    });

    // function showSuccessMessage() {
    //     // Display success message
    //     const messageContainer = document.createElement('div');
    //     messageContainer.style.position = 'fixed';
    //     messageContainer.style.top = '20px';
    //     messageContainer.style.right = '20px';
    //     messageContainer.style.padding = '10px';
    //     messageContainer.style.backgroundColor = '#4CAF50';
    //     messageContainer.style.color = 'white';
    //     messageContainer.style.borderRadius = '5px';
    //     messageContainer.innerText = 'Login successful! Redirecting...';

    //     document.body.appendChild(messageContainer);

        // Redirect after a short delay
//         setTimeout(() => {
//             window.location.href = 'index.html'; // Ensure the path is correct
//         }, 2000); // 2 seconds delay
//     }
});
