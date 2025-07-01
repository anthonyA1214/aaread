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
const signupForm = document.querySelector('#signupForm');

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
            showError('email', 'emailError', 'Email is required.');
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
            showError('email', 'emailError', 'Please enter a valid email address.');
        }

        // Validate username
        if (!username.value.trim()) {
            showError('username', 'usernameError', 'Username is required.');
        } else if (username.value.length < 3 || username.value.length > 20) {
            showError('username', 'usernameError', 'Username must be between 3 and 20 characters.');
        } else if (!/^[a-zA-Z0-9]+$/.test(username.value)) {
            showError('username', 'usernameError', 'Username must be alphanumeric.');
        }

        // Validate password
        if (!password.value.trim()) {
            showError('password', 'passwordError', 'Password is required.');
        } else if (password.value.length < 6 || password.value.length > 20) {
            showError('password', 'passwordError', 'Password must be between 6 and 20 characters.');
        }

        // Validate confirm password
        if (!confirmPassword.value.trim()) {
            showError('confirm_password', 'confirmPasswordError', 'Password confirmation is required.');
        } else if (confirmPassword.value.length < 6 || confirmPassword.value.length > 20) {
            showError('confirm_password', 'confirmPasswordError', 'Password confirmation must be between 6 and 20 characters.');
        } else if (confirmPassword.value !== password.value) {
            showError('confirm_password', 'confirmPasswordError', 'Passwords do not match.');
        }

        // Function to show error messages
        function showError(inputId, errorId, message) {
            const input = document.getElementById(inputId);
            const errorElement = document.getElementById(errorId);
            input.classList.add('is-invalid');
            errorElement.textContent = message;
            isValid = false;
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


