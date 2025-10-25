from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, NumberRange

# Formulário de Registro
class RegistroForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(min=6)])
    confirmar = PasswordField("Confirmar Senha", validators=[EqualTo("senha", message="As senhas devem ser iguais")])
    submit = SubmitField("Registrar")


# Formulário de Login
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    submit = SubmitField("Entrar")


# Formulário de Livro
class LivroForm(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired(), Length(min=1, max=200)])
    autor = StringField("Autor", validators=[DataRequired(), Length(min=1, max=100)])
    isbn = StringField("ISBN", validators=[Optional(), Length(max=20)])
    ano_publicacao = IntegerField("Ano de Publicação", validators=[Optional(), NumberRange(min=1000, max=9999)])
    editora = StringField("Editora", validators=[Optional(), Length(max=100)])
    descricao = TextAreaField("Descrição", validators=[Optional()])
    submit = SubmitField("Salvar")
