# Generated by Django 3.0.8 on 2020-08-18 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_auto_20200817_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='in_fav',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
