import os
from flask import render_template, redirect, url_for, request, flash, send_from_directory
from flask_admin.contrib.sqla import ModelView
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_ckeditor import CKEditor, upload_success, upload_fail, CKEditorField
import random

from models import User, Blog, Category
from forms import LoginForm, RegisterForm, BlogForm
from models import app, db
from flask_admin import Admin

ckeditor = CKEditor(app)
app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'
app.config['CKEDITOR_PKG_TYPE'] = 'full'
UPLOAD_FOLDER = './static/site/image'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='blog', template_mode='bootstrap4')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Category, db.session))
class PostAdmin(ModelView):
    form_overrides = dict(text=CKEditorField)
    create_template = 'edit.html'
    edit_template = 'edit.html'

admin.add_view(PostAdmin(Blog, db.session))


@app.route('/files/<path:filename>')
def uploaded_files(filename):
    path = 'upload'
    return send_from_directory(path, filename)


@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    # Add more validations here
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    f.save(os.path.join('upload', f.filename))
    url = url_for('uploaded_files', filename=f.filename)
    return upload_success(url, filename=f.filename)


@app.route('/')
def index():
    post = Blog.query.all()
    category = Category.query.all()
    return render_template('index.html', post=post, category=category)


@app.route('/<slug_cat>/<slug>')
def post_detail(slug, slug_cat):
    categoty = Category.query.all()
    post=Blog.query.filter_by(slug=slug).first()
    return render_template('post_detail.html', post=post, categoty=categoty)


@app.route('/category/<slug_cat>')
def posts_category(slug_cat):
    category = Category.query.filter_by(slug=slug_cat).first()
    print(category)
    post = Blog.query.filter_by(category_id=category.id)
    return render_template('cat.html', post=post)


@app.route('/post/<int:id>/update', methods=['GET', 'POST'])
@login_required
def post_update(id):
    form = BlogForm(request.form)
    post = Blog.query.get(id)
    update_text = form.text.data
    form.text.data = post.text
    if request.method == 'POST':
        file1 = request.files['file1']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        if file1.filename:
            if file1.filename in path:
                a = random.randrange(1,550,1)
                path = os.path.join(app.config['UPLOAD_FOLDER'],  str(a) + file1.filename)
                file1.save(path)
    if form.validate():
        post.title = form.title.data
        post.text = update_text
        post.category_id = form.category.data
        if file1.filename:
            path = path.replace('.', '', 1)
            post.photo = path
        try:
            db.session.commit()
            flash('Изменения применены')
            return redirect(url_for('index'))
        except:
            return flash('Произошла ошибка')
    return render_template('post_update.html', post=post, form=form)


@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def upload_file():
    form = BlogForm(request.form)
    category = Category.query.all()
    if request.method == 'POST':
        file1 = request.files['file1']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)
        if form.validate():
            if current_user.is_authenticated:
                path = path.replace('.', '', 1)
                new_post = Blog(title=form.title.data,
                                text=form.text.data,
                                slug=form.slug.data,
                                photo=path,
                                user_id=current_user.id,
                                category_id=form.category.data)
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


app.run(debug=True)
