# Generated by Django 4.1.7 on 2023-04-05 16:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0004_alter_mensagem_sala"),
    ]

    operations = [
        migrations.AddField(
            model_name="sala",
            name="usuarios_permitidos",
            field=models.ManyToManyField(
                related_name="usuarios_permitidos", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
