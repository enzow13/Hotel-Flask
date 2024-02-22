from flask import Flask, render_template, request, url_for
from os import path
from json import dump, load

app = Flask(__name__)

@app.route("/")
def mainPage():
    return render_template("page.html")

# Defs route registration
def jsonSendData(pathfile_, data_):
    """
    This function provides the data to be sent in a json file. It tries to search 
    for a json file and send the data, but if it doesn't exists, creates one json file to send it.

    args:
    :param: pathfile_ -> String .json file
    :param: data_ -> JSON object
    """
    try:
        if not path.exists(pathfile_):
            with open(pathfile_, "w") as file:
                dump(data_, file, indent=4)
                file.close()
        else:
            with open(pathfile_, "r") as file:
                data = load(file)
            data.append(data_)

            with open(pathfile_, "w") as file:
                dump(data, file, indent=4)
                file.close()
    except Exception as erro:
        return f"An error ocurried when tried to send the json data: {erro}"

@app.route("/registration", methods=["GET", "POST"])
def registroPage(name_=False, lname_=False, email_=False, pass_=False):
    try:
        if (request.method == "POST"):
            name_ = request.form["name"]
            lname_ = request.form["lastname"]
            email_ = request.form["email"]
            pass_ = request.form["password"]

            data_ = {
                "nome": name_,
                "sobrenome": lname_,
                "email": email_,
                "senha": pass_
            }

            jsonSendData("database.json", data_)
            pass
        else:
            return f"/***# {request.method} ERROR CONDITION ---"
    except:
        return f"/***# {request.method} ERROR EXCEPTION ---"
    return render_template("registration.html", name=name_, lname=lname_, email=email_, password=pass_)

app.run(debug=True)