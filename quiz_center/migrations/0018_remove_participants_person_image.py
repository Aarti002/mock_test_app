# Generated by Django 3.2.4 on 2021-11-17 04:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_center', '0017_auto_20210914_2041'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participants',
            name='person_image',
        ),
    ]