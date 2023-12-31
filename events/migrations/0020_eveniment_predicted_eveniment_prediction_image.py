# Generated by Django 4.2 on 2023-05-27 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0019_eveniment_initial_tickets'),
    ]

    operations = [
        migrations.AddField(
            model_name='eveniment',
            name='predicted',
            field=models.BooleanField(default=False, verbose_name='Precictie vanzare'),
        ),
        migrations.AddField(
            model_name='eveniment',
            name='prediction_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
