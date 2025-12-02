from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required

tracker_bp = Blueprint("tracker", __name__)


@tracker_bp.get("/")
def view_landing_page():
    # Public landing page (before login)
    return render_template("registration/landing_page.html")


@tracker_bp.get("/tracker", endpoint="home")
@login_required
def view_media_list():
    # Personal dashboard (where tracking features will be used)
    return render_template("tracker/media_list.html")


@tracker_bp.get("/explore")
@login_required
def explore():
    # "Explore" page after login, explaining features
    return render_template("tracker/explore.html")


@tracker_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_media():
    # Simple stub: future backend will save to database
    if request.method == "POST":
        # Here in the future: create item, associate with user etc.
        return redirect(url_for("tracker.home"))

    return render_template("tracker/add_media.html")


@tracker_bp.get("/<int:media_id>/edit")
@login_required
def edit_media(media_id):
    # Example stub for editing
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
        # Future: actually delete and redirect
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
