from flask import Flask, render_template, render_template_string, request, redirect, url_for
import smtplib, secrets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
usuarios = {}

email_remetente = os.environ.get("EMAIL_REMETENTE")
sua_senha = os.environ.get("SENHA_EMAIL")
smtp_server = "smtp.gmail.com"
smtp_porta = 587

def enviar_email(destinatario, nome, token):
    link = url_for('confirmacao_email', token=token, _external=True)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Confirmação de Cadastro"
    msg["From"] = email_remetente
    msg["To"] = destinatario

    corpo_email = f""""
        <p>Olá {nome},</p>
        <p>Ficamos muito felizes com o seu cadastro!</p>
        <p>Mas para processeguirmos precisamos confirmar o seu email.</p>
        <p>Clique em {link} para confirmar seu cadastro!</p>
    """
    msg.attach(MIMEText(corpo_email, "html"))

    with smtplib.SMTP(smtp_server, smtp_porta) as server:
        server.starttls()
        server.login(email_remetente, sua_senha)
        server.sendmail(email_remetente, destinatario, msg.as_string())

@app.route('/')
def index():
    return render_template('cadastro.html')

@app.route('/cadastro', methods=["POST"])
def cadastro():
    nome = request.form["nome"]
    email =  request.form["email"]
    senha = request.form["senha"]

    if email in usuarios:
        return "E-mail já está cadastrado!", 400

    token = secrets.token_urlsafe(16)
    usuarios[email] = {"nome": nome, "senha": senha, "verificado": False, "token": token}

    enviar_email(email, nome, token)
    return "Cadastro realizado com sucesso! Verifique seu e-mail para confirmar o cadastro."

@app.route('/confirmacao_email/<token>')
def confirmacao_email(token):
    for email,dados in usuarios.items():
        if dados.get("token") == token:
            dados["verificado"] = True
            dados["token"] = None
            return "E-mail confirmado com sucesso! Faça seu login."
    return "Link inválido ou expirado.", 400

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=["POST"])
def login():
    email = request.form["email"]
    senha = request.form["senha"]

    usuario = usuarios.get(email)
    if not usuario or usuario["senha"] != senha:
        return "E-mail ou senha incorretos!", 401

    if not usuario["verificado"]:
        return "Confirme seu e-mail antes de fazer o login.", 403
    return "Login realizado com sucesso!"

if __name__ == '__main__':
    app.run(debug=True)