from unittest.mock import MagicMock
from src.use_cases.tracker_use_cases import (
    AddMediaUseCase,
    DeleteMediaUseCase,
    GetMediaByUserUseCase,
)
from src.domain.media import Media


def test_add_media_success():
    mock_repo = MagicMock()

    media_input = Media(title="Barbie", user_id=99)

    media_with_id = Media(title="Barbie", user_id=99, id=500)
    mock_repo.add_media.return_value = media_with_id

    use_case = AddMediaUseCase(mock_repo)
    result = use_case.execute(media_input)

    assert result.id == 500
    assert result.title == "Barbie"

    mock_repo.add_media.assert_called_once_with(media_input)


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
