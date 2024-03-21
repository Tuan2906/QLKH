from django.shortcuts import render
from rest_framework import viewsets, generics, status, parsers
from rest_framework.decorators import action
from rest_framework.response import Response
from course.models import *
from course import serializers, paginators


# Create your views here.

class Catatory_view(viewsets.ModelViewSet, generics.ListAPIView, generics.CreateAPIView):
    queryset = Catatory.objects.all()
    serializer_class = serializers.Catartory_serializers


class Course_view(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active=True)
    serializer_class = serializers.Course_serializers
    pagination_class = paginators.Course_page

    def get_queryset(self):
        qr = self.queryset
        if self.action.__eq__('list'):
            q = self.request.query_params.get('q')
            if q:
                qr = qr.filter(name__icontains=q)
            cat = self.request.query_params.get('category_id')
            if cat:
                qr = qr.filter(category_id=cat)
        return qr

    @action(methods=['get'], url_path='lessons', detail=True)
    def get_lesson(self, request, pk):
        ls = self.get_object().lessons_set.filter(active=True)
        print(ls)
        q = request.query_params.get('q')
        if q:
            ls = ls.filter(subject__icontains=q)
        return Response(serializers.Lesson_serializers(ls, many=True).data, status=status.HTTP_200_OK)


class Lesson_view(viewsets.ModelViewSet, generics.RetrieveAPIView):
    queryset = Lessons.objects.prefetch_related('tag').filter(active=True)
    serializer_class = serializers.LessonDetail_serializer


class User_view(viewsets.ModelViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.User_serializer
    parser_classes = [parsers.MultiPartParser, ]
