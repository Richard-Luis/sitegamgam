from flask import Flask, render_template, request, redirect, url_for
import smtplib, secrets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import mysql.connector
from merkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)

email_remetente = os.environ.get("EMAIL_REMETENTE")
sua_senha = os.environ.get("SENHA_EMAIL")
smtp_server = "smtp.gmail.com"
smtp_porta = 587

def conectando_ao_banco():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )

def enviando_email(destinatario, nome, token):
    """Este e-mail é para a confirmação do seu cadastro."""
    link = url_for('confirmacao_email', token=token, _external=True)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Confirmação de Cadastro"
    msg["From"] = email_remetente
    msg["To"] = destinatario

    texto_email = f"""
    <p>Olá {nome},</p>

    <p>Obrigado por se cadastrar no nosso site. Por favor, clique no link abaixo para confirmar seu cadastro:</p>

    <p><a href="{link}">Confirmar Cadastro</a></p>

    <p>O link de confirmação é válido por 24 horas.</p>

    <p>Se você não se cadastrou em nosso site, por favor ignore este e-mail.</p>

    <p>Atenciosamente,</p>
    <p>Equipe GamGam!</p>
    """

    msg.attach(MIMEText(texto_email, "html"))

    with smtplib.SMTP(smtp_server, smtp_porta) as server:
        server.starttls()
        server.login(email_remetente, sua_senha)
        server.sendmail(email_remetente, destinatario, msg.as_string())

def email_redefinicao(destinatario, nome, token):
    """E-mail de redefinição de senha."""
    link = url_for('redefinir_senha', token=token, _external=True)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Redefinição de Senha"
    msg["From"] = email_remetente
    msg["To"] = destinatario

    texto_email = f"""
    <p>Olá {nome},</p>

    <p>Recebemos uma solicitação para redefinir sua senha. Por favor, clique no link abaixo para redefinir sua senha:</p>

    <p><a href="{link}">Redefinir Senha</a></p>

    <p>O link de redefinição é válido por 24 horas.</p>

    <p>Se você não solicitou a redefinição de senha, por favor ignore este e-mail.</p>

    <p>Atenciosamente,</p>
    <p>Equipe GamGam!</p>
"""
    msg.attach(MIMEText(texto_email, "html"))
    with smtplib.SMTP(smtp_server, smtp_porta) as server:
        server.starttls()
        server.login(email_remetente, sua_senha)
        server.sendmail(email_remetente, destinatario, msg.as_string())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/esqueci-senha')
def esqueci_senha():
    return render_template('esqueci_senha.html')

@app.route('/cadastro', methods=["POST"])
def cadastro():
    nome = request.form["nome"]
    email = request.form["email"]
    senha = request.form["senha"]

    senha_hash = generate_password_hash(senha)
    token = secrets.token_urlsafe(16)

    conexao = get_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (nome, email, senha, verificado, token) VALUES (%s, %s, %s, %s, %s)", (nome, email, senha_hash, False, token))
        conexao.commit()
    except mysql.connector.errors.IntegrityError:
        return "Este e-mail já está cadastrado. Por favor, tente outro e-mail.", 400
    finally:
        cursor.close()
        conexao.close()

    enviando_email(email, nome, token)
    return "Cadastro realizado com sucesso! Por favor, verifique seu e-mail para confirmar seu cadastro."

@app.route('/confirmar_email/<token>')
def confirmacao_email(token):
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome FROM usuarios WHERE token = %s", token)
    usuario = cursor.fetchone()
    if usuario is None:
        cursor.close()
        conexao.close()
        return "Token Inválido ou expirado.", 400

    cursor.execute("UPDATE usuarios SET verificado = TRUE, token = NULL WHERE token = %s", (token,))
    conexao.commit()
    cursor.close()
    conexao.close()
    return "E-mail confirmado com sucesso! Você já pode fazer login."

@app.route('/login', methods=["POST"])
def login():
    email = request.form["email"]
    senha = request.form["senha"]

    conexao = get_conexao()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
    usuario = cursor.fetchone()
    cursor.close()
    conexao.close()

    if not usuario or not check_password_hash(usuario["senha"], senha):
        return "E-mail ou senha incorretos.", 401
    if not usuario["verificado"]:
        return "E-mail não confirmado. Por favor, verifique seu e-mail.", 403
    return f"Bem-vindo, {usuario["nome"]}! Você está logado com sucesso."

