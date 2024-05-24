from app import app, db
from flask import render_template
from app.decorators import admin_required, active_user_required


@app.route('/')
@app.route('/index')
@active_user_required
def index():
    return render_template(
        'common/index.html', 
        title = 'BDA'
    )

@app.route('/admin_panel')
@admin_required
def admin_panel():
    return render_template(
        'admin/admin_panel.html', 
        title = 'BDA'
    )