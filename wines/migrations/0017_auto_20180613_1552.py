# Generated by Django 2.0.2 on 2018-06-13 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wines', '0016_vendor_stopwords'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='stopwords',
            field=models.CharField(blank=True, default='', max_length=250),
        ),
    ]