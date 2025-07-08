from models import db
from models.association import novel_genres_table

class Chapter(db.Model):
    __tablename__ = "chapters"

    id = db.Column(db.Integer, primary_key=True)
    novel_id = db.Column(db.Integer, db.ForeignKey("novels.id", ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String(150))
    content = db.Column(db.Text)
    chapter_num = db.Column(db.Integer)
    posted_on = db.Column(db.String(50))

    # Relationship to novel model
    novel = db.relationship("Novel", back_populates="chapters")


