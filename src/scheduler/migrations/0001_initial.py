# Generated by Django 2.2.6 on 2020-01-20 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FailedStatement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statement', models.TextField()),
                ('error', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'failed statement',
            },
        ),
        migrations.CreateModel(
            name='ProcessedStatement',
            fields=[
                ('statement_id', models.CharField(max_length=40, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'processed statement',
            },
        ),
    ]
