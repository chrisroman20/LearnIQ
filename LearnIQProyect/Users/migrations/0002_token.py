# Generated by Django 5.0.2 on 2024-06-10 03:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('idToken', models.AutoField(primary_key=True, serialize=False)),
                ('token', models.CharField(blank=True, default=None, max_length=100)),
                ('tipoToken', models.CharField(blank=True, default=None, max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]