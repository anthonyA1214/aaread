import os

from flask import Flask, render_template, redirect, request, session, g, flash, get_flashed_messages
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError
from urllib.parse import urlparse

from routes.admin import admin_bp
from helpers import login_required, get_db, is_safe_url

# Configure the Flask application
app = Flask(__name__)
app.register_blueprint(admin_bp)

PUBLIC_PATHS = ["/", "/novels"]

# set a secret key for session management
app.secret_key = os.urandom(24)

# Configure Flask-Session
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
Session(app)


@app.before_request
def load_user():
    """Load the user from the session before each request."""
    g.user = session.get("user_id") is not None


# injects the user information to all templates
@app.context_processor
def inject_user():
    """Inject the user information into the template context."""
    return dict(is_loggedin=session.get("user_id") is not None, is_admin=session.get("user_role") == "admin", username=session.get("username"))


# This function renders a custom 404 error page when a user tries to access a route that doesn't exist
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/")
def index():
    """Render the index page."""
    return render_template("public/index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""
    if request.method == "POST":
        usernameEmail = request.form["usernameEmail"]
        password = request.form["password"]

        if not usernameEmail or not password:
            flash("Username (or email) and password are required.", "danger")
            return render_template("public/login.html")

        db = get_db()
        cursor = db.cursor()
        user = cursor.execute(
            "SELECT * FROM users WHERE username = ? OR email = ?", (usernameEmail, usernameEmail)
        ).fetchone()
        db.close()

        if user is None or not check_password_hash(user["hashed_password"], password):
            flash("Invalid username (or email) or password.", "danger")
            return render_template("public/login.html")

        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["user_role"] = user["role"]
        flash("Login successful!", "success")
        return redirect("/")

    else:
        messages = get_flashed_messages(with_categories=True)
        if messages:
            for category, message in messages:
                flash(message, category)

        if "user_id" in session:
            flash("You are already logged in.", "info")
            return redirect("/")

        session.clear()
        return render_template("public/login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Handle user signup."""

    if "user_id" in session:
        flash("You are already logged in.", "info")
        return redirect("/")

    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

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
            for err in errors:
                flash(err, "danger")
            return render_template("public/signup.html")

        try:
            valid_email = validate_email(email, check_deliverability=True)
            email = valid_email.normalized
        except EmailNotValidError as e:
            flash(f"Invalid email: {e}", "danger")
            return render_template("public/signup.html")

        if len(username) < 3 or len(username) > 20:
            flash("Username must be between 3 and 20 characters.", "danger")
            return render_template("public/signup.html")

        if not username.isalnum():
            flash("Username must be alphanumeric.", "danger")
            return render_template("public/signup.html")

        if len(password) < 6 or len(password) > 20:
            flash("Password must be between 6 and 20 characters.", "danger")
            return render_template("public/signup.html")

        if len(confirm_password) < 6:
            flash("Password confirmation must be at least 6 characters long.", "danger")
            return render_template("public/signup.html")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("public/signup.html")

        db = get_db()
        cursor = db.cursor()
        existing_user = cursor.execute(
            "SELECT * FROM users WHERE username = ? OR email = ?", (username, email)
        ).fetchone()

        if existing_user:
            flash("Username or email already exists.", "danger")
            return render_template("public/signup.html")

        hashed_password = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (email, username, hashed_password) VALUES (?, ?, ?)",
            (email, username, hashed_password)
        )
        db.commit()
        db.close()

        flash("Signup successful! Please log in.", "success")
        return redirect("/login")
    else:
        return render_template("public/signup.html")


@app.route("/logout")
@login_required
def logout():
    """Handle user logout."""
    next_page = request.args.get("next") or "/"

    session.clear()
    flash("You have been logged out.", "info")

    if not is_safe_url(next_page):
        return redirect("/")

    parsed_next = urlparse(next_page).path
    if parsed_next not in PUBLIC_PATHS:
        return redirect("/")

    return redirect(next_page)


@app.route("/novels", methods=["GET", "POST"])
def novels():
    """Display a list of novels."""
    if request.method == "POST":
        pass
    else:
        return render_template("public/novels.html")


@app.route("/library")
@login_required
def library():
    """Display the user's library."""
    return render_template("public/library.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
