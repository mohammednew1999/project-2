# Generated by Django 3.0.3 on 2020-06-14 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0015_auto_20200613_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company_user',
            name='company_logo',
            field=models.ImageField(blank=True, default='std_personal_images/default_personal_image.jpg', null=True, upload_to='companys_logo/'),
        ),
    ]
