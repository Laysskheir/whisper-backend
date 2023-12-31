# Generated by Django 4.2.7 on 2023-11-28 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name_plural': 'Products'},
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
                ('products', models.ManyToManyField(to='store.product')),
            ],
            options={
                'verbose_name_plural': 'Sizes',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
                ('products', models.ManyToManyField(to='store.product')),
            ],
            options={
                'verbose_name_plural': 'Colors',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='colors',
            field=models.ManyToManyField(to='store.color'),
        ),
        migrations.AddField(
            model_name='product',
            name='sizes',
            field=models.ManyToManyField(to='store.size'),
        ),
    ]
