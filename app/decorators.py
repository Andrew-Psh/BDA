from functools import wraps
from flask import redirect, url_for
from flask_login import current_user


def active_user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.status == 'active':
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))  # Перенаправление на страницу login.html
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.status == 'active' and current_user.is_admin:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('index'))  # Перенаправление на страницу index.html
    return decorated_function