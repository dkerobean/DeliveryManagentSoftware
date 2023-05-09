# Generated by Django 4.2 on 2023-05-06 18:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0016_alter_bookdelivery_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='id',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
