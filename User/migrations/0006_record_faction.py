# Generated by Django 3.2.6 on 2022-01-29 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0005_alter_record_totalstats'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='Faction',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
