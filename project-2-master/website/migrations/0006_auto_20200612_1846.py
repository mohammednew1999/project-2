# Generated by Django 3.0.3 on 2020-06-12 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_job_employer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='num_of_views',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
