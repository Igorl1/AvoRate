from src.domain.user import User


def test_create_user_structure():
    """Tests if we can create a user with the correct fields"""
    user = User(
        username="TestUser", email="test@test.com", password="hashed_password", id=1
    )

    assert user.username == "TestUser"
    assert user.email == "test@test.com"
    assert user.password == "hashed_password"
    assert user.id == 1


def test_user_flask_login_properties():
    """Tests the required properties that Flask-Login expects"""
    user = User(username="TestUser", email="test@test.com", password="pw")

    assert user.is_authenticated is True
    assert user.is_active is True
    assert user.is_anonymous is False


def test_user_get_id_returns_string():
    """Tests if get_id returns the ID as a string (Flask-Login requirement)"""
    user = User(username="Test", email="a@a.com", password="pw", id=123)

    result = user.get_id()

    assert isinstance(result, str)
    assert result == "123"


def test_user_id_is_optional():
    """Tests if we can create a user without an ID (before saving to the database)"""
    user = User(username="NoID", email="noid@test.com", password="pw")

    assert user.id is None
