# Generated by Django 2.2.6 on 2019-12-17 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_inactivity_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='external_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='choice',
            name='external_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='external_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='external_id',
            field=models.IntegerField(),
        ),
    ]
