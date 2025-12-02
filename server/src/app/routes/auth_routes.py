# TODO: Implement account deletion

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from src.use_cases.auth_use_cases import AuthUseCases
from src.infra.repositories.user_repository import UserRepository

auth = Blueprint("auth", __name__)

# Dependency injection would be better, but for now
auth_use_cases = AuthUseCases(UserRepository())


@auth.route("/login")
def login():
    return render_template("registration/login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = auth_use_cases.login(email, password)
    if not user:
        flash("Please check your login details and try again.")
        return redirect(url_for("auth.login"))

    login_user(user, remember=remember)
    return redirect(url_for("tracker.home"))


@auth.route("/signup")
def signup():
    return render_template("registration/sign_up.html")


@auth.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")

    try:
        auth_use_cases.signup(email, name, password)
        return redirect(url_for("auth.login"))
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("auth.signup"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("tracker.view_landing_page"))


@auth.route("/delete-account", methods=["GET", "POST"])
@login_required
def delete_account():
    if request.method == "POST":
        return redirect(url_for("tracker.home"))
    return render_template("registration/delete_account.html")
