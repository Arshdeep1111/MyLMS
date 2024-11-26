# Generated by Django 3.2.9 on 2021-12-07 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_alter_course_thumbnail'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=25, unique=True)),
                ('txnid', models.IntegerField()),
                ('amount', models.IntegerField(default=0)),
                ('hash', models.CharField(max_length=25)),
                ('status', models.CharField(max_length=100)),
            ],
        ),
    ]