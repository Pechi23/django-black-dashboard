# Generated by Django 3.2.25 on 2024-04-16 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='played',
            field=models.BooleanField(default=False),
        ),
    ]