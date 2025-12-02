from src.infra.db.database import db
from src.domain.media import Media, MediaStatus, MediaType, MediaRating


class MediaModel(db.Model):
    __tablename__ = "media"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    media_type = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def to_entity(self):
        """
        Converts the Model (Database) to Entity (Domain)
        """
        return Media(
            id=self.id,
            title=self.title,
            user_id=self.user_id,
            status=MediaStatus(self.status) if self.status else None,
            _rating=MediaRating(self.rating) if self.rating else None,
            mediaType=MediaType(self.media_type) if self.media_type else None,
            description=self.description,
        )

    @staticmethod
    def from_entity(media_entity):
        """
        Converts Entity (Domain) to Model (Database)
        """
        return MediaModel(
            id=media_entity.id if hasattr(media_entity, "id") else None,
            title=media_entity.title,
            user_id=media_entity.user_id,
            status=media_entity.status.value if media_entity.status else None,
            rating=media_entity.rating,
            media_type=media_entity.mediaType.value if media_entity.mediaType else None,
            description=media_entity.description,
        )


class MediaRepository:
    def add_media(self, media: Media) -> Media:
        media_model = MediaModel.from_entity(media)
        db.session.add(media_model)
        db.session.commit()
        media.id = media_model.id
        return media

    def delete_media(self, media_id: int, user_id: int) -> bool:
        media_model = MediaModel.query.filter_by(id=media_id, user_id=user_id).first()
        if media_model:
            db.session.delete(media_model)
            db.session.commit()
            return True
        return False

    def get_media_by_id(self, media_id: int, user_id: int) -> Media:
        media_model = MediaModel.query.filter_by(id=media_id, user_id=user_id).first()
        if media_model:
            return media_model.to_entity()
        return None

    def get_media_by_user(self, user_id: int) -> list[Media]:
        media_models = MediaModel.query.filter_by(user_id=user_id).all()
        return [model.to_entity() for model in media_models]

    def update_media(self, media: Media) -> Media:
        media_model = MediaModel.query.filter_by(
            id=media.id, user_id=media.user_id
        ).first()
        if media_model:
            media_model.title = media.title
            media_model.status = media.status.value if media.status else None
            media_model.rating = media.rating
            media_model.media_type = media.mediaType.value if media.mediaType else None
            media_model.description = media.description
            db.session.commit()
            return media_model.to_entity()
        return None
