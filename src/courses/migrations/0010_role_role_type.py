# Generated by Django 2.2.6 on 2020-01-20 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_auto_20200120_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='role_type',
            field=models.CharField(choices=[('teacher', 'teacher'), ('manager', 'manager')], default='teacher', max_length=25),
        ),
    ]
