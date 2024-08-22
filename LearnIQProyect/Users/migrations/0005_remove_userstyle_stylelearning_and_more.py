# Generated by Django 5.0.2 on 2024-08-22 06:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_learningstyles_actividades'),
        ('Users', '0004_userstyle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userstyle',
            name='stylelearning',
        ),
        migrations.AddField(
            model_name='userstyle',
            name='learningStyle',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='App.learningstyles'),
            preserve_default=False,
        ),
    ]
