# Generated by Django 4.2 on 2023-05-27 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_alter_bilet_eveniment_alter_bilet_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='funds',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]