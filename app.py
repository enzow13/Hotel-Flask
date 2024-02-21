from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route("/")
def mainPage():
    return render_template("page.html")

@app.route("/registration", methods=["GET", "POST"])
def registroPage():
    if (request.method == "POST"):
        nome = request.form["name"]
        senha = request.form["password"]
        return f"Seu nome é: {nome} e sua senha é {senha}"
    else:
        return request.method
    return render_template("registration.html")

app.run(debug=True)