# Generated by Django 4.2.1 on 2024-03-31 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logo', '0009_author_scriptpost_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scriptpost',
            name='author',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ascript', to='logo.author'),
        ),
    ]
