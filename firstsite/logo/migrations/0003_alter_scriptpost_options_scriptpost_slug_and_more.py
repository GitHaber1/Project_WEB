# Generated by Django 4.2.1 on 2024-03-23 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logo', '0002_scriptpost_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scriptpost',
            options={'ordering': ['-time_create']},
        ),
        migrations.AddField(
            model_name='scriptpost',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=255),
        ),
        migrations.AddIndex(
            model_name='scriptpost',
            index=models.Index(fields=['-time_create'], name='logo_script_time_cr_e42343_idx'),
        ),
    ]
