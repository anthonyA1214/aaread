import os

from flask import Flask, render_template, redirect, request, session, g, flash, get_flashed_messages
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError
import sqlite3

from auth import login_required, admin_required

# Configure the Flask application
app = Flask(__name__)

# set a secret key for session management
app.secret_key = os.urandom(24)

# Configure Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

def get_db():
    """Connect to the SQLite database."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('app.db')
        db.row_factory = sqlite3.Row
    return db


@app.before_request
def load_user():
    """Load the user from the session before each request."""
    g.user = session.get('user_id') is not None


@app.context_processor
def inject_user():
    """Inject the user information into the template context."""
    return dict(is_loggedin=session.get('user_id') is not None, is_admin=session.get('user_role') == 'admin')


@app.route('/')
def index():
    """Render the index page."""
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""

    messages = get_flashed_messages(with_categories=True)
    session.clear()  # Clear the session to ensure no previous session data is present
    if messages:
        for category, message in messages:
            flash(message, category)
    # If the user is already logged in, redirect to the novels page
    if 'user_id' in session:
        flash("You are already logged in.", "info")
        return redirect('/')
    
    # If the request method is POST, handle the login logic
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash("Username and password are required.", "danger")
            return render_template('login.html')
        
        # Connect to the database
        db = get_db()
        cursor = db.cursor()
        user = cursor.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        db.close()

        # Check if the user exists and if the password matches
        if user is None or not check_password_hash(user['hashed_password'], password):
            flash("Invalid username or password.", "danger")
            return render_template('login.html')
        
        # Store user information in the session
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['user_role'] = user['role']
        flash("Login successful!", "success")
        # Redirect to the novels page after successful login
        return redirect('/')
        
    # If the request method is GET, render the login page        
    else:
        return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user signup."""
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        errors = []

        if not email:
            errors.append("Email is required.")
        if not username:
            errors.append("Username is required.")
        if not password:
            errors.append("Password is required.")
        if not confirm_password:
            errors.append("Password confirmation is required.")           
        if errors:
            # If there are validation errors, flash them and render the signup page again
            for err in errors:
                flash(err, "danger")
            return render_template('signup.html')

        try:
            # Validate the email address
            valid_email = validate_email(email, check_deliverability=True)
            email = valid_email.normalized  # Get the normalized email address
        except EmailNotValidError as e:
            flash(f"Invalid email: {e}", "danger")
            return render_template('signup.html')

        if len(username) < 3 and len(username) > 20:
            flash("Username must be between 3 and 20 characters.", "danger")
            return render_template('signup.html')
        
        if not username.isalnum():
            flash("Username must be alphanumeric.", "danger")
            return render_template('signup.html')
        
        if len(password) < 6 and len(password) > 20:
            flash("Password must be between 6 and 20 characters.", "danger")
            return render_template('signup.html')
        
        if len(confirm_password) < 6:
            flash("Password confirmation must be at least 6 characters long.", "danger")
            return render_template('signup.html')
                
        # Check if the username already exists (this is a placeholder, replace with actual database check)
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template('signup.html')
        
        # Connect to the database and check if the username or email already exists
        db = get_db()
        cursor = db.cursor()
        existing_user = cursor.execute(
            "SELECT * FROM users WHERE username = ? OR email = ?", (username, email)
        ).fetchone()

        if existing_user:
            flash("Username or email already exists.", "danger")
            return render_template('signup.html')

        # Here you would typically save the user to a database
        # Save the user with email, username, and hashed_password to the database
        hashed_password = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (email, username, hashed_password) VALUES (?, ?, ?)",
            (email, username, hashed_password)
        )
        db.commit()
        db.close()
        
        # Redirect to the login page after successful signup
        flash("Signup successful! Please log in.", "success")
        return redirect('/login')
    else:
        return render_template('signup.html')
    
@app.route('/logout')
@login_required
def logout():
    """Handle user logout."""

    session.clear()  # Clear the session   

    flash("You have been logged out.", "info")
    return redirect('/')
    

@app.route('/novels', methods=['GET', 'POST'])
def novels():
    """Display a list of novels."""
    if request.method == 'POST':
        # Here you would typically handle novel creation or search
        pass
    else:
        # For now, just render the novels page
        # In a real application, you would pass the list of novels to the template
        return render_template('novels.html')

@app.route('/library')
@login_required
def library():
    """Display the user's library."""
    # Here you would typically fetch the user's library from a database
    return render_template('library.html')


@app.route('/upload', methods=['GET', 'POST'])
@login_required
@admin_required
def upload():
    """Handle file uploads."""
    if request.method == 'POST':
        file = request.files['file']
        # Here you would typically save the file to a server or cloud storage
        return redirect('/library')
    else:
        return render_template('upload.html')
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)