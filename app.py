from flask import Flask, flash, redirect, render_template, request, url_for
from models import db, User, Phone
from datetime import datetime
import re
import os


# Конфигурация базы данных SQLite
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'simple_secret_key'


# Инициализация БД
db.init_app(app)


# Создание БД при запуске
with app.app_context():
    db.create_all()


#Валидация для номерров
def validate_number(phone_number):
    return (phone_number.startswith('+') or phone_number.startswith('0')) and phone_number[1:].isdigit() and len(phone_number) >= 10


# Валидация для email
def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None



# Главная страница 
@app.route('/')
def index():
    users = User.query.all()
    phones = Phone.query.all()
    return render_template('index.html', users=users, phones=phones)


'''--------USERS--------'''
# # Список пользователей (Read User)
# @app.route('/users')
# def users():
#     all_users = User.query.all()
#     return render_template('user.html', users = all_users)


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
        date_of_birth_str = request.form['date_of_birth']

        if not name:
            flash('Имя обязательно', 'error')
            return render_template('user_form.html', user=user)
        
        # добавил валидацию
        if not validate_email(email):
            flash(f'Неверный email', 'error')
            return render_template('user_form.html', user=user)
        
        try:
            date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Неверная дата (YYYY-MM-DD)', 'error')
            return render_template('user_form.html', user=user)
        
        # Проверка уникальности email
        existing_user = User.query.filter_by(email=email).first()
        if existing_user and (not user or existing_user.id != user.id):
            flash('Этот Email уже используется', 'error')
            return render_template('user_form.html', user=user)
        
        if user:
            # Update User
            user.name = name
            user.email = email
            user.date_of_birth = date_of_birth
            action = 'обновлен'
        else:
            # Create User
            user = User(name=name, 
                        email=email, 
                        date_of_birth=date_of_birth)
            db.session.add(user)
            action = 'добавлен'

        try:
            db.session.commit()
            flash(f'Пользователь {action}', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Ошибка: {str(e)}', 'error')

    return render_template('user_form.html', user=user)


# Удаление пользователей (Delete User)
@app.route('/user/delete/<int:id>')
def delete_user(id):
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash('Пользователь удален', 'success')
    except Exception as e:
        flash(f'Ошибка при удаленини: {str(e)}', 'error')
    return redirect(url_for('index'))


'''--------PHONES--------'''
# # Список телефонов (Read Phones)
# @app.route('/phones')
# def phones():
#     all_phones = Phone.query.all()
#     return render_template('phones.html', phones=all_phones)


# Добавление + редактирование телефонов (Create + Update Phone)
@app.route('/phones/form', methods=['GET', 'POST'])
@app.route('/phones/form/<int:id>', methods=['GET', 'POST'])
def phone_form(id=None):
    phone = None
    if id:
        phone = Phone.query.get_or_404(id)
    
    users = User.query.all()

    if request.method == 'POST':
        phone_number = request.form['phone_number']
        user_id = int(request.form['user_id'])

        if not validate_number(phone_number):
            flash('Неверный номер', 'error')
            return render_template('phone_form.html', phone=phone, users=users)

        if phone:
            # Update Phone
            phone.phone_number = phone_number
            phone.user_id = user_id
            action = 'обновлен'
        else:
            # Create Phone
            phone = Phone(phone_number=phone_number, 
                          user_id=user_id)
            db.session.add(phone)
            action = 'добавлен'

        try:
            db.session.commit()
            flash(f'Телефон {action}', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Ошибка: {str(e)}', 'error')
        
    return render_template('phone_form.html', phone=phone, users=users)


# Удаление телефона (Delete Phone)
@app.route('/phones/delete/<int:id>')
def delete_phone(id):
    phone = Phone.query.get_or_404(id)
    try:
        db.session.delete(phone)
        db.session.commit()
        flash('Телефон удален', 'success')
    except Exception as e:
        flash(f'Ошибка удаления: {str(e)}', 'error')
    
    return redirect(url_for('index'))
    

if __name__ == '__main__':
    app.run(debug=True)
