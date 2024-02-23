from flask import Flask, render_template, request, url_for
import sqlite3

# Flask server
app = Flask(__name__)

@app.route("/")
def mainPage():
    return render_template("page.html")

@app.route("/registration", methods=["GET", "POST"])
def registroPage(name_=False, lname_=False, email_=False, pass_=False):
    try:
        if (request.method == "POST"):
            name_ = request.form["name"]
            lname_ = request.form["lastname"]
            email_ = request.form["email"]
            pass_ = request.form["password"]
            try:
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS cadastro (nome, sobrenome, email, senha)""")
                cursor.execute(f"""INSERT INTO cadastro (nome, sobrenome, email, senha) VALUES (?, ?, ?, ?)""", (name_, lname_, email_, pass_))
                conn.commit()
                conn.close()
            except Exception as e:
                return f"ERRO NO SQL: {e}"
        else:
            return f"/***# {request.method} ERROR CONDITION ---"
    except:
        return f"/***# {request.method} ERROR EXCEPTION ---"
    return render_template("registration.html", name=name_, lname=lname_, email=email_, password=pass_)

app.run(debug=True)