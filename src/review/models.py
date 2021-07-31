from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Ticket(models.Model):
    title = models.CharField(
        verbose_name='Titre',
        max_length=128
    )
    description = models.TextField(
        max_length=2048,
        blank=True
    )
    user = models.ForeignKey(
        verbose_name='Auteur',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        blank=True,
        null=True
    )
    time_created = models.DateField(
        verbose_name='Date',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Ticket'
        ordering = ['user']

    def __str__(self):
        return self.title


class Review(models.Model):
    ticket = models.ForeignKey(
        verbose_name='Ticket',
        to=Ticket,
        on_delete=models.CASCADE
    )
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ]
    )
    user = models.ForeignKey(
        verbose_name='Auteur',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    headline = models.CharField(
        verbose_name='Titre',
        max_length=128
    )
    body = models.CharField(
        verbose_name='Description',
        max_length=8192,
        blank=True
    )
    time_created = models.DateField(
        verbose_name='Date',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Revue'
        ordering = ['user']


class UserFollows(models.Model):
    user = models.ForeignKey(
        verbose_name='Utilisateur',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following'
    )

    followed_user = models.ForeignKey(
        verbose_name='Utilisateur suivi',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followed_by'
    )

    class Meta:
        verbose_name = 'Abonnement'
        ordering = ['user']
        unique_together = ('user', 'followed_user')
