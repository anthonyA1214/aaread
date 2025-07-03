from functools import wraps
from flask import session, redirect

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