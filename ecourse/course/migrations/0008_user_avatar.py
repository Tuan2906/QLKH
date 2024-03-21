# Generated by Django 5.0.3 on 2024-03-21 03:49

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_course_image_lessons_image_comment_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=cloudinary.models.CloudinaryField(max_length=255, null=True),
        ),
    ]
