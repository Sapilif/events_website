# Generated by Django 4.2 on 2023-05-27 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0021_bilet_sale_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.DeleteModel(
            name='MyClubUser',
        ),
        migrations.DeleteModel(
            name='Venue',
        ),
    ]
