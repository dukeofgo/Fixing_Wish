# Generated by Django 3.1 on 2020-09-12 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('new_app', '0002_auto_20200912_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='wish',
            name='liker',
            field=models.ManyToManyField(related_name='wishes_liked', to='new_app.User'),
        ),
    ]
