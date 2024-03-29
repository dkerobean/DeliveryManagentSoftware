# Generated by Django 4.2 on 2023-05-07 13:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0019_deliveryaction_deliverytype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryaction',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='deliverytype',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
