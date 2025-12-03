import pytest
from src.domain.media import Media, MediaRating
from unittest.mock import MagicMock
from src.use_cases.tracker_use_cases import DeleteMediaUseCase, GetMediaByUserUseCase


def test_create_media_valid_rating():
    """Tests if we can create media with a valid rating"""
    media = Media(title="Inception", user_id=1)
    media.rating = 10
    assert media.rating == 10
    assert media._rating == MediaRating.MASTERPIECE


def test_create_media_invalid_rating_too_high():
    """Tests if the system blocks rating higher than 10"""
    media = Media(title="Inception", user_id=1)

    with pytest.raises(ValueError):
        media.rating = 11


def test_create_media_invalid_rating_too_low():
    """ "Tests if the system blocks rating lower than 1"""
    media = Media(title="Bad Movie", user_id=1)
    with pytest.raises(ValueError):
        media.rating = 0


def test_media_string_representation():
    """Tests the __str__ method"""
    media = Media(title="Matrix", user_id=1)
    assert str(media) == "Matrix"


def test_rating_setter_valid_values():
    """Tests if the logic accepts valid ratings (limits 1 and 10 and a mid value 5)"""
    media = Media(title="Test", user_id=1)

    media.rating = 1
    assert media.rating == 1
    assert media._rating == MediaRating.TERRIBLE

    media.rating = 5
    assert media.rating == 5
    assert media._rating == MediaRating.AVERAGE

    media.rating = 10
    assert media.rating == 10
    assert media._rating == MediaRating.MASTERPIECE


def test_rating_setter_invalid_values():
    """Tests if the logic REJECTS invalid ratings (0, 11)"""
    media = Media(title="Test", user_id=1)

    with pytest.raises(ValueError, match="Rating must be between 1 and 10"):
        media.rating = 0

    with pytest.raises(ValueError, match="Rating must be between 1 and 10"):
        media.rating = 11


def test_rating_setter_none():
    """Tests if the logic accepts removing the rating (None)"""
    media = Media(title="Test", user_id=1)
    media.rating = 5
    assert media.rating == 5

    media.rating = None
    assert media.rating is None
    assert media._rating is None


def test_delete_media_success():
    """Tests if the use case returns True when the repository deletes successfully"""
    mock_repo = MagicMock()
    mock_repo.delete_media.return_value = True

    use_case = DeleteMediaUseCase(mock_repo)
    result = use_case.execute(media_id=10, user_id=1)

    assert result is True
    mock_repo.delete_media.assert_called_once_with(10, 1)


def test_delete_media_not_found():
    """Tests if the use case returns False when the media does not exist"""
    mock_repo = MagicMock()
    mock_repo.delete_media.return_value = False

    use_case = DeleteMediaUseCase(mock_repo)
    result = use_case.execute(media_id=999, user_id=1)

    assert result is False


def test_get_media_by_user_returns_list():
    """Tests if the use case returns the list that comes from the repository"""
    mock_repo = MagicMock()
    fake_list = [Media(title="Movie A", user_id=1), Media(title="Movie B", user_id=1)]
    mock_repo.get_media_by_user.return_value = fake_list

    use_case = GetMediaByUserUseCase(mock_repo)
    result = use_case.execute(user_id=1)

    assert len(result) == 2
    assert result[0].title == "Movie A"
    mock_repo.get_media_by_user.assert_called_once_with(1)


def test_get_media_by_user_empty():
    """Tests if the use case handles empty list well"""
    mock_repo = MagicMock()
    mock_repo.get_media_by_user.return_value = []

    use_case = GetMediaByUserUseCase(mock_repo)
    result = use_case.execute(user_id=1)

    assert result == []
