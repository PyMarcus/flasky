import time
from typing import Any
from flask import Flask, request, g, current_app, session, url_for
from flask import make_response, redirect, abort, render_template
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Email, DataRequired, InputRequired, Length, EqualTo
from flask import request, flash
"""
Toda a aplicação flask deve ter uma instância
de Flask, pois, por meio dela, há os dados de
requisicao do cliente, que são recebidos e 
manipulados na instância pelo protocolo Web
Server Gateway Interface (WSGI)
"""

app = Flask(__name__)
moment = Moment(app)

STATUS_CODE_200_OK = 200
STATUS_CODE_404_NOT_FOUND = 404
STATUS_CODE_204_NO_RESULT = 204
STATUS_CODE_302_REDIRECT = 302
STATUS_CODE_201_CRETED = 201
STATUS_CODE_500_SERVER_ERROR = 500


# criação de rotas
@app.route("/")  # as rotas possuem as funções para manipular o acesso à URL passada
def index():  # função view, aquela que é chamada por uma rota e exibe uma response para o user ver
    if session.get('name') != 'okok':
        print("OK2")
        print(session.get('name'))
        flash("OK", "info")

    return render_template("index.html", len=len), STATUS_CODE_200_OK


# rotas dinâmicas
@app.route("/home/<int:year>/<name>")
def home(year, name):
    return f"Happy new year ({year}), {name}", STATUS_CODE_200_OK


# flask tem threads que atendem a vários clientes
@app.route("/global_variables")
def global_variables():
    """
    Variaveis globais que contém informações:
    g -> armazena info temporariamente, até uma nova request
    request -> informações http da requisicao
    session -> infor da sessão
    current_app -> info da app atual
    Assim, há momentos para essas variaveis estarem disponíveis, quando
    recebem uma requisicao, cria-se o contexto e a thread tem acesso
    :return:
    """
    print(f"Request: {request.host}")
    print(f"Request: {request.headers}")
    print(f"G: {g}")
    print(f"Current_app = {current_app.name}")
    print(f"Session: {session.items()}")
    return "Pronto", STATUS_CODE_200_OK


def request_hooks() -> tuple[str, int]:
    """
    Antes e depois de algumas requisições,
    pode-se querer processar algumas informações, para isso,
    o flask têm os hooks:
    before_first_request
    before_request
    after_request
    Cada retorno da função é chamado response
    Mas, na web, é necessario retornar o status code
    que, no flask,por padrão, é 200
    """
    return "<h1>Response</h1>", STATUS_CODE_200_OK


@app.route("/setcookie")
def make_response_c() -> Any:
    # make response permite criar um objeto response
    response = make_response("This document carries a cookie!")
    response.set_cookie("Key", "value")
    if session.get('name') != 'okok':
        print("OK2")
        print(session.get('name'))
        flash("Nome estranho!")
    return response


@app.route('/redirect')
def redirect_to_yt() -> Any:
    return redirect("https://www.youtube.com.br"), STATUS_CODE_302_REDIRECT


@app.route("/abort/<int:id>")
def using_abort_functions(id: int) -> Any:
    if id not in [1, 2, 3]:
        abort(404, "Message")
    else:
        return "<h1>OK</h1>", STATUS_CODE_200_OK


@app.route('/template/<user>')
def generate_a_template(user: str) -> Any:
    # flask usa templates para tornar a aplicação
    # fácil de manter e modificar
    # usa o engine jinja2 para isso
    # jinja escapa as variáveis, ou seja, não deixa que vaze codigo html como variavel
    return render_template("index.html", user=user, len=len)


@app.route("/h")
def herdado():
    return render_template("herdado.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("custom_error_page.html", error=e, current_time=datetime.utcnow()), STATUS_CODE_404_NOT_FOUND


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("custom_error_page.html", error=e), STATUS_CODE_500_SERVER_ERROR


def flask_moment():
    # trabalhar com fuso horario com flask moment
    # assim, a hora se adequa a do navegador do usuário
    return datetime.utcnow()


# web forms
"""
Trabalhar com formulários com flask é simples
usando WTForms, que pode gerenciar os dados
de formulário
pip install flask-wtf
Ele evita CRFS que é um ataque que visa manipular a interação do usuário com
um site
"""
# configurar uma chave criptográfica para proteger informações do usuário ao enviar pelo formulário
app.config['SECRET_KEY'] = "RANDOMKEY"  # armazenar em variáveis de ambiente


# classe que realiza verificação
class NameForm(FlaskForm):
    """
    Campos suportados
    StringFieldText field
    TextAreaFieldMultiple-line text field
    PasswordFieldPassword text field
    HiddenFieldHidden text field
    DateFieldText field that accepts a datetime.date value in a given format
    DateTimeFieldText field that accepts a datetime.datetime value in a given format
    IntegerFieldText field that accepts an integer value
    DecimalFieldText field that accepts a decimal.Decimal value
    FloatFieldText field that accepts a floating-point value
    BooleanFieldCheckbox with True and False values
    RadioFieldList of radio buttons
    SelectFieldDrop-down list of choices
    SelectMultipleField Drop-down list of choices with multiple selection
    FileFieldFile upload field
    SubmitFieldForm submission button
    FormFieldEmbed a form as a field in a container form
    FieldListList of fields of a given type
    """
    name = StringField("What's your name?", validators=[DataRequired(), InputRequired()])
    email = StringField("What's your email?", validators=[Email()])  # pip install email_validator
    password = PasswordField("Pass: ",validators = [
                  Length(min=1, message='Password should be at least %(min)d characters long')])
    confirm_password = PasswordField(
    label = ('Confirm Password'),
    validators=[EqualTo('password', message='Both password fields must be equal!')])
    submit = SubmitField("Submit")


@app.route('/form', methods=['GET', 'POST'])  # post tem body
def form():
    name = None
    form = NameForm()
    print(f"AQ {form.password.data}")
    #if form.validate_on_submit():  # true se passar pelos validadores
    print("OK")
    session['name'] = form.name.data
    name = form.name.data  # busca os dados
    form.name.data = ''  # reseta
    form.password.data = ''
    form.confirm_password.data = ''
    form.email.data = ''


    return render_template('form.html', form=form), STATUS_CODE_200_OK


"""
Sessão do usuário
Ao efetuar um login etc, um form ,no geral,
são armazenadas informações em um local privado chamado sessão do usuário
Por padrão, as sessões de usuário estão contidas nos cookies e são cripto
grafadas com a key das config 
"""


@app.route('/usersession', methods=['GET', 'POST'])
def sess():
    form = NameForm()
    if request.method == "POST":
        print(form.email)
        flash("OK", "success")
        print(form.password)
        #if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('index')), STATUS_CODE_302_REDIRECT
    else:
        return render_template('user.html', form=form), STATUS_CODE_200_OK


if __name__ == '__main__':
    app.run(debug=True)  # debug true permite reload
