from flask import session, render_template, redirect, request, flash
from flask_app.models.user import User
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
@app.route("/")
def Home():
    return render_template("index.html")
@app.route("/register", methods=["POST"])
def register():
    if not User.validate_registration(request.form):
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash,
    }
    user = User.save(data)
    session["id"] = user
    return redirect("/success")
@app.route("/login", methods=["POST"])
def login():
    data = {"email":request.form["email"]}
    user = User.get_by_email(data)
    if not user:
        flash("Invalid email or password")
        return redirect("/")
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Invalid email or password")
        return redirect("/")
    session["id"] = user.id
    return redirect("/success")
@app.route("/success")
def success():
    data = {
        "id":session["id"]
    }
    return render_template("success.html", user = User.get_by_id(data))
@app.route("/logout")
def logout():
    session["id"] = ""
    return redirect("/")

