# Generated by Django 4.2.7 on 2023-11-25 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rent', '0012_alter_resource_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(default='9131852123', max_length=10),
        ),
    ]
