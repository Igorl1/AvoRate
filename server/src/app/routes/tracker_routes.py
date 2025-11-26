from flask import Blueprint, render_template
from flask_login import login_required

tracker_bp = Blueprint("tracker", __name__)


@tracker_bp.get("/")
def view_landing_page():
    return render_template("registration/landing_page.html")


@tracker_bp.get("/tracker", endpoint="home")
@login_required
def view_media_list():
    return render_template("tracker/media_list.html")


@tracker_bp.route("/add", methods=["GET", "POST"])
def add_media():
    return render_template("tracker/add_media.html")


@tracker_bp.route("/<int:media_id>/edit", methods=["GET", "POST"])
def edit_media(media_id):
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
def delete_media(media_id):
    media = {"id": media_id, "title": "Sample"}
    return render_template("tracker/delete_media.html", media=media)
