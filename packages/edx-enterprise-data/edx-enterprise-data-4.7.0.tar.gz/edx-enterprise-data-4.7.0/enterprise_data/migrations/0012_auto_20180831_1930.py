# Generated by Django 1.11.15 on 2018-08-31 19:30


import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise_data', '0011_enterpriseuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enterpriseenrollment',
            name='enterprise_user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='enterprise_data.EnterpriseUser', to_field='enterprise_user_id'),
        ),
        migrations.AlterField(
            model_name='enterpriseuser',
            name='enterprise_user_id',
            field=models.PositiveIntegerField(unique=True),
        ),
    ]
