# Generated by Django 5.0.6 on 2024-06-21 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_alter_reservations_user_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservations',
            name='user_ref',
            field=models.CharField(max_length=100),
        ),
    ]
