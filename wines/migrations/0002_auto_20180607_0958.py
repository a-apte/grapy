# Generated by Django 2.0.2 on 2018-06-07 07:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wines', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('code_iso2', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('code_iso3', models.CharField(max_length=3)),
            ],
            options={
                'ordering': ['code_iso2'],
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='VendorWine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_code', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('quantity', models.PositiveSmallIntegerField(default=1)),
                ('url', models.URLField()),
                ('modified', models.DateTimeField(auto_now=True)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='vendors', to='wines.Vendor')),
            ],
        ),
        migrations.RemoveField(
            model_name='wine',
            name='modified',
        ),
        migrations.RemoveField(
            model_name='wine',
            name='price',
        ),
        migrations.RemoveField(
            model_name='wine',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='wine',
            name='url',
        ),
        migrations.RemoveField(
            model_name='wine',
            name='vendor_code',
        ),
        migrations.AddField(
            model_name='wine',
            name='name',
            field=models.CharField(default='', max_length=150, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='wine',
            name='aroma',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='wine',
            name='color',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='wine',
            name='contents',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='wine',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='wines', to='wines.Country'),
        ),
        migrations.AlterField(
            model_name='wine',
            name='region',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='wine',
            name='serving_temp',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='wine',
            name='vintage',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='wine',
            name='winery',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='wine',
            name='winetype',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='vendorwine',
            name='wine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='wines', to='wines.Wine'),
        ),
        migrations.AlterUniqueTogether(
            name='vendorwine',
            unique_together={('vendor', 'vendor_code')},
        ),
    ]