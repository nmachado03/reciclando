from src import app, db
from flask import render_template, request, redirect, url_for, flash, session, escape, abort
from werkzeug.security import generate_password_hash, check_password_hash
from src.schemas.models import Containers, Users

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = Users.query.filter_by(
            username=request.form["username"]).first()
        if username:
            flash("Ese nombre de usuario ya existe, intente uno nuevo", "alert-error")
            return redirect(url_for('signup'))
            
        hashed_pw = generate_password_hash(
            request.form["password"], method="sha256")
        new_user = Users(
            username=request.form["username"], password=hashed_pw, email=request.form["email"])
        db.session.add(new_user)
        db.session.commit()
        flash("Te has registrado correctamente.", "alert-acierto")
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = Users.query.filter_by(username=request.form["username"]).first()
        if user and check_password_hash(user.password, request.form["password"]):
            session["username"] = user.username
            flash("Has iniciado sesión.", "alert-acierto")
            return redirect(url_for('home'))
        flash(
            "Las  credenciales ingresadas son invalidas, revisa e intenta de nuevo", "alert-error")

    return render_template('login.html')


@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Has cerrado sesión", "alert-acierto")
    return redirect(url_for('home'))


@app.route("/containers", methods=['GET', 'POST'])
def containers():
    if request.method == 'POST':
        ccz = request.form["ccz"]
        nombre_con = request.form["nombre_con"]
        return redirect(url_for('result', ccz = ccz, nombre_con = nombre_con))
    else:
        listCCZ = []
        listNOMBRE_CON = []
        for container in Containers.query.all():
            if not container.CCZ in listCCZ:
                listCCZ.append(container.CCZ)
            if not container.NOMBRE_CON in listNOMBRE_CON:
                listNOMBRE_CON.append(container.NOMBRE_CON)
        listCCZ.sort()
        return render_template('containers.html', listCCZ=listCCZ, listNOMBRE_CON  = listNOMBRE_CON )

@app.route("/result/<ccz>/<nombre_con>")
def result(ccz, nombre_con):
    results = Containers.query.filter_by(CCZ=ccz).filter_by(NOMBRE_CON=nombre_con).limit(10).all()
    return render_template('result.html', results = results)


@app.route("/edit_user")
def edit_user():
    if request.method == 'POST':
        return "POST"
    else:
        return render_template('edit_user.html')


@app.errorhandler(404)
def page_not_fpund(err):
    return render_template('page_not_found.html'), 404
