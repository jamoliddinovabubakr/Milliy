# Generated by Django 5.0.4 on 2024-04-26 16:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Kafedra',
                'verbose_name_plural': 'Kafedralar',
            },
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Savolni baxolash',
                'verbose_name_plural': 'Savollarni baxolash',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Savol',
                'verbose_name_plural': 'Savollar',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('mark', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='question_app.mark')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question_app.question')),
            ],
            options={
                'verbose_name': 'Javob',
                'verbose_name_plural': 'Javoblar',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question_app.faculty')),
            ],
            options={
                'verbose_name': "O'qituvchi",
                'verbose_name_plural': "O'qituvchilar",
            },
        ),
    ]
