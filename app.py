from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'yatvoyamatb'  # секретный ключ для сессий

# Временные базы данных для хранения пользователей и паст
users = {}
paste_id_counter = 1
pastes = []

# Главная страница для отображения всех паст
@app.route('/')
def index():
    return render_template('index.html', pastes=pastes)

# Маршрут для регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash('Имя пользователя уже занято. Попробуйте другое.')
        else:
            # Хеширование пароля перед сохранением
            users[username] = generate_password_hash(password)
            flash('Регистрация прошла успешно! Войдите в систему.')
            return redirect(url_for('login'))
    return render_template('register.html')

# Маршрут для входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_hash = users.get(username)
        if user_hash and check_password_hash(user_hash, password):
            session['username'] = username
            flash('Вход выполнен успешно!')
            return redirect(url_for('index'))
        else:
            flash('Неправильное имя пользователя или пароль.')
    return render_template('login.html')

# Маршрут для выхода
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Вы вышли из системы.')
    return redirect(url_for('index'))

# Маршрут для создания новой пасты (доступен только авторизованным пользователям)
@app.route('/create_paste', methods=['POST'])
def create_paste():
    if 'username' not in session:
        flash('Вам нужно войти в систему, чтобы создавать пасты.')
        return redirect(url_for('login'))

    global paste_id_counter
    title = request.form.get('title')
    content = request.form.get('content')
    author = session['username']
    if title and content:
        new_paste = {
            "id": paste_id_counter,
            "title": title,
            "content": content,
            "timestamp": datetime.now().strftime("%d.%m.%Y, %H:%M:%S"),
            "author": author
        }
        pastes.append(new_paste)
        paste_id_counter += 1
        flash('Паста успешно создана!')
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

# Маршрут для просмотра деталей пасты
@app.route('/paste/<int:paste_id>')
def view_paste(paste_id):
    paste = next((p for p in pastes if p["id"] == paste_id), None)
    if paste:
        return render_template('paste_detail.html', paste=paste)
    else:
        return "Паста не найдена", 404


if __name__ == '__main__':
    app.run(debug=True)
