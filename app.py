from flask import Flask, render_template, redirect, request, session
from werkzeug.security import generate_password_hash, check_password_hash

from auth import login_required, admin_required

# Configure the Flask application
app = Flask(__name__)


@app.route('/')
def index():
    """Render the index page."""
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Here you would typically check the username and password against a database
    else:
        return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user signup."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Here you would typically save the user to a database
        session['user_id'] = username
    else:
        return render_template('signup.html')
    
@app.route('/logout')
@login_required
def logout():
    """Handle user logout."""
    session.pop('user_id', None)
    return redirect('/')
    

@app.route('/novels', methods=['GET', 'POST'])
def novels():
    """Display a list of novels."""
    if request.method == 'POST':
        # Here you would typically handle novel creation or search
        pass
    else:
        # For now, just render the novels page
        # In a real application, you would pass the list of novels to the template
        return render_template('novels.html')

@app.route('/library')
@login_required
def library():
    """Display the user's library."""
    # Here you would typically fetch the user's library from a database
    return render_template('library.html')


@app.route('/upload', methods=['GET', 'POST'])
@login_required
@admin_required
def upload():
    """Handle file uploads."""
    if request.method == 'POST':
        file = request.files['file']
        # Here you would typically save the file to a server or cloud storage
        return redirect('/library')
    else:
        return render_template('upload.html')
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)