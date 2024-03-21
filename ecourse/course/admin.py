from django.contrib import admin
from course.models import *
from django.utils.html import mark_safe
from ckeditor_uploader.widgets \
    import CKEditorUploadingWidget
from django import forms


class CourseForm(forms.ModelForm):
    descriptions = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Course
        fields = '__all__'


class LessonInlineAdmin(admin.StackedInline):
    model = Lessons
    fk_name = 'course'


# Register your models here.
class Course_admin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_date', 'updated_date', 'image', 'active']
    search_fields = ['name']
    list_filter = ['id', 'name']
    readonly_fields = ['avatar']
    form = CourseForm

    def avatar(self, course):
        if course.image:
            return mark_safe(f"<img width='200' src='/static/{course.image.name}' />")


admin.site.register(Catatory)
admin.site.register(Lessons)
admin.site.register(Tag)

admin.site.register(Course, Course_admin)
