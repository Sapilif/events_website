# Generated by Django 4.2 on 2023-06-14 13:13

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0029_alter_event_description_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Bilet',
            new_name='Ticket',
        ),
    ]
