# Generated by Django 4.2 on 2023-04-26 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0003_bookdelivery_order_number_alter_bookdelivery_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookdelivery',
            name='order_status',
            field=models.CharField(choices=[('P', 'Pending'), ('A', 'Assigned'), ('PU', 'PickedUp'), ('D', 'Delivered')], default='P', max_length=2),
        ),
    ]
