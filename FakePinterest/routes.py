# criar as rotas do nosso ssite (links do site)

from flask import render_template, url_for, redirect
from FakePinterest import app, database, bcrypt
from FakePinterest.models import User, Posts
from flask_login import login_required, login_user, logout_user, current_user
from FakePinterest.forms import FormLogin, FormCriarConta, FormPosts
import os
from werkzeug.utils import secure_filename


@app.route("/", methods=["GET", "POST"])
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = User.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.password, formlogin.password.data):
            login_user(usuario)
            return redirect(url_for("perfil", user_id=usuario.id))
    return render_template('homepage.html', form=formlogin)


@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(form_criarconta.password.data)
        usuario = User(username=form_criarconta.username.data, password=senha, email=form_criarconta.email.data)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", user_id=usuario.id))
    return render_template("criarconta.html", form=form_criarconta)


@app.route("/perfil/<user_id>", methods=["GET", "POST"])
@login_required
def perfil(user_id):
    if int(user_id) == int(current_user.id):
        form_post = FormPosts()
        if form_post.validate_on_submit():
            file = form_post.picture.data
            safe_name = secure_filename(file.filename)
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"], safe_name)
            file.save(path)
            picture = Posts(image=safe_name, id_user=current_user.id)
            database.session.add(picture)
            database.session.commit()
        return render_template("perfil.html", usuario=current_user, form=form_post)
    else:
        usuario = User.query.get(int(user_id))
        return render_template("perfil.html", usuario=usuario, form=None)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))


@app.route("/feed")
@login_required
def feed():
    lista_fotos = Posts.query.order_by(Posts.data_criacao.desc()).all()
    return render_template("feed.html", fotos=lista_fotos)
