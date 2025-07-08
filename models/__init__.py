from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from . import association, chapter, genre, novel, user