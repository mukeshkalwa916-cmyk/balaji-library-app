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

        try:
            cur.execute(
                "INSERT INTO users(username,password) VALUES(?,?)",
                (username,password)
            )
            conn.commit()
        except:
            return "User already exists"

        conn.close()
        return redirect("/login")

    return """
    <h2>Signup</h2>
    <form method='post'>
        <input name='username' placeholder='Username'><br><br>
        <input type='password' name='password' placeholder='Password'><br><br>
        <button>Signup</button>
    </form>
    """

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("library.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT password FROM users WHERE username=?",
            (username,)
        )

        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user[0], password):
            session["user"] = username
            return redirect("/")

        return "Invalid Login"

    return """
    <h2>Login</h2>
    <form method='post'>
        <input name='username' placeholder='Username'><br><br>
        <input type='password' name='password' placeholder='Password'><br><br>
        <button>Login</button>
    </form>
    """

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
from flask import Flask, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "balaji123"

def init_db():
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()

    # Users Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # Books Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
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

        <a href='/admin'>Admin Panel</a><br><br>
        <a href='/books'>View Books</a><br><br>
        <a href='/logout'>Logout</a>
        """

    return """
    <h1>📚 Balaji Library App</h1>

    <a href='/login'>Login</a><br><br>
    <a href='/signup'>Signup</a>
    """

@app.route("/signup", methods=["GET","POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]
        password = generate_password_hash(
            request.form["password"]
        )

        conn = sqlite3.connect("library.db")
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO users(username,password) VALUES(?,?)",
                (username,password)
            )

            conn.commit()

        except:
            return "User Already Exists"

        conn.close()

        return redirect("/login")

    return """
    <h2>Signup</h2>

    <form method='post'>
        <input name='username' placeholder='Username'><br><br>

        <input type='password'
               name='password'
               placeholder='Password'><br><br>

        <button>Signup</button>
    </form>
    """

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("library.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT password FROM users WHERE username=?",
            (username,)
        )

        user = cur.fetchone()

        conn.close()

        if user and check_password_hash(
            user[0], password
        ):
            session["user"] = username
            return redirect("/")

        return "Invalid Login"

    return """
    <h2>Login</h2>

    <form method='post'>
        <input name='username'
               placeholder='Username'><br><br>

        <input type='password'
               name='password'
               placeholder='Password'><br><br>

        <button>Login</button>
    </form>
    """

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

@app.route("/admin")
def admin():

    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("library.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM books")
    books = cur.fetchall()

    conn.close()

    html = """
    <h1>📚 Balaji Library Admin Panel</h1>

    <form action='/add_book' method='post'>
        <input name='book'
               placeholder='Book Name'>

        <button>Add Book</button>
    </form>

    <hr>
    """

    for book in books:

        html += f"""
        {book[1]}
        <a href='/delete_book/{book[0]}'>
        Delete
        </a><br>
        """

    return html

@app.route("/add_book", methods=["POST"])
def add_book():

    if "user" not in session:
        return redirect("/login")

    book = request.form["book"]

    conn = sqlite3.connect("library.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO books(name) VALUES(?)",
        (book,)
    )

    conn.commit()
    conn.close()

    return redirect("/admin")

@app.route("/delete_book/<int:id>")
def delete_book(id):

    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("library.db")
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM books WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/admin")

@app.route("/books")
def books():

    conn = sqlite3.connect("library.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM books")

    data = cur.fetchall()

    conn.close()

    html = "<h1>📚 Balaji Library Books</h1>"

    for book in data:
        html += f"<p>{book[1]}</p>"

    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
