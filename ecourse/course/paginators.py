from rest_framework import pagination


class Course_page(pagination.PageNumberPagination):
    page_size = 1

class CommentPaginator(pagination.PageNumberPagination):
    page_size = 2