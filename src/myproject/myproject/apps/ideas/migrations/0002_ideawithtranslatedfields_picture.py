# Generated by Django 3.0.14 on 2022-11-01 04:48

from django.db import migrations, models
import myproject.apps.ideas.models


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ideawithtranslatedfields',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=myproject.apps.ideas.models.upload_to, verbose_name='Picture'),
        ),
    ]