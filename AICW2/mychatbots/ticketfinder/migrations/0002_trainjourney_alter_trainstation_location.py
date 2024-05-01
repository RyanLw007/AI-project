# Generated by Django 5.0.4 on 2024-05-01 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketfinder', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainJourney',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rid', models.CharField(max_length=10, verbose_name='Train RTTI Identifier')),
                ('tpl', models.CharField(max_length=15, verbose_name='Location TIPOC')),
                ('pta', models.TimeField(blank=True, null=True, verbose_name='Planned Time of Arrival')),
                ('ptd', models.TimeField(blank=True, null=True, verbose_name='Planned Time of Departure')),
                ('wta', models.TimeField(blank=True, null=True, verbose_name='Working Time of Arrival')),
                ('wtp', models.TimeField(blank=True, null=True, verbose_name='Working Time of Passing')),
                ('wtd', models.TimeField(blank=True, null=True, verbose_name='Working Time of Departure')),
                ('arr_et', models.TimeField(blank=True, null=True, verbose_name='Estimated Arrival Time')),
                ('dep_et', models.TimeField(blank=True, null=True, verbose_name='Estimated Departure Time')),
                ('arr_at', models.TimeField(blank=True, null=True, verbose_name='Actual Time of Arrival')),
                ('dep_at', models.TimeField(blank=True, null=True, verbose_name='Actual Time of Departure')),
                ('arr_wet', models.TimeField(blank=True, null=True, verbose_name='Working Estimated Arrival Time')),
                ('dep_wet', models.TimeField(blank=True, null=True, verbose_name='Working Estimated Departure Time')),
                ('pass_et', models.TimeField(blank=True, null=True, verbose_name='Estimated Passing Time')),
                ('pass_wet', models.TimeField(blank=True, null=True, verbose_name='Working Estimated Passing Time')),
                ('arr_removed', models.BooleanField(default=False, verbose_name='Arrival Time Replaced')),
                ('pass_removed', models.BooleanField(default=False, verbose_name='Passing Time Replaced')),
                ('cr_code', models.CharField(blank=True, max_length=10, null=True, verbose_name='Cancellation Reason Code')),
                ('lr_code', models.CharField(blank=True, max_length=10, null=True, verbose_name='Late Running Reason Code')),
            ],
        ),
        migrations.AlterField(
            model_name='trainstation',
            name='location',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
