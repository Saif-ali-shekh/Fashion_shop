# Generated by Django 5.0.6 on 2024-06-25 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_Models', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='designimage',
            old_name='product_obj',
            new_name='Design_obj',
        ),
    ]
