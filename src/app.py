from flask import Flask, render_template, request, redirect, url_for, flash, session, escape
from . import config
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)	

from src.models import Containers, Users


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        errors = check_form( request.form["username"],request.form["password"],request.form["email"])
        if not errors :
            hashed_pw = generate_password_hash(request.form["password"], method="sha256" )
            new_user = Users(username=request.form["username"], password = hashed_pw, email = request.form["email"])
            db.session.add(new_user)
            db.session.commit()
            flash("Te has registrado correctamente.", "acierto")
            return redirect(url_for('login'))
        for error in errors:
            flash( "" + error + " ", "error")

    else:
        return render_template('signup.html')




@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        errors = check_form( request.form["username"],request.form["password"])
        if not errors:
            user = Users.query.filter_by(username=request.form["username"]).first()
            if user and check_password_hash(user.password, request.form["password"]):
                session["username"] = user.username
                flash("Has iniciado sesión.", "acierto")
                return redirect(url_for('home'))
            flash("Error revisa", "error")
        for error in errors:
            flash( "" + error + " ", "error")    
    else:
        return render_template('login.html')


def check_form(user, psw, email = None):
    errors = []
    if user == '':
        errors.append("Usuario incorrecto")
    if psw == '':
        errors.append("Contrseña incorrecta") 
    if email == '':
        errors.append("Email incorrecto")
    
    return errors

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Has cerrado sesión", "acierto")
    return redirect(url_for('home'))

@app.route("/containers", methods = ['GET', 'POST'])
def containers():
    if request.method == 'POST':
        ccz = request.form["ccz"]
        nombre_con= request.form["nombre_con"]
        resultados = Containers.query.filter_by(CCZ=ccz).filter_by(NOMBRE_CON=nombre_con).first()
        return "" + resultados.DIRECCION + ""
    else:
        listCCZ = []
        listNOMBRE_CON = []
        for container in Containers.query.all(): 
            if not container.CCZ in listCCZ:
                listCCZ.append(container.CCZ)  
            if not container.NOMBRE_CON in listNOMBRE_CON:
                listNOMBRE_CON.append(container.NOMBRE_CON)
        listCCZ.sort()
        return render_template('containers.html', listCCZ = listCCZ, listNOMBRE_CON = listNOMBRE_CON)


@app.route("/edit_user")
def edit_user():
    if request.method == 'POST':
        return "POST"
    else:
        return render_template('edit_user.html')






if __name__ == '__main__':
    app.run(debug=True)