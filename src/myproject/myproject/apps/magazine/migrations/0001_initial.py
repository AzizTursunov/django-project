# Generated by Django 3.0.14 on 2022-10-29 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewsArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('body', models.TextField(verbose_name='Body')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('theme', models.CharField(max_length=20, verbose_name='Theme')),
            ],
            options={
                'verbose_name': 'News article',
            },
        ),
    ]