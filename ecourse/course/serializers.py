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


class User_serializer(serializers.ModelSerializer):
    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'avatar']


class CommentSerializer(serializers.ModelSerializer):
    user = User_serializer()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_date', 'user']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class AuthenticatedLessonDetailsSerializer( LessonDetail_serializer):
    liked = serializers.SerializerMethodField()

    def get_liked(self, lesson):
        return lesson.like_set.filter(active=True).exists()

    class Meta:
        model =  LessonDetail_serializer.Meta.model
        fields =  LessonDetail_serializer.Meta.fields + ['liked']

