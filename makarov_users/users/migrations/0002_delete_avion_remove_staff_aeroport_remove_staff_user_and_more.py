# Generated by Django 5.0.6 on 2024-06-12 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Avion',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='aeroport',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='user',
        ),
        migrations.RemoveField(
            model_name='vol',
            name='aeroport_arrivee',
        ),
        migrations.RemoveField(
            model_name='vol',
            name='aeroport_depart',
        ),
        migrations.DeleteModel(
            name='Reservation',
        ),
        migrations.DeleteModel(
            name='Staff',
        ),
        migrations.DeleteModel(
            name='Vol',
        ),
    ]
