# Generated by Django 2.2.6 on 2020-05-25 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hopital', '0009_auto_20200525_1607'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fee_patient',
            name='pat',
        ),
        migrations.AddField(
            model_name='fee_patient',
            name='appoint',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hopital.Appointment'),
        ),
    ]
