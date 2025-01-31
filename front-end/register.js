   document.addEventListener('DOMContentLoaded', () => {
            const form = document.getElementById('registerForm');
            const messageDiv = document.getElementById('message');

            form.addEventListener('submit', async (event) => {
                event.preventDefault();  // Prevent the form from submitting the default way

                // Gather form data manually
                const username = document.getElementById('username').value;
                const email = document.getElementById('email').value;
                const first_name = document.getElementById('first_name').value;
                const last_name = document.getElementById('last_name').value;
                const password = document.getElementById('password').value;

                const data = {
                    username,
                    email,
                    first_name,
                    last_name,
                    password
                };

                try {
                    // Send data to Flask backend
                    const response = await fetch('http://127.0.0.1:5000/usersignup', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(data),
                    });

                    const result = await response.json();

                    // Handle response
                    if (response.ok) {
                        messageDiv.innerHTML = `<p>${result.message}</p>`;
                        form.reset();  // Reset the form on successful submission
                        // Redirect to login page
                        window.location.href = './login.html'; // Adjust URL to your actual login page
                    } else {
                        messageDiv.innerHTML = `<p style="color: red;">${result.message}</p>`;
                    }
                } catch (error) {
                    console.error('Error:', error);
                    messageDiv.innerHTML = `<p style="color: red;">An error occurred. Please try again.</p>`;
                }
            });
        });

        function validateForm(username, email, password) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            if (username.length < 3 || username.length > 20) {
                alert('Username must be between 3 and 20 characters.');
                return false;
            }

            if (!emailRegex.test(email)) {
                alert('Please enter a valid email address.');
                return false;
            }

            if (password.length < 6) {
                alert('Password must be at least 6 characters long.');
                return false;
            }

            return true;
        }