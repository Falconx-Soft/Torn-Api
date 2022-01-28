# Generated by Django 3.2.6 on 2022-01-27 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_apiinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('level', models.IntegerField()),
                ('age', models.IntegerField()),
                ('lastAction', models.CharField(max_length=100)),
                ('updated', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='apiinfo',
            name='age',
        ),
        migrations.RemoveField(
            model_name='apiinfo',
            name='lastAction',
        ),
        migrations.RemoveField(
            model_name='apiinfo',
            name='level',
        ),
        migrations.RemoveField(
            model_name='apiinfo',
            name='name',
        ),
        migrations.RemoveField(
            model_name='apiinfo',
            name='status',
        ),
        migrations.RemoveField(
            model_name='apiinfo',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='apiinfo',
            name='userId',
        ),
    ]
