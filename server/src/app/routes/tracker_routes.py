from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required

tracker_bp = Blueprint("tracker", __name__)


@tracker_bp.get("/")
def view_landing_page():
    # Landing page pública (antes do login)
    return render_template("registration/landing_page.html")


@tracker_bp.get("/tracker", endpoint="home")
@login_required
def view_media_list():
    # Dashboard pessoal (onde as funcionalidades de tracking serão usadas)
    return render_template("tracker/media_list.html")


@tracker_bp.get("/explore")
@login_required
def explore():
    # Página de "Explorar" depois do login, explicando as funcionalidades
    return render_template("tracker/explore.html")


@tracker_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_media():
    # Stub simples: futuro backend vai salvar no banco
    if request.method == "POST":
        # Aqui no futuro: criar item, associar ao usuário etc.
        return redirect(url_for("tracker.home"))

    return render_template("tracker/add_media.html")


@tracker_bp.get("/<int:media_id>/edit")
@login_required
def edit_media(media_id):
    # Stub de exemplo para edição
    media = {
        "id": media_id,
        "title": "Sample",
        "status": "",
        "rating": "",
        "type": "",
        "description": "",
    }
    return render_template("tracker/edit_media.html", media=media)


@tracker_bp.route("/<int:media_id>/delete", methods=["GET", "POST"])
@login_required
def delete_media(media_id):
    media = {"id": media_id, "title": "Sample"}
    if request.method == "POST":
        # Futuro: apagar de fato e redirecionar
        return redirect(url_for("tracker.home"))

    return render_template("tracker/delete_media.html", media=media)


@tracker_bp.get("/shelf")
@login_required
def shelf():
    rated_media = []
    favorite_media = []
    return render_template(
        "tracker/shelf.html",
        rated_media=rated_media,
        favorite_media=favorite_media,
    )


@tracker_bp.get("/friends")
@login_required
def friends():
    friend_invites = []
    friends = []
    return render_template(
        "tracker/friends.html",
        friend_invites=friend_invites,
        friends=friends,
    )
