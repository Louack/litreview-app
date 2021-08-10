from django.conf import settings
from django.core.exceptions import ValidationError
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
        null=True,
        upload_to='images/'
    )
    time_created = models.DateTimeField(
        verbose_name='Date',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Ticket'
        ordering = ['user']

    def __str__(self):
        return self.title

    def get_verbose_name(self):
        return self._meta.verbose_name

    def get_ticket_reviewers(self):
        reviews = [review for review in self.review_set.all()]
        reviewers = [review.user for review in reviews]
        return reviewers


class Review(models.Model):
    ticket = models.ForeignKey(
        verbose_name='Ticket',
        to=Ticket,
        on_delete=models.CASCADE,
    )
    rating = models.PositiveSmallIntegerField(
        verbose_name='Note',
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
        verbose_name='Commentaire',
        max_length=8192,
        blank=True
    )
    time_created = models.DateTimeField(
        verbose_name='Date',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Critique'
        ordering = ['user']

    def __str__(self):
        name = self.user.username
        ticket = self.ticket.title
        title = 'Revue de ' + name + ' à ' + ticket
        return title

    def get_verbose_name(self):
        return self._meta.verbose_name


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

    def save(self, *args, **kwargs):
        if self.user == self.followed_user:
            raise ValidationError("Un utilisateur ne peut pas s'abonner à lui-même")
        super().save(*args, **kwargs)
