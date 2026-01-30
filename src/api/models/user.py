from typing import Optional
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    """Manager for custom User model using email as username."""

    def create_user(
        self, 
        email: str, 
        password: Optional[str] = None, 
        full_name: str = ""
    ) -> "User":
        """
        Create and save a regular User with email, full_name, and password.
        
        Args:
            email (str): User's email (login).
            password (Optional[str]): User's raw password.
            full_name (str): Full name of the user.
        
        Returns:
            User: The created user instance.
        """
        if not email:
            raise ValueError("Email is required")
        
        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, 
        email: str, 
        password: str, 
        full_name: str = "Admin"
    ) -> "User":
        """
        Create and save a superuser.
        """
        user = self.create_user(email, password, full_name)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model that uses email instead of username.
    
    Attributes:
        email (str): Unique email of the user (used for login).
        full_name (str): Full name of the user.
        is_active (bool): Whether the user account is active.
        is_staff (bool): Whether the user can access the admin site.
        created_at (datetime): Timestamp of user creation.
    """
    email: str = models.EmailField(unique=True)
    full_name: str = models.CharField(max_length=255)

    is_active: bool = models.BooleanField(default=True)
    is_staff: bool = models.BooleanField(default=False)

    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    objects: UserManager = UserManager()

    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: list[str] = []

    def __str__(self) -> str:
        """Return string representation of user."""
        return self.email
