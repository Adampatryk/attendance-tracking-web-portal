# Generated by Django 3.0.3 on 2020-04-09 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_auto_20200409_1905'),
        ('lectures', '0008_auto_20200328_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.UserTypeWrapper'),
        ),
    ]
