import sqlite3
from flask import Flask, request

app = Flask(__name__)

# FALHA 3: segredo hardcoded (valor FALSO)
API_KEY = "sk-fake-1234567890abcdef"

def get_db():
    return sqlite3.connect("app.db")

@app.route("/user")
def buscar_usuario():
    nome = request.args.get("nome", "")
    cur = get_db().cursor()
    # FALHA 1: SQL Injection (entrada colada na query)
    cur.execute(f"SELECT * FROM users WHERE name = '{nome}'")
    return str(cur.fetchall())

@app.route("/ola")
def ola():
    nome = request.args.get("nome", "")
    # FALHA 2: XSS (entrada devolvida sem escape)
    return "<h1>Olá, " + nome + "!</h1>"