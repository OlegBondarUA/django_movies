# Generated by Django 4.1.1 on 2023-01-13 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kinozal', '0017_alter_reviews_options_delete_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='film',
            options={'ordering': ['id']},
        ),
    ]
