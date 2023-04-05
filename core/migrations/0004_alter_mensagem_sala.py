# Generated by Django 4.1.7 on 2023-04-05 02:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_alter_mensagem_sala"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mensagem",
            name="sala",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="mensagens",
                to="core.sala",
            ),
        ),
    ]