# Generated by Django 4.1.4 on 2023-03-15 21:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0002_alter_points_full_name_alter_points_order_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='points',
            name='country',
        ),
        migrations.RemoveField(
            model_name='points',
            name='county',
        ),
        migrations.RemoveField(
            model_name='points',
            name='delivery_cost',
        ),
        migrations.RemoveField(
            model_name='points',
            name='email',
        ),
        migrations.RemoveField(
            model_name='points',
            name='full_name',
        ),
        migrations.RemoveField(
            model_name='points',
            name='grand_total',
        ),
        migrations.RemoveField(
            model_name='points',
            name='order_number',
        ),
        migrations.RemoveField(
            model_name='points',
            name='order_total',
        ),
        migrations.RemoveField(
            model_name='points',
            name='original_bag',
        ),
        migrations.RemoveField(
            model_name='points',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='points',
            name='postcode',
        ),
        migrations.RemoveField(
            model_name='points',
            name='street_address1',
        ),
        migrations.RemoveField(
            model_name='points',
            name='street_address2',
        ),
        migrations.RemoveField(
            model_name='points',
            name='town_or_city',
        ),
    ]
