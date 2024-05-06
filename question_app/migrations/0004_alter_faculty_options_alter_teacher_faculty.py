# Generated by Django 5.0.4 on 2024-04-27 08:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question_app', '0003_kafedra'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faculty',
            options={'verbose_name': 'Fakultet', 'verbose_name_plural': 'Fakultetlar'},
        ),
        migrations.AlterField(
            model_name='teacher',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question_app.kafedra'),
        ),
    ]