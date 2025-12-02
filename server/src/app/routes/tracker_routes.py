from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from src.domain.media import MediaStatus, MediaType, MediaRating, Media
from src.infra.repositories.media_repository import MediaRepository
from src.use_cases.tracker_use_cases import (
    AddMediaUseCase,
    DeleteMediaUseCase,
    GetMediaByIdUseCase,
    GetMediaByUserUseCase,
    UpdateMediaUseCase,
)

tracker_bp = Blueprint("tracker", __name__)

# Initialize repository and use cases
media_repo = MediaRepository()
add_media_uc = AddMediaUseCase(media_repo)
delete_media_uc = DeleteMediaUseCase(media_repo)
get_media_by_id_uc = GetMediaByIdUseCase(media_repo)
get_media_by_user_uc = GetMediaByUserUseCase(media_repo)
update_media_uc = UpdateMediaUseCase(media_repo)


@tracker_bp.get("/")
def view_landing_page():
    # Public landing page (before login)
    return render_template("registration/landing_page.html")


@tracker_bp.get("/tracker", endpoint="home")
@login_required
def view_media_list():
    media_list = get_media_by_user_uc.execute(current_user.id)

    # Calculate stats
    stats = {
        "total": len(media_list),
        "consuming": sum(1 for m in media_list if m.status == MediaStatus.CONSUMING),
        "completed": sum(1 for m in media_list if m.status == MediaStatus.COMPLETED),
        "planned": sum(1 for m in media_list if m.status == MediaStatus.PLANNED),
    }

    # Choices for filters
    status_choices = [(s.value, s.name.replace("_", " ").title()) for s in MediaStatus]
    type_choices = [(t.value, t.name.replace("_", " ").title()) for t in MediaType]

    return render_template(
        "tracker/media_list.html",
        items=media_list,
        stats=stats,
        status_choices=status_choices,
        media_types=type_choices,
    )


@tracker_bp.get("/explore")
@login_required
def explore():
    # "Explore" page after login, explaining features
    return render_template("tracker/explore.html")


@tracker_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_media():
    if request.method == "POST":
        title = request.form.get("title")
        status = request.form.get("status")
        rating = request.form.get("rating")
        media_type = request.form.get("media_type")
        description = request.form.get("description")

        media = Media(
            title=title,
            user_id=current_user.id,
            status=MediaStatus(status) if status else None,
            mediaType=MediaType(media_type) if media_type else None,
            description=description,
        )
        if rating:
            media.rating = int(rating)

        add_media_uc.execute(media)
        return redirect(url_for("tracker.home"))

    # Choices for template
    status_choices = [("", "Select Status")] + [
        (s.value, s.name.replace("_", " ").title()) for s in MediaStatus
    ]
    type_choices = [("", "Select Type")] + [
        (t.value, t.name.replace("_", " ").title()) for t in MediaType
    ]
    rating_choices = [("", "Select Rating")] + [
        (r.value, f"{r.value} - {r.name.replace('_', ' ').title()}")
        for r in MediaRating
    ]

    return render_template(
        "tracker/add_media.html",
        status_choices=status_choices,
        media_types=type_choices,
        rating_choices=rating_choices,
    )


@tracker_bp.route("/<int:media_id>/edit", methods=["GET", "POST"])
@login_required
def edit_media(media_id):
    media = get_media_by_id_uc.execute(media_id, current_user.id)
    if not media:
        return redirect(url_for("tracker.home"))

    if request.method == "POST":
        media.title = request.form.get("title")
        status_value = request.form.get("status")
        media.status = MediaStatus(status_value) if status_value else None
        type_value = request.form.get("media_type")
        media.mediaType = MediaType(type_value) if type_value else None
        rating_value = request.form.get("rating")
        if rating_value:
            media.rating = int(rating_value)
        else:
            media._rating = None
        media.description = request.form.get("description")

        update_media_uc.execute(media)
        return redirect(url_for("tracker.home"))

    status_choices = [("", "Select Status")] + [
        (s.value, s.name.replace("_", " ").title()) for s in MediaStatus
    ]
    type_choices = [("", "Select Type")] + [
        (t.value, t.name.replace("_", " ").title()) for t in MediaType
    ]
    rating_choices = [("", "Select Rating")] + [
        (r.value, f"{r.value} - {r.name.replace('_', ' ').title()}")
        for r in MediaRating
    ]

    return render_template(
        "tracker/edit_media.html",
        media=media,
        status_choices=status_choices,
        media_types=type_choices,
        rating_choices=rating_choices,
    )


@tracker_bp.route("/<int:media_id>/delete", methods=["GET", "POST"])
@login_required
def delete_media(media_id):
    media = get_media_by_id_uc.execute(media_id, current_user.id)
    if not media:
        return redirect(url_for("tracker.home"))  # or maybe error?

    if request.method == "POST":
        delete_media_uc.execute(media_id, current_user.id)
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
