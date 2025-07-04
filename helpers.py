import sqlite3
from functools import wraps
from flask import session, redirect, request, g
from urllib.parse import urlparse, urljoin

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            return redirect('/login')
        return f(*args, **kwargs)    
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):      
        if session.get("user_role") != "admin":
            return redirect("/")
        return f(*args, **kwargs)    
    return decorated_function


def get_db():
    """Connect to the SQLite database."""
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect("app.db")
        db.row_factory = sqlite3.Row
    return db


def is_safe_url(target):
    """Check if the target URL is safe for redirection."""
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return (
        test_url.scheme in ("http", "https") and
        ref_url.netloc == test_url.netloc
    )