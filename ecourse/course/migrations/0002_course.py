# Generated by Django 5.0.3 on 2024-03-07 02:10
import django.db.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=100)),
                ('descriptions', models.TextField(null=True)),
                ('image', models.ImageField(upload_to='course/%y/%m')),
                ( 'category',  models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,to='course.Catatory'))
            ],
            options={
                'abstract': False,
            },
        ),
    ]