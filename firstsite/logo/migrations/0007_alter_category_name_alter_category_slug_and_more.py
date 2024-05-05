# Generated by Django 4.2.1 on 2024-03-26 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logo', '0006_category_remove_scriptpost_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='scriptpost',
            name='cat_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='logo.category'),
        ),
    ]