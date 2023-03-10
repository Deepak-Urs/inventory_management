# Generated by Django 4.1.5 on 2023-01-17 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mass_g', models.IntegerField()),
                ('product_name', models.CharField(max_length=255)),
                ('product_id', models.IntegerField()),
            ],
            options={
                'ordering': ('-product_id',),
            },
        ),
    ]
