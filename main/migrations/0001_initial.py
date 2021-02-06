# Generated by Django 3.0 on 2019-12-09 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerFace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cust_name', models.CharField(max_length=200)),
                ('cust_face', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='PostSimFace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postsim_name', models.CharField(max_length=200)),
                ('postsim_face', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='EyeBrowFace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eyebrow_name', models.CharField(max_length=200)),
                ('eyebrow_face', models.ImageField(upload_to='')),
            ],
        ),
    ]
