# Generated by Django 3.2.9 on 2021-12-09 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_payment_success'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='payment',
        ),
        migrations.AddField(
            model_name='payment',
            name='cart',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='course.cart'),
            preserve_default=False,
        ),
    ]