/* 
  This is a SAMPLE FILE to get you started.
  (HAHAH NOT FOR LONG)
  
  Please, follow the project instructions to complete the tasks.
*/


/* Login Interaction */
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            await loginUser(email, password);
          });
    }
});

async function loginUser(email, password){
  try{
    const response = await fetch('/api/v1/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    });

    if (response.ok) {
      const data = await response.json();

      document.cookie = `token=${data.access_token}; path=/`;
      window.location.href = 'index.html'
    } else {
      alert('Login failed: ' + response.statusText);
    }
  } catch (error) {
    console.error('Error:', error);
    alert('Something went wrong');
  }
}