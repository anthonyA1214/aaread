from datetime import datetime, timezone
from models import db
from models.association import novel_genres_table, user_library_table


class Novel(db.Model):
    __tablename__ = "novels"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    cover_image = db.Column(db.String(255))
    status = db.Column(db.String(20))
    author = db.Column(db.String(100))
    released = db.Column(db.Integer)

    posted_by = db.Column(db.Integer, db.ForeignKey("users.id") ,nullable=False)
    user = db.relationship("User")

    posted_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime)

    view_count = db.Column(db.Integer, default=0)


    genres = db.relationship("Genre", secondary=novel_genres_table, back_populates="novels")
    saved_by_users = db.relationship("User", secondary=user_library_table, back_populates="saved_novels")

    chapters = db.relationship("Chapter", back_populates="novel", cascade="all, delete-orphan", order_by="Chapter.chapter_num")



