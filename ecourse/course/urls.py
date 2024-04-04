from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import routers
from course import views

r = routers.DefaultRouter()
r.register("catatory", viewset=views.Catatory_view, basename='catatory')
r.register("course", viewset=views.Course_view, basename='course')
r.register("lesson", viewset=views.Lesson_view, basename="lesson")
r.register("user", viewset=views.User_view, basename="user")
r.register("comment", viewset=views.Comment_View, basename="comment")
urlpatterns = [
    path('', include(r.urls)),
]
