# Generated by Django 3.0.3 on 2020-03-19 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lectures', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('professorId', models.IntegerField()),
                ('moduleCode', models.IntegerField()),
                ('academicYearStart', models.DateField()),
                ('active', models.BooleanField()),
            ],
        ),
        migrations.RemoveField(
            model_name='lecture',
            name='classId',
        ),
        migrations.AddField(
            model_name='lecture',
            name='moduleCode',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='lectures.Module'),
            preserve_default=False,
        ),
    ]
