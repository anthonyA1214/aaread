from flask import Blueprint, render_template, request
from helpers import admin_required

# create the admin blueprint
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route('/')
@admin_required
def index():
    """Admin panel."""
    return render_template('admin/index.html')


# ----------------------
# Novels
# ----------------------
@admin_bp.route('/novels')
@admin_required
def view_novels():
    return render_template('admin/novels/list.html')


@admin_bp.route('/novels/add', methods=['GET', 'POST'])
@admin_required
def add_novel():
    if request.method == 'POST':
        pass
    
    else:
        return render_template('admin/novels/add.html')
    

@admin_bp.route('/novels/edit', methods=['GET', 'POST'])
@admin_required
def edit_novel():
    if request.method == 'POST':
        pass

    else:
        return render_template('admin/novels/edit.html')
    

