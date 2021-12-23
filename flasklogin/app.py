from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import User
from forms import LoginForm, RegisterForm
from models import app, db


@app.route('/')
@login_required
def hello_world():  # put application's code here
    flash('sefsf')
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm(request.form)
    if form.validate():
        user = User.query.filter_by(login=form.login.data).first()
        if user is not None and check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page)
        else:
            flash('Login or password is not correct')

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form, csrf_enabled=False)
    password = form.password.data
    password2 = form.confirm.data
    for i in User.query:
        if i.login == form.login.data:
            flash('Это имя уже занято')
    if password != password2:
        flash('Пароли не совпадают')
    if form.validate():
        hash_pwd = generate_password_hash(form.password.data)
        new_user = User(login=form.login.data,
                            password=hash_pwd)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались')
        return redirect(url_for('hello_world'))
    return render_template('register.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('hello_world'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)

    return response


if __name__ == '__main__':
    app.run(debug=True)
