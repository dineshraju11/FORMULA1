// ✅ Firebase Configuration (replace with your actual project's config)
const firebaseConfig = {
  apiKey: "AIzaSyDLqQ9HFXgE9i6-8b9VXAVGxOScDSJFtpA",  // ✅ API Key (can be public for frontend)
  authDomain: "f1databaseproject-7688d.firebaseapp.com", // ✅ Auth domain from project
  projectId: "f1databaseproject-7688d", // ✅ Correct Project ID
  storageBucket: "f1databaseproject-7688d.appspot.com", // Optional: for storage, but okay to add
  messagingSenderId: "742229075357", // Optional if you use messaging (placeholder for now)
  appId: "1:742229075357:web:e64ae81cab589fd9f4fb74" // Optional if you use apps (placeholder for now)
};

// ✅ Initialize Firebase
firebase.initializeApp(firebaseConfig);

// ✅ Monitor authentication state and dynamically update UI
firebase.auth().onAuthStateChanged(function (user) {
  const userInfoDiv = document.getElementById('user-info');
  const loginBtn = document.getElementById('login-btn');
  const logoutBtn = document.getElementById('logout-btn');

  if (user) {
      userInfoDiv.innerHTML = `Logged in as: ${user.email}`;
      loginBtn.style.display = 'none';  // Hide login button when logged in
      logoutBtn.style.display = 'inline-block'; // Show logout button
  } else {
      userInfoDiv.innerHTML = 'Not logged in';
      loginBtn.style.display = 'inline-block'; // Show login button when logged out
      logoutBtn.style.display = 'none'; // Hide logout button
  }
});

// ✅ Login function (Google)
function login() {
  var provider = new firebase.auth.GoogleAuthProvider();
  firebase.auth().signInWithPopup(provider)
      .then((result) => {
          console.log('Logged in as:', result.user.email);
      }).catch((error) => {
          console.error('Login failed:', error.message);
      });
}

// ✅ Logout function
function logout() {
  firebase.auth().signOut().then(() => {
      console.log('Logged out successfully!');
  }).catch((error) => {
      console.error('Logout failed:', error.message);
  });
}
