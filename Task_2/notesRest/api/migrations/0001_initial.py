# Generated by Django 5.1.3 on 2024-11-20 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('note', models.CharField(max_length=120)),
                ('description', models.TextField(max_length=1024)),
            ],
        ),
    ]