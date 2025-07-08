from models import db

novel_genres_table = db.Table(
    "novel_genres",
    db.Column("novel_id", db.Integer, db.ForeignKey("novels.id", ondelete="CASCADE", name="fk_novel_genres_novel_id"), primary_key=True),
    db.Column("genre_id", db.Integer, db.ForeignKey("genres.id", ondelete="CASCADE", name="fk_novel_genres_genre_id"), primary_key=True)
)

user_library_table = db.Table(
    "user_library",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id", ondelete="CASCADE", name="fk_user_library_user_id"), primary_key=True),
    db.Column("novel_id", db.Integer, db.ForeignKey("novels.id", ondelete="CASCADE", name="fk_user_library_novel_id"), primary_key=True)
)