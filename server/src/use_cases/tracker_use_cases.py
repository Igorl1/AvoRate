from src.domain.media import Media
from src.infra.repositories.media_repository import MediaRepository


class AddMediaUseCase:
    def __init__(self, media_repository: MediaRepository):
        self.media_repository = media_repository

    def execute(self, media: Media) -> Media:
        return self.media_repository.add_media(media)


class DeleteMediaUseCase:
    def __init__(self, media_repository: MediaRepository):
        self.media_repository = media_repository

    def execute(self, media_id: int, user_id: int) -> bool:
        return self.media_repository.delete_media(media_id, user_id)


class GetMediaByUserUseCase:
    def __init__(self, media_repository: MediaRepository):
        self.media_repository = media_repository

    def execute(self, user_id: int) -> list[Media]:
        return self.media_repository.get_media_by_user(user_id)


class GetMediaByIdUseCase:
    def __init__(self, media_repository: MediaRepository):
        self.media_repository = media_repository

    def execute(self, media_id: int, user_id: int) -> Media:
        return self.media_repository.get_media_by_id(media_id, user_id)
