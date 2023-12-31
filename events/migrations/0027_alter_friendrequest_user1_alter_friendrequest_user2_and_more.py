# Generated by Django 4.2 on 2023-06-04 18:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0026_alter_bilet_sale_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendrequest',
            name='user1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user1_friendrequest', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='friendrequest',
            name='user2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2_friendrequest', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='prietenie',
            name='user1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user1_prietenie', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='prietenie',
            name='user2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2_prietenie', to=settings.AUTH_USER_MODEL),
        ),
    ]
