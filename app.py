from flask import Flask, flash, redirect, render_template, request, url_for
from models import db, User, Phone
from datetime import datetime
import re
import os


# Конфигурация базы данных SQLite
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite.///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'simple_secret_key'


# Инициализация БД
db.init_app(app)


# Создание БД при запуске
with app.app_context():
    db.create_all()


'''--------USERS--------'''
# Главная страница - пользователи
@app.route('/')
def index():
    return render_template('index.html')


# Список пользователей (Read User)
@app.route('/users')
def users():
    all_users = User.query.all()
    return render_template('user.html', users = all_users)


# Добавление + редактирование пользователей (Create + Update User)
@app.route('/users/form', methods=['GET', 'POST'])
@app.route('/users/form/<int:id>', methods=['GET', 'POST'])
def user_form(id=None):
    user = None
    if id:
        user = User.query.get_or_404(id)

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        dob_str = request.form['date_of_birth']

        if not name:
            flash('Имя обязательно', 'error')
            return render_template('user_form.html', user=user)
        
        try:
            date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Неверная дата (YYYY-MM-DD)', 'error')
            return render_template('user_form.html', user=user)
        
        # Проверка уникальности email
        existing_user = User.query.filter_by(email=email).first()
        if existing_user and (not user or existing_user.id != user.id):
            flash('Этот Email уже используется', 'error')
            return render_template('user_form.html', user=user)
        
        if user:
            # Update
            user.name = name
            user.email = email
            user.date_of_birth = date_of_birth
            action = 'дбновлен'
        else:
            # Create
            use = User(name=name, email=email, date_of_birth=date_of_birth)
            db.session.add(user)
            action = 'добавлен'

        try:
            db.session.commit()
            flash(f'Пользователь {action}', 'success')
            return redirect(url_for('users'))
        except Exception as e:
            flash(f'Ошибка: {str(e)}', 'error')

    return render_template('user_form.html', user=user)


# Удаление пользователей (Delete User)
@app.route('/user/delete/<int:id>')
def delete_user(id):
    user = User.query.get_or_404(id)
    try:
        db.session.delete()
        db.session.commit()
        flash('Пользователь удален', 'success')
    except Exception as e:
        flash(f'Ошибка {str(e)}', 'error')
    return redirect(url_for('users'))