from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from users.utils import Util


def upload_to(instance, filename):
    now = timezone.now()
    return f"avatar/{now:%Y%m%d}/{filename}"


class UserRoles(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'


class UserGender(models.TextChoices):
    male = 'male'
    female = 'female'


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email,
                    password=None, **extra_fields):

        if first_name is None:
            raise TypeError('Users should have a first_name')
        if last_name is None:
            raise TypeError('Users should have a last_name')
        if email is None:
            raise TypeError('Users should have a email')

        user = self.model(first_name=first_name, last_name=last_name,
                          email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, first_name, last_name, email, password=None,
                         **extra_fields):
        user = self.create_user(first_name, last_name, email, password,
                                **extra_fields)

        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(
        max_length=50, verbose_name='First name')
    last_name = models.CharField(
        max_length=50, verbose_name='Last name')

    avatar = models.ImageField(verbose_name='Avatar', upload_to=upload_to,
                               blank=True)
    gender = models.CharField(max_length=10, blank=True,
                              choices=UserGender.choices,
                              default=UserGender.male)

    email = models.EmailField(_('email address'), unique=True, db_index=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    created_at = models.DateTimeField(_('created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated'), auto_now=True)
    role = models.CharField(max_length=10, blank=True,
                            choices=UserRoles.choices, default=UserRoles.USER)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name')
    objects = UserManager()

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        if self.avatar:
            image_patch = str(self.avatar)
            Util.compress_image(image_patch)

    def __str__(self):
        return self.email

    @property
    def is_moderator(self):
        return self.role == UserRoles.MODERATOR
