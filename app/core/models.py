from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
     PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Cretes a new user and save to db"""
        if not email:
            raise ValueError('User must have an email address')
        normalized_email = self.normalize_email(email)
        user = self.model(email=normalized_email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Overrides the AbstractBaseUser supporting emails as username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # creates a new UserManager to manage this object
    objects = UserManager()
    # default user has an username, this custom uses email as username
    USERNAME_FIELD = 'email'
