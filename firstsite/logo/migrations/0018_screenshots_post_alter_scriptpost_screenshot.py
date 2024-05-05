# Generated by Django 4.2.1 on 2024-05-05 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logo', '0017_screenshots_remove_scriptpost_screenshot_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='screenshots',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='logo.scriptpost'),
        ),
        migrations.AlterField(
            model_name='scriptpost',
            name='screenshot',
            field=models.ManyToManyField(blank=True, null=True, to='logo.screenshots', verbose_name='Скриншоты'),
        ),
    ]
