// Add event listeners to the show/hide password buttons
showPassword = document.getElementById("showPassword");
showPasswordConfirmation = document.getElementById("showPasswordConfirmation");

// Ensure showPassword exists before adding the event listener
if (showPassword) {
    showPassword.addEventListener("click", () => {
        const passwordField = document.getElementById('password');
        if (passwordField.type === "password") {
            passwordField.type = "text";
            showPassword.innerHTML = '<i class="bi bi-eye-slash"></i>';
        } else {
            passwordField.type = "password";
            showPassword.innerHTML = '<i class="bi bi-eye"></i>';
        }
    });
}

// Ensure showPasswordConfirmation exists before adding the event listener
if (showPasswordConfirmation) {
    showPasswordConfirmation.addEventListener("click", () => {
        const passwordConfirmationField = document.getElementById('confirm_password');
        if (passwordConfirmationField.type === "password") {
            passwordConfirmationField.type = "text";
            showPasswordConfirmation.innerHTML = '<i class="bi bi-eye-slash"></i>';
        } else {
            passwordConfirmationField.type = "password";
            showPasswordConfirmation.innerHTML = '<i class="bi bi-eye"></i>';
        }
    });    
}

// input validation for the signup page
const signupForm = document.getElementById('signupForm');

// Function to show error messages
function showError(inputId, errorId, message) {
    const input = document.getElementById(inputId);
    const errorElement = document.getElementById(errorId);
    input.classList.add('is-invalid');
    errorElement.textContent = message;

    return false; // Indicate that the form is not valid
}

// Function to clear validation messages
function clearValidation(inputId, errorId) {
    const input = document.getElementById(inputId);
    if (input) {
        input.classList.remove('is-invalid');
    }
    const errorElement = document.getElementById(errorId);
    if (errorElement) {
        errorElement.textContent = '';
    }
}

if (signupForm) {
    signupForm.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevent the form from submitting immediately

        const email = document.getElementById('email');
        const username = document.getElementById('username');
        const password = document.getElementById('password');
        const confirmPassword = document.getElementById('confirm_password');

        let isValid = true;

        // Clear previous error messages
        clearValidation('email', 'emailError');
        clearValidation('username', 'usernameError');
        clearValidation('password', 'passwordError');
        clearValidation('confirm_password', 'confirmPasswordError');

        // Validate email
        if (!email.value.trim()) {
            isValid = showError('email', 'emailError', 'Email is required.');
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
            isValid = showError('email', 'emailError', 'Please enter a valid email address.');
        }

        // Validate username
        if (!username.value.trim()) {
            isValid = showError('username', 'usernameError', 'Username is required.');
        } else if (username.value.length < 3 || username.value.length > 20) {
            isValid = showError('username', 'usernameError', 'Username must be between 3 and 20 characters.');
        } else if (!/^[a-zA-Z0-9]+$/.test(username.value)) {
            isValid = showError('username', 'usernameError', 'Username must be alphanumeric.');
        }

        // Validate password
        if (!password.value.trim()) {
            isValid = showError('password', 'passwordError', 'Password is required.');
        } else if (password.value.length < 6 || password.value.length > 20) {
            isValid = showError('password', 'passwordError', 'Password must be between 6 and 20 characters.');
        }

        // Validate confirm password
        if (!confirmPassword.value.trim()) {
            isValid = showError('confirm_password', 'confirmPasswordError', 'Password confirmation is required.');
        } else if (confirmPassword.value.length < 6 || confirmPassword.value.length > 20) {
            isValid = showError('confirm_password', 'confirmPasswordError', 'Password confirmation must be between 6 and 20 characters.');
        } else if (confirmPassword.value !== password.value) {
            isValid = showError('confirm_password', 'confirmPasswordError', 'Passwords do not match.');
        }

        // If all validations pass, submit the form
        if (isValid) {
            signupForm.submit();
        }

        // Clear validation messages on input
        [ 
            {id: 'email', errorId: 'emailError'},
            {id: 'username', errorId: 'usernameError'},
            {id: 'password', errorId: 'passwordError'},
            {id: 'confirm_password', errorId: 'confirmPasswordError'}
        ].forEach(({id, errorId}) => {
            const input = document.getElementById(id);
            input.addEventListener('input', () => {
                clearValidation(id, errorId);
            })
        });
    });
}

// input validation for the login page
const loginForm = document.getElementById('loginForm');

if (loginForm) {
    loginForm.addEventListener('submit', (event) => {
        
        event.preventDefault(); // Prevent the form from submitting immediately
        
        const username_email = document.getElementById('username_email');
        const password = document.getElementById('password');

        let isValid = true;

        // Clear previous error messages
        clearValidation('username_email', 'username_emailError');
        clearValidation('password', 'passwordError');

        // Validate username/email
        if (!username_email.value.trim()) {
            isValid = showError('username_email', 'username_emailError', 'Username or email is required.');
        } else if (username_email.value.length < 3) {
            isValid = showError('username_email', 'username_emailError', 'Username or email must be at least 3 characters long.');
        } else if (!/^[a-zA-Z0-9@.]+$/.test(username_email.value)) {
            isValid = showError('username_email', 'username_emailError', 'Username or email must be alphanumeric or contain @ and .');
        } 

        // Validate password
        if (!password.value.trim()) {
            isValid = showError('password', 'passwordError', 'Password is required.');
        } else if (password.value.length < 6 || password.value.length > 20) {
            isValid = showError('password', 'passwordError', 'Password must be between 6 and 20 characters.');
        } 

        // If all validations pass, submit the form
        if (isValid) {
            loginForm.submit();
        }

        // Clear validation messages on input
        [ 
            {id: 'username_email', errorId: 'username_emailError'},
            {id: 'password', errorId: 'passwordError'}
        ].forEach(({id, errorId}) => {
            const input = document.getElementById(id);
            input.addEventListener('input', () => {
                clearValidation(id, errorId);
            })
        });
    });
}
