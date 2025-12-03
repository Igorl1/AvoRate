# tests/unit/use_cases/test_auth_use_cases.py
import pytest
from unittest.mock import MagicMock
from werkzeug.security import generate_password_hash
from src.use_cases.auth_use_cases import AuthUseCases
from src.domain.user import User


def test_signup_success():
    """Tests if signup works correctly with a new email"""
    mock_repo = MagicMock()

    mock_repo.get_user_by_email.return_value = None

    def side_effect_save(user):
        user.id = 1
        return user

    mock_repo.save_user.side_effect = side_effect_save

    auth_use_case = AuthUseCases(mock_repo)

    new_user = auth_use_case.signup("test@email.com", "Tester", "123456")

    assert new_user.email == "test@email.com"
    assert new_user.username == "Tester"
    assert new_user.id == 1

    assert new_user.password != "123456"

    mock_repo.save_user.assert_called_once()


def test_signup_duplicate_email_error():
    """Tests if the system blocks signup with duplicate email"""
    mock_repo = MagicMock()

    existing_user = User(username="Old", email="test@email.com", password="hash")
    mock_repo.get_user_by_email.return_value = existing_user

    auth_use_case = AuthUseCases(mock_repo)

    with pytest.raises(ValueError, match="Email already exists"):
        auth_use_case.signup("test@email.com", "New Guy", "123456")

    mock_repo.save_user.assert_not_called()


def test_login_success():
    """Tests if login works with the correct password"""
    mock_repo = MagicMock()

    password_real = "my_secret_password"
    password_hash = generate_password_hash(password_real)

    user_in_db = User(
        username="Tester", email="test@email.com", password=password_hash, id=55
    )

    mock_repo.get_user_by_email.return_value = user_in_db

    auth_use_case = AuthUseCases(mock_repo)

    result = auth_use_case.login("test@email.com", password_real)

    assert result is not None
    assert result.id == 55
    assert result.email == "test@email.com"


def test_login_wrong_password():
    """Tests if login fails with the wrong password"""
    mock_repo = MagicMock()

    password_real = "correct_password"
    password_hash = generate_password_hash(password_real)
    user_in_db = User(
        username="Tester", email="test@email.com", password=password_hash, id=55
    )

    mock_repo.get_user_by_email.return_value = user_in_db

    auth_use_case = AuthUseCases(mock_repo)

    result = auth_use_case.login("test@email.com", "wrong_password")

    assert result is None


def test_login_user_not_found():
    """Tests if login fails when the email does not exist"""
    mock_repo = MagicMock()
    mock_repo.get_user_by_email.return_value = None

    auth_use_case = AuthUseCases(mock_repo)

    result = auth_use_case.login("nonexistent@email.com", "123456")
    assert result is None
