# app/routes/user_functions.py

from app import app, db
from flask import render_template, flash, redirect, url_for, session
from app.forms import LoginForm, UserRegistrationForm, ChangePassword
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    return render_template(
        'common/profile.html', 
        title = 'BDA'
    )

@app.route('/password_error', methods=['GET', 'POST'])
def password_error():
    messages = session.get('messages')
    return render_template('common/password_error.html', title='BDA', messages=messages)


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePassword()
    if form.validate_on_submit():
        if check_password_hash(current_user.password_hash, form.old_password.data):  # Проверка старого пароля
            user_to_update = User.query.get(current_user.id)  # Получение объекта User по id текущего пользователя
            print("in change_password, текущий пользователь,",  user_to_update)
            if user_to_update:
                if form.password.data == user_to_update.username:
                    messages = ['ERROR! Пароль не был изменен!!!', 'Пароль не должен совпадать с логином.']
                    return render_template('common/password_error.html', title='BDA', messages=messages)
                elif form.old_password.data == form.password.data:
                    messages = ['ERROR! Пароль не был изменен!!!', 'Пароль не должен совпадать со старым паролем.']
                    return render_template('common/password_error.html', title='BDA', messages=messages)
                elif form.password.data != form.password2.data:
                    messages = ['ERROR! Пароль не был изменен!!!', 'Пароли не совпадают']
                    return render_template('common/password_error.html', title='BDA', messages=messages)                   
                else:
                    print('form.password.data != user_to_update.username')
                    user_to_update.password_hash = generate_password_hash(form.password.data)  # Обновление хэша пароля
                    db.session.commit()  # Сохранение изменений в базе данных
                    flash('Пароль успешно изменен.', 'success')
                    # Перенаправление пользователя на страницу профиля после успешного изменения пароля
                    return redirect(url_for('profile'))
            else:
                messages = ['ERROR!', 'Пользователь не найден.']
        else:
            messages = ['ERROR! Неверный старый пароль!!!', 'Попробуйте еще раз.']
    return render_template('forms/change_password.html', title='BDA', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user is None:
            session['message'] = 'Не верный логин или пароль'
            return redirect(url_for('login'))
        
        if user.status == 'archive':
            session['message'] = f'Пользователь {user.username} в архиве'
            return redirect(url_for('login'))
                
        if not user.check_password(form.password.data):
            session['message'] = 'Не верный логин или пароль'
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        if check_password_hash(user.password_hash, form.username.data):
            session['messages'] = ['Для дальнейшего продолжения работы', 'смените разовый пароль']       
            return redirect(url_for('password_error'))
        if user.is_admin:
            return redirect(url_for('admin_panel'))
        return redirect(url_for('index'))
    # else:
    #     session['message'] = 'Заполните правильно форму'
    return render_template('forms/login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated and not current_user.is_admin:
        return redirect(url_for('index'))
    elif current_user.is_anonymous:    
        is_not_admin_exists = True if User.query.filter_by(is_admin=True, status='active').count() == 0 else False
        permission_for_change_the_is_admin = is_not_admin_exists
    elif current_user.is_admin and current_user.status == 'active':
        permission_for_change_the_is_admin = True
    else:
        permission_for_change_the_is_admin = False
    form = UserRegistrationForm()
    
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, is_admin=form.is_admin.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        if current_user.is_anonymous:       
            return redirect(url_for('login'))
        else:
            return redirect(url_for('admin_panel'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in field "{field}": {error}', 'error')

    return render_template(
        'forms/user_registration.html', 
        permission_for_change_the_is_admin=permission_for_change_the_is_admin, 
        form=form
        )


