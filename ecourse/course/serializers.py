from course.models import *
from rest_framework import serializers


class Catartory_serializers(serializers.ModelSerializer):
    class Meta:
        model = Catatory
        fields = '__all__'


class Item_serializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['image'] = instance.image.url

        return rep


class Course_serializers(Item_serializers):
    class Meta:
        model = Course
        fields = ['id', 'name', 'image']


class Lesson_serializers(Item_serializers):
    class Meta:
        model = Lessons
        fields = ['id', 'subject', 'created_date']


class Tag_serializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class LessonDetail_serializer(Lesson_serializers):
    tag = Tag_serializer(many=True)

    class Meta:
        model = Lesson_serializers.Meta.model
        fields = Lesson_serializers.Meta.fields + ['content', 'tag']


class User_serializer(Item_serializers):
    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'avatar']
