let isLogin = true;

async function initializeFirebase() {
    try {
        // Fetch Firebase config from Flask backend
        const response = await fetch('/config');
        console.log('response:', response);
        const config = await response.json();
        
        // ✅ Initialize Firebase (Only if not already initialized)
        if (!firebase.apps.length) {
            firebase.initializeApp(config);
        }

        // ✅ Check if user is already logged in
        firebase.auth().onAuthStateChanged((user) => {
            if (user) {
                console.log('User is signed in:', user);
                showMessage(`Welcome ${user.displayName || user.email}!`, 'success');
                
                // ✅ Redirect to /authenticate after login
                setTimeout(() => {
                    window.location.href = "/authenticate";  
                }, 2000);
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

        // ✅ Trigger Google Sign-In Popup
        const result = await firebase.auth().signInWithPopup(provider);

        if (result.user) {
            console.log('Login successful:', result.user);
            showMessage(`Welcome ${result.user.displayName || result.user.email}!`, 'success');

            // ✅ Get Firebase ID token & send to Flask backend
            const idToken = await result.user.getIdToken();
            await fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `idToken=${idToken}`
            });

            // ✅ Redirect to /authenticate
            setTimeout(() => {
                window.location.href = "/authenticate";
            }, 2000);
        }
    } catch (error) {
        console.error('Error during Google sign-in:', error);

        if (error.code === 'auth/unauthorized-domain') {
            showMessage('Please add this domain in Firebase Console -> Auth -> Sign-in methods -> Authorized domains', 'error');
        } else {
            showMessage(error.message, 'error');
        }
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

// ✅ Show messages to user
function showMessage(message, type) {
    const messageContainer = document.getElementById('message-container');
    messageContainer.textContent = message;
    messageContainer.className = `message ${type}`;
    messageContainer.style.display = 'block';
    
    // Hide message after 5 seconds
    setTimeout(() => {
        messageContainer.style.display = 'none';
    }, 5000);
}
