# Generated by Django 2.1.3 on 2018-11-12 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='snipet_Demand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=4)),
                ('population', models.CharField(max_length=50)),
                ('substitute', models.CharField(max_length=50)),
                ('income', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='snipet_Harvest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=4)),
                ('districts', models.CharField(choices=[('Anuradapura', 'Anuradapura')], max_length=50)),
                ('season', models.CharField(choices=[('Yala-Season', 'Yala-Season'), ('Maha-Season', 'Maha-Season')], max_length=50)),
                ('area', models.CharField(max_length=50)),
                ('rainfall', models.CharField(max_length=50)),
            ],
        ),
    ]
