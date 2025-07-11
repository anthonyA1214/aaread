from models import db
from sqlalchemy import UniqueConstraint

class Chapter(db.Model):
    __tablename__ = "chapters"

    id = db.Column(db.Integer, primary_key=True)
    novel_id = db.Column(db.Integer, db.ForeignKey("novels.id", ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String(150))
    content = db.Column(db.Text)
    chapter_num = db.Column(db.Integer)
    posted_on = db.Column(db.DateTime)

    # Relationship to novel model
    novel = db.relationship("Novel", back_populates="chapters")

    __table_args__ = (UniqueConstraint('novel_id', 'chapter_num', name='uq_novel_chapter_num'),)


