# Generated by Django 4.1.4 on 2023-01-20 23:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate_amount', models.IntegerField(blank=True, null=True)),
                ('rate_qnt', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('rate_id', models.IntegerField(blank=True, null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('member', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
