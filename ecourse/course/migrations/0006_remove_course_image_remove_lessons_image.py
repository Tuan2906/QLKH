# Generated by Django 5.0.3 on 2024-03-07 04:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_tag_alter_course_descriptions_lessons'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='image',
        ),
        migrations.RemoveField(
            model_name='lessons',
            name='image',
        ),
    ]
