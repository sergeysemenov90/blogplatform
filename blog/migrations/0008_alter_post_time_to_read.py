# Generated by Django 4.0 on 2021-12-17 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_tag_blog_post_blog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='time_to_read',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
