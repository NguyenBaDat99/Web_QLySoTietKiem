from app import app, login
from flask import render_template, redirect, request
from app.models import AdminAccount
from flask_login import login_user
import hashlib


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login-admin", methods=["post", "get"])
def login_admin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password", "")
        password = hashlib.md5(password.strip().encode("utf-8")).hexdigest()
        ad = AdminAccount.query.filter(AdminAccount.username == username.strip(),
                                       AdminAccount.password == password).first()
        if ad:
            login_user(user=ad)
    return redirect("/admin")


@login.user_loader
def admin_load(admin_id):
    return AdminAccount.query.get(admin_id)


if __name__ == "__main__":
    app.run(debug=True)
