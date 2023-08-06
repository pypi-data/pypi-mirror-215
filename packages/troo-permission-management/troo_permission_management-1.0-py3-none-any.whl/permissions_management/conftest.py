import pytest
from django.contrib.auth.models import User

from permissions_management.factories import UserFactory


@pytest.fixture(scope="function")
def user(db) -> User:
    return UserFactory()
