"""
Contains tests for app.models.User class
"""
# pylint: disable=redefined-outer-name
from unittest import mock
import pytest
from app.models import User


@pytest.fixture
def user1():
    """
    User object
    """
    return User(
        username='john',
        email='john@example.com',
        about_me="Hello",
    )


def test_new_user(user1):
    """
    Test that user object contain correct values
    """
    assert user1.email == 'john@example.com'
    assert user1.username == "john"
    assert user1.about_me == 'Hello'
    assert str(user1) == "<User john, john@example.com>"


@mock.patch("app.models.current_app")
def test_password_hashing(_mock_current_app, user1):
    """
    Test setting password for user
    """
    user1.set_password('cat')
    assert user1.check_password('dog') is False
    assert user1.check_password('cat') is True


@mock.patch("app.models.current_app")
def test_avatar(_mock_current_app, user1):
    """
    Test creation of Gravatar URL
    """
    assert user1.avatar(128) == ('https://www.gravatar.com/avatar/'
                                 'd4c74594d841139328695756648b6bd6'
                                 '?d=retro&s=128')
