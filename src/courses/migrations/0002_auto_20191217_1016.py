# Generated by Django 2.2.6 on 2019-12-17 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20191211_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='external_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='name',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='choice',
            name='external_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='choice',
            name='name',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='question',
            name='external_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='name',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='external_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='name',
            field=models.CharField(max_length=256),
        ),
    ]
