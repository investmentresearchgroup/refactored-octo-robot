# Generated by Django 3.2.6 on 2021-09-18 05:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CountryIndex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Country Index',
                'verbose_name_plural': 'Country Indices',
                'unique_together': {('name',)},
            },
        ),
        migrations.CreateModel(
            name='TickerPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(blank=True, max_length=100)),
                ('date', models.DateField()),
                ('volume', models.DecimalField(decimal_places=5, default=0.0, max_digits=15)),
                ('change', models.DecimalField(decimal_places=5, default=0.0, max_digits=15)),
                ('price', models.DecimalField(decimal_places=5, default=0.0, max_digits=15)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'unique_together': {('ticker', 'date')},
            },
        ),
        migrations.CreateModel(
            name='Ticker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_index', models.CharField(blank=True, max_length=100)),
                ('sector', models.CharField(blank=True, max_length=100)),
                ('industry', models.CharField(blank=True, max_length=100)),
                ('name', models.CharField(max_length=10)),
                ('full_name', models.CharField(blank=True, max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'unique_together': {('country_index', 'sector', 'industry', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('country_index', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.countryindex')),
            ],
            options={
                'unique_together': {('country_index', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('country_index', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.countryindex')),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.sector')),
            ],
            options={
                'verbose_name_plural': 'Industries',
                'unique_together': {('country_index', 'sector', 'name')},
            },
        ),
        migrations.CreateModel(
            name='IndexPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('value', models.DecimalField(decimal_places=5, max_digits=15)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.countryindex')),
            ],
            options={
                'verbose_name_plural': 'Country Index Prices',
                'unique_together': {('name', 'date')},
            },
        ),
    ]
