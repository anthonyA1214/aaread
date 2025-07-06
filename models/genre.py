from models import db
from models.association import novel_genres_table

class Genre(db.Model):
    __tablename__ = "genres"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    novels = db.relationship("Novel", secondary=novel_genres_table, back_populates="genres")

