# Generated by Django 3.2.9 on 2021-12-12 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0014_alter_payment_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.CharField(max_length=10),
        ),
    ]
