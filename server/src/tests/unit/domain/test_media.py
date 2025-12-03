import pytest
from src.domain.media import Media, MediaRating


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
