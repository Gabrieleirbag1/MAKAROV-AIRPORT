# Generated by Django 5.0.6 on 2024-06-14 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vols', '0003_vol_numero_vol'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vol',
            old_name='numero_vol',
            new_name='numvol',
        ),
    ]
