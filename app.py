from flask import Flask, render_template, request, url_for, jsonify, redirect, session
from random import randint
import sqlite3
from os import urandom

# SQL server
db = "database.db"

# Flask server
app = Flask(__name__)
app.secret_key = urandom(24).hex()

@app.route("/")
def mainPage():
    return render_template("page.html")

@app.route("/registration", methods=["GET", "POST"])
def registroPage(id_=False, name_=False, lname_=False, email_=False, pass_=False):
    def getRequestFormToSQL(form_name):
        return request.form[form_name]
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS cadastro (id, nome, sobrenome, email, senha)""")
        if (request.method == "POST"):
            while True:
                user_id = str(randint(0, 999))
                cursor.execute("""SELECT id FROM cadastro WHERE id=?""", (user_id,))
                check_id = cursor.fetchone()
                if check_id is None:
                    id_ = user_id
                    break
            name_ = getRequestFormToSQL("name")
            lname_ = getRequestFormToSQL("lastname")
            email_ = getRequestFormToSQL("email")
            pass_ = getRequestFormToSQL("password") 
            try:
                cursor.execute(f"""INSERT INTO cadastro (id, nome, sobrenome, email, senha) VALUES (?, ?, ?, ?, ?)""", (id_, name_, lname_, email_, pass_))
                conn.commit()
                conn.close()
            except Exception as e:
                return f"ERRO NO SQL: {e}"
        else:
            return f"/***# {request.method} ERROR CONDITION ---"
    except Exception as e:
        return f"/***# {request.method} ERROR EXCEPTION: {e}---"
    return redirect(url_for("mainPage"))

@app.route("/Cadastros")
def goToCadastros():
    try:
        records = session.get('records')
        id_user = session.get('id')

        if (records is not None):
            pass
        else:
            records = "USER NOT FOUND"
            
        if (id_user is not None):
            pass
        else:
            id_user = "ID USER NOT FOUND"

        return render_template("registration.html", records=records, id_user=id_user)
    except Exception as e:
        return e

@app.route("/returnSQL")
def returnSqlUserInfo():
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        try:
            getUser_id = request.args.get('id', default = 1, type = str)
            if (getUser_id is not None):
                cursor.execute("""SELECT * FROM cadastro WHERE id=?""", (getUser_id,))
                records = cursor.fetchone()
                if (records is not None):
                    session['records'] = records
                    session['id'] = getUser_id
                    conn.close()
                else:
                    session['id'] = None
                    session['records'] = None
            else:
                session['records'] = None
        except Exception as e:
            return e
        return redirect(url_for("goToCadastros"))
    except Exception as e:
        return e

app.run(debug=True)