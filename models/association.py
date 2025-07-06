from models import db

novel_genres_table = db.Table(
    "novel_genres",
    db.Column("novel_id", db.Integer, db.ForeignKey("novels.id"), primary_key=True),
    db.Column("genre_id", db.Integer, db.ForeignKey("genres.id"), primary_key=True)
)

user_library_table = db.Table(
    "user_library",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("novels_id", db.Integer, db.ForeignKey("novels.id"), primary_key=True)
)