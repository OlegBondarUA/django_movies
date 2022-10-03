# Generated by Django 4.1.1 on 2022-10-03 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kinozal', '0005_film_base_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='films',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='kinozal.film'),
        ),
    ]
