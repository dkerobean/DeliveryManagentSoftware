# Generated by Django 4.2 on 2023-05-04 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0014_rider_bookdelivery_rider'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookdelivery',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='bookdelivery',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]