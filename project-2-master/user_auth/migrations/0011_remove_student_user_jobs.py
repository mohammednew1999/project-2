# Generated by Django 3.0.3 on 2020-06-12 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0010_student_user_jobs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student_user',
            name='jobs',
        ),
    ]
