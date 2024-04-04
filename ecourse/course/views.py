from django.shortcuts import render
from rest_framework import viewsets, generics, status, parsers, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from course.models import *
from course import serializers, paginators, perm


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

    def get_permissions(self):
        if self.action in ['add-comments', 'add_likes']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return serializers.AuthenticatedLessonDetailsSerializer

        return self.serializer_class

    @action(methods=['get'], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        comments = self.get_object().comment_set.select_related('user').order_by('-id')

        paginator = paginators.CommentPaginator()
        page = paginator.paginate_queryset(comments, request)
        if page is not None:
            serializer = serializers.CommentSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        return Response(serializers.CommentSerializer(comments, many=True).data)

    @action(methods=['post'], url_path='comments', detail=True)
    def add_comments(self, request, pk):
        id_user = request.user
        id_khoaHoa = self.get_object()
        c = id_khoaHoa.comment_set.create(content=request.data.get('content'),
                                          user=id_user)
        return Response(serializers.CommentSerializer(c).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], url_path='like', detail=True)
    def add_likes(self, request, pk):
        id_user = request.user
        id_khoaHoa = self.get_object()
        li, created = Like.objects.get_or_create(lesson=id_khoaHoa, user=id_user)
        if not created:
            li.active = not li.active
            li.save()
        return Response(serializers.AuthenticatedLessonDetailsSerializer(self.get_object()).data)


class User_view(viewsets.ModelViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.User_serializer
    parser_classes = [parsers.MultiPartParser, ]

    def get_permissions(self):
        if self.action in ['get_current_user']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get', 'patch'], url_path='current-user', detail=False)
    def get_current_user(self, request):
        user = request.user
        if request.method.__eq__('PATCH'):
            for k, v in request.data.items():
                setattr(user, k, v)
            user.save()
        return Response(serializers.User_serializer(user).data)


class Comment_View(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    # @action(methods=['delete'], url_path='comments', detail=False)
    # def del_comment(self,request):
    #     lay_id= Comment.objects.filter(user=request.user)
    #     del lay_id

    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [perm.CommentOwner]
