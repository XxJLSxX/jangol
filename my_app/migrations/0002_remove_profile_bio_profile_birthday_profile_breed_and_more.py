# Generated by Django 5.1.4 on 2024-12-19 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='bio',
        ),
        migrations.AddField(
            model_name='profile',
            name='birthday',
            field=models.DateField(default='2000-01-01'),
        ),
        migrations.AddField(
            model_name='profile',
            name='breed',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(default='Unknown', max_length=10),
        ),
        migrations.AddField(
            model_name='profile',
            name='location',
            field=models.CharField(default='Unknown', max_length=200),
        ),
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.CharField(default='Unknown', max_length=100),
        ),
    ]
