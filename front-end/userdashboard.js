// // document.getElementById('get-details-btn').addEventListener('click', async () => {
//     try {
//         // Assuming the email is fetched or stored after admin login
//         const email = 'mythili@gmail.com'; // Replace with the actual email
 
//         c
//         if (!response.ok) {
//             throw new Error('Failed to fetch user data');
//         }
 
//         const data = await response.json();
//         const users = data.users;
 
//         const tableBody = document.getElementById('user-table-body');
//         tableBody.innerHTML = '';
 
//         users.forEach(user => {
           
//             tableBody.appendChild(row);
//         });
//     } catch (error) {
//         console.error('Error:', error);
//         alert('An error occurred while fetching user data.');
//     }
// });
 
function create_row(user,parent) {
    console.log(user.first_name)
    const child = document.createElement('tr');
    child.innerHTML = `
        <td>${user.id}</td>
        <td>${user.first_name}</td>
        <td>${user.last_name}</td>
        <td>${user.email}</td>
    `;
    parent.appendChild(child);
}
 
 
async function getUsers() {
    const response = await fetch(`http://127.0.0.1:5000/users`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    let users = await response.json();
   let table1 = document.getElementById('user-table')
   users.forEach(user => {
       create_row(user,table1)
   });
    console.log(users);
    if (!response.ok) {
 
    }
 
}
getUsers()
 