let isLogin = true;

async function initializeFirebase() {
    try {
        // Fetch Firebase config from Flask backend
        const response = await fetch('/config');
        const config = await response.json();
        
        // ✅ Initialize Firebase (Only if not already initialized)
        if (!firebase.apps.length) {
            firebase.initializeApp(config);
        } else {
            firebase.app(); // Ensure the app is used properly
        }

        // ✅ Check if user is already logged in
        firebase.auth().onAuthStateChanged(async (user) => {
            if (user) {
                console.log('User is signed in:', user);
                showMessage(`Welcome ${user.displayName || user.email}!`, 'success');
                const idToken = await user.getIdToken(); // Get Firebase token

                console.log("Firebase ID Token:", idToken);
                await fetch('/set-token', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ idToken })
                });

                // ✅ Redirect to /authenticate after login
                setTimeout(() => {
                    window.location.href = "/authenticate";  
                }, 2000);
                // window.location.href = "/authenticate"; 
                // window.location.href = "/authenticate";
            } else {
                console.log('User is signed out');
            }
        });
    } catch (error) {
        console.error('Error initializing Firebase:', error);
        showMessage('Error initializing authentication', 'error');
    }
}

// ✅ Ensure Firebase is initialized before calling auth functions
document.addEventListener("DOMContentLoaded", initializeFirebase);

async function handleGoogleAuth() {
    try {
        const provider = new firebase.auth.GoogleAuthProvider();
        const result = await firebase.auth().signInWithPopup(provider);
        const user = result.user;

        if (user) {
            const idToken = await user.getIdToken(); // Get Firebase token

            console.log("Firebase ID Token:", idToken);

            // ✅ Send token to Flask backend instead of setting cookies manually
            await fetch('/set-token', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ idToken })
            });

            // ✅ Redirect to authentication route
            window.location.href = '/authenticate';
        }
    } catch (error) {
        console.error('Login error:', error);
        showMessage(error.message, 'error');
    }
}

// ✅ Toggle login/signup UI
function toggleAuthMode() {
    isLogin = !isLogin;
    
    document.getElementById('title').textContent = isLogin ? 'Welcome back' : 'Create account';
    document.getElementById('subtitle').textContent = isLogin 
        ? 'Sign in to your account to continue'
        : 'Sign up for a new account';

    document.getElementById('toggle-question').textContent = isLogin 
        ? "Don't have an account?"
        : 'Already have an account?';

    document.getElementById('toggle-action').textContent = isLogin ? 'Sign up' : 'Sign in';

    document.getElementById('google-btn-text').textContent = isLogin 
        ? 'Sign in with Google'
        : 'Sign up with Google';
}

document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM fully loaded and parsed");
});

// ✅ Show messages to user
function showMessage(message, type) {
    const messageContainer = document.getElementById('message-container');
    
    if (!messageContainer) {
        console.error("Error: message-container element not found!");
        return; // Prevent crash
    }

    messageContainer.textContent = message;
    messageContainer.className = `message ${type}`;
    messageContainer.style.display = 'block';

    // Hide message after 5 seconds
    setTimeout(() => {
        messageContainer.style.display = 'none';
    }, 5000);
}
