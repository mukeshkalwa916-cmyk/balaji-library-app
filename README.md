# balaji-library-app
Online Library Management App with Login, Admin Panel, Book Management and Fine System.
  GNU nano 9.0                                 app.py
from flask import Flask, request, redirect, session

import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "balaji123"

def init_db():
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    if "user" in session:
        return f"""
        <h1>📚 Balaji Library App</h1>
        <h3>Welcome {session['user']}</h3>
        <a href='/logout'>Logout</a>
        """
    return """
    <h1>📚 Balaji Library App</h1>
    <a href='/login'>Login</a><br>
    <a href='/signup'>Signup</a>
    """

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        conn = sqlite3.connect("library.db")
        cur = conn.cursor()
