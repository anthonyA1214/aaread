import os

from flask import Flask, render_template, redirect, request, session, g, flash, get_flashed_messages, jsonify, url_for
from flask_session import Session
from flask_migrate import Migrate
from flask_moment import Moment
from email_validator import validate_email, EmailNotValidError
from urllib.parse import urlparse

from routes.admin import admin_bp
from helpers import login_required, is_safe_url

from models import db
from models.user import User
from models.novel import Novel
from models.chapter import Chapter

from dotenv import load_dotenv
import cloudinary

# to load .env file
load_dotenv()

# Cloudinary Configuration       
cloudinary.config( 
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key = os.getenv("CLOUDINARY_API_KEY"),
    api_secret = os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

# Configure the Flask application
app = Flask(__name__)
moment = Moment(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(admin_bp)

PUBLIC_PATHS = ["/", "/novels"]

# set a secret key for session management
app.secret_key = os.urandom(24)

# Configure Flask-Session
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
Session(app)

# You may need to create tables on startup to avoid errors
with app.app_context():
    db.create_all()

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
    popular_novels = Novel.query.order_by(Novel.view_count.desc()).limit(4).all()
    latest_novels = Novel.query.order_by(Novel.updated_on.desc()).limit(10).all()
    
    for novel in latest_novels:
        novel.latest_chapters = (
            Chapter.query.filter_by(novel_id=novel.id)
            .order_by(Chapter.chapter_num.desc()).limit(3).all()
        )

    return render_template("public/index.html", popular_novels=popular_novels, latest_novels=latest_novels)


# ----------------------
# Auth
# ----------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""
    if request.method == "POST":
        username_email = request.form["username_email"]
        password = request.form["password"]

        if not username_email or not password:
            flash("Username (or email) and password are required.", "danger")
            return render_template("public/auth/login.html")

        user = User.query.filter(
            (User.username == username_email) | (User.email == username_email)
        ).first()

        if user is None or not user.check_password(password):
            flash("Invalid username (or email) or password.", "danger")
            return render_template("public/auth/login.html")

        session["user_id"] = user.id
        session["username"] = user.username
        session["user_role"] = user.role
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
        return render_template("public/auth/login.html")


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
            return render_template("public/auth/signup.html")

        try:
            valid_email = validate_email(email, check_deliverability=True)
            email = valid_email.normalized
        except EmailNotValidError as e:
            flash(f"Invalid email: {e}", "danger")
            return render_template("public/authsignup.html")

        if len(username) < 3 or len(username) > 20:
            flash("Username must be between 3 and 20 characters.", "danger")
            return render_template("public/auth/signup.html")

        if not username.isalnum():
            flash("Username must be alphanumeric.", "danger")
            return render_template("public/auth/signup.html")

        if len(password) < 6 or len(password) > 20:
            flash("Password must be between 6 and 20 characters.", "danger")
            return render_template("public/auth/signup.html")

        if len(confirm_password) < 6:
            flash("Password confirmation must be at least 6 characters long.", "danger")
            return render_template("public/auth/signup.html")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("public/auth/signup.html")

        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            flash("Username or email already exists.", "danger")
            return render_template("public/auth/signup.html")

        new_user = User(
            email=email,
            username=username
        )

        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash("Signup successful! Please log in.", "success")
        return redirect("/login")
    else:
        return render_template("public/auth/signup.html")


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


# ----------------------
# Novels
# ----------------------

@app.route("/novels", methods=["GET", "POST"])
def novels():
    """Display a list of novels."""
    if request.method == "POST":
        pass
    else:
        novels = Novel.query.all()

        user_id = session.get("user_id")
        user = User.query.get(user_id) if user_id else None

        return render_template("public/novels.html", novels=novels, user=user)


@app.route("/novels/<int:novel_id>")
def view_novel(novel_id):
    novel = Novel.query.get_or_404(novel_id)

    chapters = novel.chapters

    first_chapter = chapters[0] if chapters else None
    last_chapter = chapters[-1] if chapters else None

    user_id = session.get("user_id")
    user = User.query.get(user_id) if user_id else None
    in_library = False

    if user:
        in_library = novel in user.saved_novels

    return render_template("public/view_novel.html", novel=novel, first_chapter=first_chapter, last_chapter=last_chapter, in_library=in_library)


@app.route("/novels/<int:novel_id>/chapters/<int:chapter_num>")
def read_chapter(novel_id, chapter_num):
    
    novel = Novel.query.get_or_404(novel_id)
    chapter = Chapter.query.filter_by(novel_id=novel_id, chapter_num=chapter_num).first_or_404()

    prev_chapter = (
        Chapter.query
        .filter(Chapter.novel_id == novel_id, Chapter.chapter_num < chapter_num)
        .order_by(Chapter.chapter_num.desc())
        .first()
    )

    next_chapter = (
        Chapter.query
        .filter(Chapter.novel_id == novel_id, Chapter.chapter_num > chapter_num)
        .order_by(Chapter.chapter_num.asc())
        .first()
    )

    if novel.cover_image:
        cover_url = novel.cover_image
    else:
        cover_url = "https://res.cloudinary.com/dha8kpdrp/image/upload/v1752913413/placeholder-image_elvsaz.jpg"

    return render_template("public/read_chapter.html", 
                           novel=novel, 
                           chapter=chapter, 
                           chapter_num=chapter_num, 
                           prev_chapter=prev_chapter, 
                           next_chapter=next_chapter,
                           cover_url=cover_url)


@app.route("/library")
@login_required
def library():
    """Display the user's library."""
    user_id = session.get("user_id")

    user = User.query.get(user_id) if user_id else None

    saved_novels = user.saved_novels

    return render_template("public/library.html", novels=saved_novels)


@app.route("/add-to-library", methods=["POST"])
def add_to_library():
    if request.method == "POST":

        if 'user_id' not in session:
            return jsonify(success=False, message="You must be logged in."), 401
        
        data = request.get_json()
        novel_id = data.get('novel_id')

        if not novel_id:
            return jsonify(success=False, message="Missing novel ID."), 400
        
        user = User.query.get(session["user_id"])
        novel = Novel.query.get(novel_id)

        if not novel:
            return jsonify(success=False, message="Novel not found."), 404
        
        if novel in user.saved_novels:
            return jsonify(success=True, message="Already in library.")
        
        user.saved_novels.append(novel)
        db.session.commit()

        return jsonify(success=True, message="Novel added to library.")


@app.route("/remove-from-library", methods=["POST"])
def remove_from_library():
    if request.method == "POST":

        if "user_id" not in session:
            return jsonify(success=False, message="You must be logged in."), 401
        
        data = request.get_json()
        novel_id = data.get("novel_id")

        if not novel_id:
            return jsonify(success=False, message="Missing novel ID."), 400
        
        user = User.query.get(session["user_id"])
        novel = Novel.query.get(novel_id)

        if not novel:
            return jsonify(success=False, message="Novel not found."), 404
        
        user.saved_novels.remove(novel)
        db.session.commit()

        return jsonify(success=True, message="Novel removed from library.")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


