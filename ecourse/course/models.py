from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField

# Create your models here.
class User(AbstractUser):
    pass


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
    image = CloudinaryField()
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
    image = CloudinaryField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
