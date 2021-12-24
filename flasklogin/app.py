import os
from flask import render_template, redirect, url_for, request, flash
from flask_admin.contrib.sqla import ModelView
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash


from models import User, load_user, Blog
from forms import LoginForm, RegisterForm, BlogForm
from models import app, db
from flask_admin import Admin


UPLOAD_FOLDER = './static/site/image'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='blog', template_mode='bootstrap4')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Blog, db.session))


@app.route('/', methods=['GET', 'POST'])
def index():
    post = Blog.query.all()
    return render_template('index.html', post=post)


@app.route('/add_post', methods=['GET', 'POST'])
def upload_file():
    form = BlogForm(request.form)
    if request.method == 'POST':
        file1 = request.files['file1']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)
        if form.validate():
            new_post = Blog(title=form.title.data,
                            text=form.text.data,
                            photo=path)
            db.session.add(new_post)
            db.session.commit()
            flash('add')
            return redirect(url_for('index'))
    return render_template('index1.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm(request.form)
    if form.validate():
        user = User.query.filter_by(login=form.login.data).first()
        if user is not None and check_password_hash(user.password, form.password.data):
            next_page = request.args.get('next')
            login_user(user)
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('index'))
        else:
            flash('Login or password is not correct')

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form, csrf_enabled=False)
    password = form.password.data
    password2 = form.confirm.data
    for i in User.query:
        if i.phone == form.phone.data:
            flash('Этот телефон уже используется')
    for i in User.query:
        if i.email == form.email.data:
            flash('Этот email уже используется')
    if password != password2:
        flash('Пароли не совпадают')
    if form.validate():
        hash_pwd = generate_password_hash(form.password.data)
        new_user = User(login=form.login.data,
                        password=hash_pwd,
                        email=form.email.data,
                        phone=form.phone.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)

    return response


if __name__ == '__main__':
    app.run(debug=True)
