from flask import Flask, render_template, request, url_for, jsonify
from random import randint
import sqlite3

# SQL server
db = "database.db"

# Flask server
app = Flask(__name__)

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
    return render_template("registration.html", id=id_, name=name_, lname=lname_, email=email_, password=pass_)

@app.route("/returnSQL", methods=["GET", "POST"])
def funcao():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    if (request.method == "POST"):
        cursor.execute("""SELECT * FROM cadastro""")
        records = cursor.fetchall()

        print(records)
        print(records[0])
        
        return "True"
    else:
        return "False"

app.run(debug=True)