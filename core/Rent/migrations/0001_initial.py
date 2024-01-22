# Generated by Django 4.2.7 on 2023-11-17 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource_name', models.CharField(max_length=100)),
                ('resource_description', models.TextField()),
                ('resource_image', models.ImageField(upload_to='resource')),
            ],
        ),
    ]
