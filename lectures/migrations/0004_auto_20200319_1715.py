# Generated by Django 3.0.3 on 2020-03-19 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lectures', '0003_auto_20200319_1640'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lecture',
            old_name='moduleCode',
            new_name='module',
        ),
    ]
