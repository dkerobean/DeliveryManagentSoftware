# Generated by Django 4.2 on 2023-04-26 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookDelivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(blank=True, max_length=200, null=True)),
                ('item_type', models.CharField(blank=True, max_length=200, null=True)),
                ('pickup_location', models.CharField(blank=True, max_length=250, null=True)),
                ('destination_location', models.CharField(blank=True, max_length=250, null=True)),
                ('sender_contact', models.CharField(blank=True, max_length=200, null=True)),
                ('reciever_contact', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]
