import os
import sqlite3
from flask import Flask, request, render_template_string

app = Flask(__name__)

# CORREÇÃO 3: segredo vem do ambiente, não do código
API_KEY = os.environ.get("API_KEY")

def get_db():
    return sqlite3.connect("app.db")

@app.route("/user")
def buscar_usuario():
    nome = request.args.get("nome", "")
    cur = get_db().cursor()
    # CORREÇÃO 1: query parametrizada
    cur.execute("SELECT * FROM users WHERE name = ?", (nome,))
    return str(cur.fetchall())

@app.route("/ola")
def ola():
    nome = request.args.get("nome", "")
    # CORREÇÃO 2: template com escape automático
    return render_template_string("<h1>Olá, {{ nome }}!</h1>", nome=nome)