from typing import Optional
from django.contrib.auth.models import User
import pytest

@pytest.fixture
def user_factory():
    """Factory for creating User instances."""
    def create_user(
        username: str,
        password: Optional[str] = None,
        first_name: Optional[str] = "first name",
        last_name: Optional[str] = "last name",
        email: Optional[str] = "foo@bar.com",
        is_staff: str = False,
        is_superuser: str = False,
        is_active: str = True,
    ) -> User:
        """Create a user with the given parameters."""
        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
        )
        if password:
            user.set_password(password)
        user.save()
        return user
    return create_user