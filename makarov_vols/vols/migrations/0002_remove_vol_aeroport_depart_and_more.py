# Generated by Django 5.0.6 on 2024-06-12 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vols', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vol',
            name='aeroport_depart',
        ),
        migrations.RemoveField(
            model_name='vol',
            name='aeroport_arrivee',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='aeroport',
        ),
        migrations.DeleteModel(
            name='Avion',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='user',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='vol',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.AddField(
            model_name='vol',
            name='aeroport_arrivee_ref',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vol',
            name='aeroport_depart_ref',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Aeroport',
        ),
        migrations.DeleteModel(
            name='Reservation',
        ),
        migrations.DeleteModel(
            name='Staff',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]