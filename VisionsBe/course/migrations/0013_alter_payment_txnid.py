# Generated by Django 3.2.9 on 2021-12-12 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0012_auto_20211212_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='txnid',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
