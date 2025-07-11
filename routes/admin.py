import os

from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from helpers import admin_required
from datetime import datetime, timezone
from werkzeug.utils import secure_filename

from models import db
from models.genre import Genre
from models.novel import Novel
from models.chapter import Chapter

# the first argument is the location of the second argument will be saved be it file or folder
UPLOAD_FOLDER = os.path.join("static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "jfif", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

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

@admin_bp.route("/novels",)
@admin_required
def view_novels():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '')

    query = Novel.query
    if search:
        query = query.filter(Novel.title.ilike(f"%{search}%"))

    pagination = query.order_by(Novel.id.asc()).paginate(page=page, per_page=per_page, error_out=False)
    novels = pagination.items

    return render_template("admin/novels/list.html", novels=novels, pagination=pagination)


@admin_bp.route("/novels/add", methods=["GET", "POST"])
@admin_required
def add_novel():
        if request.method == "POST":
            title = request.form.get("title")
            description = request.form.get("description")
            status = request.form.get("status")
            author = request.form.get("author")
            released = request.form.get("released", type=int)
            genres_ids = request.form.getlist("genres")
            posted_by = session.get("user_id")  

            genres_ids = [int(gid) for gid in genres_ids] # converting strings id into integer optional but recommended said by AI
            selected_genres = Genre.query.filter(Genre.id.in_(genres_ids)).all() # on why there is an underscore in 'in' cuz in is a python keyword so sqlalchemy make it 'in_'

            if not title:
                flash("Title is required.", "danger")
                return redirect(request.url)
            
            posted_on = datetime.now(timezone.utc)

            file = request.files.get("cover_image")
            cover_filename = None

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                cover_filename = f"{title.replace(" ", "_")}_{filename}" # every space in the filename will be replaced by underscore
                save_path = os.path.join(UPLOAD_FOLDER, cover_filename)

                # Creates a folder if doesnt exit yet
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)

                file.save(save_path)

            new_novel = Novel(
                title=title,
                description=description,
                status=status,
                author=author,
                released=released,
                posted_by=posted_by,
                posted_on=posted_on,
                cover_image=os.path.join("uploads", cover_filename).replace('\\', '/') if cover_filename else None
            )

            new_novel.genres = selected_genres

            db.session.add(new_novel)
            db.session.commit()

            flash("Novel added successfully!", "success")
            return redirect(url_for("admin.view_novels"))

        else:
            genres = Genre.query.order_by(Genre.name.asc()).all()
            return render_template("admin/novels/add.html", genres=genres)
    

@admin_bp.route("/novels/<int:novel_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_novel(novel_id):
    novel = Novel.query.get_or_404(novel_id)

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        status = request.form.get("status")
        author = request.form.get("author")
        released = request.form.get("released", type=int)

        genres_ids = request.form.getlist("genres")
        selected_genres = Genre.query.filter(Genre.id.in_(genres_ids)).all()

        if not title:
            flash("Title is required.", "danger")
            return redirect(request.url)
        
        file = request.files.get("cover_image")
        if file and allowed_file(file.filename):
            if novel.cover_image:
                old_path = os.path.join('static', novel.cover_image)
                if os.path.exists(old_path):
                    os.remove(old_path)

            
            filename = secure_filename(file.filename)
            cover_filename = f"{title.replace(" ", "_")}_{filename}"
            save_path = os.path.join(UPLOAD_FOLDER, cover_filename)

            # Creates a folder if doesnt exit yet
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            file.save(save_path)

            novel.cover_image = os.path.join("uploads", cover_filename).replace("\\", "/")
        
        novel.title = title
        novel.description = description
        novel.status = status
        novel.author = author
        novel.released = released
        novel.genres = selected_genres

        db.session.commit()

        flash("Novel updated successfully!", "success")
        return redirect(url_for("admin.view_novels"))


    else:
        genres = Genre.query.order_by(Genre.name.asc()).all()

        return render_template("admin/novels/edit.html", novel=novel, genres=genres)

@admin_bp.route("/novels/<int:novel_id>/delete", methods=["POST"])
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
    novel = Novel.query.get_or_404(novel_id)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '')

    query = Chapter.query.filter_by(novel_id=novel.id)

    if search:
        query = query.filter(Chapter.chapter_num.ilike(f"%{search}%"))

    pagination = query.order_by(Chapter.chapter_num.asc()).paginate(page=page, per_page=per_page)
    chapters = pagination.items

    return render_template("admin/chapters/list.html", novel=novel, chapters=chapters, pagination=pagination)


@admin_bp.route("/novels/<int:novel_id>/chapters/add", methods=["GET", "POST"])
@admin_required
def add_chapter(novel_id):
    novel = Novel.query.get_or_404(novel_id)

    if request.method == "POST":
        chapter_num = request.form.get("chapter_num", type=int)
        title = request.form.get("title")
        content = request.form.get("content")
        posted_on = datetime.now(timezone.utc)

        # check for duplicate chapter
        existing_chapter = Chapter.query.filter_by(novel_id=novel.id, chapter_num=chapter_num).first()
        if existing_chapter:
            flash(f"Chapter {chapter_num} already exists for this novel.", "danger")
            return redirect(request.url)
        
        new_chapter = Chapter(
            novel_id = novel.id,
            chapter_num = chapter_num,
            title = title,
            content = content,
            posted_on = posted_on
        )

        # update novel's last updated timestamp
        novel.updated_on = posted_on

        db.session.add(new_chapter)
        db.session.commit()

        flash("Chapter added successfully!", "success")
        return redirect(url_for("admin.view_chapters", novel_id=novel.id))

    else:
        return render_template("admin/chapters/add.html", novel=novel)


@admin_bp.route("/novels/<int:novel_id>/chapters/<int:chapter_num>/edit", methods=["GET", "POST"])
@admin_required
def edit_chapter(novel_id, chapter_num):
    novel = Novel.query.get_or_404(novel_id)

    chapter = Chapter.query.filter_by(novel_id=novel.id, chapter_num=chapter_num).first_or_404()

    if request.method == "POST":
        new_chapter_num = request.form.get("chapter_num", type=int)
        title = request.form.get("title")
        content = request.form.get("content")

        if new_chapter_num != chapter.chapter_num:
            existing_chapter = Chapter.query.filter_by(novel_id=novel.id, chapter_num=new_chapter_num).first()
            if existing_chapter:
                flash(f"Chapter {chapter_num} already exists for this novel.", "danger")
                return redirect(request.url)

            chapter.chapter_num = new_chapter_num
        
        chapter.title = title
        chapter.content = content

        chapter.novel.updated_on = datetime.now(timezone.utc)

        db.session.commit()

        flash(f"Chapter {chapter.chapter_num} updated successfully!", "success")
        return redirect(url_for("admin.view_chapters", novel_id=novel.id))

    else:   
        return render_template("admin/chapters/edit.html", novel=novel, chapter=chapter)


@admin_bp.route("/novels/<int:novel_id>/chapters/<int:chapter_num>/delete", methods=["POST"])
@admin_required
def delete_chapter(novel_id, chapter_id):
    pass


# ----------------------
# Genres
# ----------------------

@admin_bp.route("/genres")
@admin_required
def view_genres():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '')

    query = Genre.query
    if search:
        query = query.filter(Genre.name.ilike(f"%{search}%"))

    pagination = query.order_by(Genre.id.asc()).paginate(page=page, per_page=per_page, error_out=False)
    genres = pagination.items

    return render_template("admin/genres/list.html", genres=genres, pagination=pagination)


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