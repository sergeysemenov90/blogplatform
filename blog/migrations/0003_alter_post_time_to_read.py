# Generated by Django 4.0 on 2021-12-10 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_post_changed_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='time_to_read',
            field=models.TimeField(blank=True, null=True),
        ),
    ]