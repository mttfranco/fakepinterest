# criar os formularios do site
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from FakePinterest.models import User


class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    button_confirm = SubmitField("Fazer Login")
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("Usuario inexistente, crie uma conta.")

class FormCriarConta(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    username = StringField("User Name", validators=[DataRequired(), ])
    password = PasswordField("Password", validators=[DataRequired(), Length(6, 20), ])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    button_confirm = SubmitField("Create Account")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("E-mail já cadastrado, faça login para continuar.")


class FormPosts(FlaskForm):
    picture = FileField("Foto", validators=[DataRequired()])
    confirm_buton = SubmitField("Enviar")
