# Generated by Django 2.0.2 on 2018-07-10 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wines', '0039_auto_20180710_1249'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grape',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('url', models.URLField(blank=True, default='')),
            ],
        ),
        migrations.AddField(
            model_name='wine',
            name='grapes',
            field=models.ManyToManyField(blank=True, null=True, related_name='wines', to='wines.Grape'),
        ),
    ]
