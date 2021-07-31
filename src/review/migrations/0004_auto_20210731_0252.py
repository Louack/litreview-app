# Generated by Django 3.2.5 on 2021-07-31 00:52

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('review', '0003_alter_ticket_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticket',
            options={'ordering': ['user'], 'verbose_name': 'Ticket'},
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(max_length=1024, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(0)])),
                ('headline', models.CharField(max_length=128, verbose_name='Titre')),
                ('body', models.CharField(blank=True, max_length=8192, verbose_name='Description')),
                ('time_created', models.DateField(auto_now_add=True, verbose_name='Date')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='review.ticket', verbose_name='Ticket')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Auteur')),
            ],
            options={
                'verbose_name': 'Revue',
                'ordering': ['user'],
            },
        ),
        migrations.CreateModel(
            name='UserFollows',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followed_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_by', to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur suivi')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
            options={
                'verbose_name': 'Abonnement',
                'ordering': ['user'],
                'unique_together': {('user', 'followed_user')},
            },
        ),
    ]
