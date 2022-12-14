# Generated by Django 3.0.14 on 2022-11-10 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_auto_20221029_1436'),
        ('ideas', '0002_ideawithtranslatedfields_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ideawithtranslatedfields',
            name='raiting',
        ),
        migrations.AddField(
            model_name='ideawithtranslatedfields',
            name='rating',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, '★☆☆☆☆'), (2, '★★☆☆☆'), (3, '★★★☆☆'), (4, '★★★★☆'), (5, '★★★★★')], null=True, verbose_name='Rating'),
        ),
        migrations.AlterField(
            model_name='ideawithtranslatedfields',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='category_ideas', to='categories.Category', verbose_name='Categories'),
        ),
    ]
