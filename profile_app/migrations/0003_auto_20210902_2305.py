# Generated by Django 3.1.2 on 2021-09-02 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_app', '0002_auto_20210902_2245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='created_at',
        ),
        migrations.AddField(
            model_name='employee',
            name='designation',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
