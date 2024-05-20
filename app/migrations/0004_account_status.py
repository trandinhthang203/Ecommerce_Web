# Generated by Django 5.0.6 on 2024-05-20 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_account_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='status',
            field=models.CharField(choices=[('admin', 'Admin'), ('user', 'User')], default='active', max_length=20),
        ),
    ]