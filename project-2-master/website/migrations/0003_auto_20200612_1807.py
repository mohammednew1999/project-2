# Generated by Django 3.0.3 on 2020-06-12 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20200612_0027'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='image',
        ),
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.BooleanField(default=False, null=True),
        ),
    ]