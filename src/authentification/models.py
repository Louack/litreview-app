from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.text import slugify


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password):
        if not username:
            raise ValueError("Vous devez rentrer un nom d'utilisateur valide.")
        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password):
        superuser = self.create_user(
            username=username,
            password=password,
        )
        superuser.is_staff = True
        superuser.is_admin = True
        superuser.save()
        return superuser


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'Utilisateur'

    username = models.CharField(
        verbose_name="Nom d'utilisateur",
        max_length=30,
        unique=True,
        blank=False
    )

    slug = models.SlugField(
        blank=True,
        unique=True,
        editable=False
    )

    password = models.CharField(
        verbose_name='Mot de passe',
        max_length=128,
    )
    last_login = models.DateTimeField(
        verbose_name="Dernière connexion",
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_unique_slug(self):
        count = 0
        for user in CustomUser.objects.all():
            if user != self:
                if slugify(user.username) == slugify(self.username):
                    count += 1
        string = str(self.username) + '-' + str(count + 1)
        slug = slugify(string)
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug()
        super().save(*args, **kwargs)
