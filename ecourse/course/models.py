from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField


# Create your models here.
class User(AbstractUser):
    avatar = CloudinaryField(null=True)


class Catatory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class BaseMode(models.Model):
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Course(BaseMode):
    name = models.CharField(max_length=100)
    descriptions = RichTextField(null=True)
    image = CloudinaryField(null=True)
    category = models.ForeignKey(Catatory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Tag(BaseMode):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Lessons(BaseMode):
    subject = models.CharField(max_length=100)
    content = RichTextField(null=True)
    image = CloudinaryField(null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.subject


class Interaction(BaseMode):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user_id} - {self.lesson_id}'

    class Meta:
        abstract = True


class Comment(Interaction):
    content = models.CharField(max_length=255)

    def __str__(self):
        return self.content


class Like(Interaction):
    class Meta:
        unique_together = ('user', 'lesson')


class Rating(Interaction):
    rate = models.IntegerField

    class Meta:
        unique_together = ('user', 'lesson')
