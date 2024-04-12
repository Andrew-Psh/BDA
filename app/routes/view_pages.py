from app import app, db
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, UserRegistrationForm, ChangePassword
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash
from app.models import User
# from werkzeug.urls import url_parse




@app.route('/')
@app.route('/index')
@login_required
def index():

    return render_template(
        'common/index.html', 
        title = 'BDA'
    )

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# @login.user_loader
# def load_user(id):
#     return db.session.get(User, int(id))




@app.route('/profile')
@login_required
def profile():

    return render_template(
        'common/profile.html', 
        title = 'BDA'
    )



@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePassword()
    if form.validate_on_submit():
        if 0 == 0:
        # if form.validate_old_password(form.old_password):  # Проверка старого пароля
            current_user.password_hash = generate_password_hash(form.password.data)  # Обновление хэша пароля
            db.session.commit()  # Сохранение изменений в базе данных
            flash('Пароль успешно изменен.', 'success')
            return redirect(url_for('profile'))  # Перенаправление пользователя на страницу профиля после успешного изменения пароля
        else:
            flash('Неверный старый пароль. Попробуйте еще раз.', 'error')
    return render_template('forms/change_password.html', title='BDA', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    flash('form.password.data:', form.password.data)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user is None:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        if not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
            
        print('load user: {}'.format(user.username))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    else:
        flash('Форма не валидна')
    return render_template('forms/login.html', title='Sign In', form=form)


@app.route('/register',  methods=['GET', 'POST'])
def register(): 
    print('запущена функкция registration()')
    if current_user.is_authenticated:
        print('if current_user.is_authenticated: True')
        return redirect(url_for('index'))
    form = UserRegistrationForm()
    print('form:', form)
    if form.validate_on_submit():
        print(f'Форма  валидна')
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('"Поздравляем, теперь вы зарегистрированный пользователь!"!')
        return redirect(url_for('login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in field "{field}": {error}', 'error')
        return render_template('forms/user_registration.html', form=form)

