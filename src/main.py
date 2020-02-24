from flask import Flask, render_template, request, session, escape, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

dbdir = 'sqlite:///' + os.path.abspath(os.getcwd()) + '/database.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = dbdir
app.config['SQLALCHEMY_TRACE_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = "123"

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/search")
def search():
    nickname = request.args.get("username")

    users = Users.query.filter_by(username = nickname)
    for user in users:
       return  user.username 
    return "Este usuario no existe"


@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        errors = check_form(request.form["username"], request.form["password"], request.form["email"])
        if not errors :
            hashed_pw = generate_password_hash(request.form["password"], method="sha256" )
            new_user = Users(username=request.form["username"], password = hashed_pw, email = request.form["email"])
            db.session.add(new_user)
            db.session.commit()
            flash("Te has registrado correctamente.", "acierto")
            return redirect(url_for('login'))
        for error in errors:
            flash( "" + error + " ", "error")
    return render_template('signup.html')

@app.route("/check_form")
def check_form(user, psw, email = None):
    errors = []
    if user == '':
        errors.append("Usuario incorrecto")
    if psw == '':
        errors.append("Contrseña incorrecta") 
    if email == '':
        errors.append("Email incorrecto")
    
    return errors

@app.route("/login", methods=["GET", "POST" ])
def login():
    if request.method == 'POST':
        errors = check_form(request.form["username"], request.form["password"])

        if not errors:
            user = Users.query.filter_by(username=request.form["username"]).first()
            if user and check_password_hash(user.password, request.form["password"]):
                session["username"] = user.username
                flash("Has iniciado sesión.", "acierto")
                return redirect(url_for('home'))
            flash("Error revisa", "error")
        for error in errors:
            flash( "" + error + " ", "error")
    return render_template('login.html')

 

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Has cerrado sesión", "acierto")
    return redirect(url_for('home'))


@app.route("/geo")
def geo():
    return render_template('geo.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
