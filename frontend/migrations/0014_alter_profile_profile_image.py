# Generated by Django 4.2 on 2023-05-01 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0013_alter_bookdelivery_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='profiles/avatar.svg', null=True, upload_to='profiles'),
        ),
    ]