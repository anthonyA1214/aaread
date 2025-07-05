from flask import Blueprint, render_template, request, flash, redirect, url_for
from helpers import admin_required, is_safe_url

from models import db
from models.genre import Genre

# create the admin blueprint
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/")
@admin_required
def index():
    """Admin panel."""
    return render_template("admin/index.html")


# ----------------------
# Novels
# ----------------------

@admin_bp.route("/novels")
@admin_required
def view_novels():
    return render_template("admin/novels/list.html")


@admin_bp.route("/novels/add", methods=["GET", "POST"])
@admin_required
def add_novel():
    if request.method == "POST":
        pass
    else:
        return render_template("admin/novels/add.html")
    

@admin_bp.route("/novels/<int:novel_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_novel(novel_id):
    pass
    

@admin_bp.route("/novels/<int:novel_id>/edit", methods=["POST"])
@admin_required
def delete_novel(novel_id):
    pass


# ----------------------
# Chapters
# ----------------------

@admin_bp.route("/novels/<int:novel_id>/chapters")
@admin_required
def view_chapters(novel_id):
    # list chapters for a specific novel
    pass


@admin_bp.route("/novels/<int:novel_id>/chapters/add", methods=["GET", "POST"])
@admin_required
def add_chapter(novel_id):
    pass


@admin_bp.route("/novels/<int:novel_id>/chapters/edit", methods=["GET", "POST"])
@admin_required
def edit_chapter(novel_id):   
    pass


@admin_bp.route("/novels/<int:novel_id>/chapters/delete", methods=["POST"])
@admin_required
def delete_chapter(novel_id):
    pass


# ----------------------
# Genres
# ----------------------

@admin_bp.route("/genres")
@admin_required
def view_genres():
    genres = Genre.query.all()

    return render_template("admin/genres/list.html", genres=genres)


@admin_bp.route("/genres/add", methods=["POST"])
@admin_required
def add_genre():
    if request.method == "POST":
        addGenreName = request.form.get("addGenreName")
        
        if not addGenreName:
            flash("Genre name is required", "danger")
            return render_template("admin/genres/list.html")

        existing_genre = Genre.query.filter(
            (Genre.name == addGenreName)
        ).first()

        if existing_genre:
            flash("Genre name already exists.", "danger")
            return redirect(url_for("admin.view_genres"))
        
        new_genre = Genre(name=addGenreName)

        db.session.add(new_genre)
        db.session.commit()

        flash("Genre added succesfully!", "success")
        return redirect(url_for("admin.view_genres"))


@admin_bp.route("/genres/<int:genre_id>/edit", methods=["POST"])
@admin_required
def edit_genre(genre_id):
    if request.method == "POST":
        editGenreName = request.form.get("editGenreName")

        if not editGenreName:
            flash("Genre name is required", "danger")
            return render_template("admin/genres/list.html")
        
        existing_genre = Genre.query.filter(
            (Genre.name == editGenreName)
        ).first()

        if existing_genre:
            flash("Genre name already exists.", "danger")
            return render_template("admin/genres/list.html") 
        
        genre = Genre.query.get_or_404(genre_id)
        genre.name = editGenreName

        db.session.commit()

        flash("Genre updated succesfully!", "success")
        return redirect(url_for("admin.view_genres"))


@admin_bp.route("/genres/<int:genre_id>/delete", methods=["POST"])
@admin_required
def delete_genre(genre_id):
    pass