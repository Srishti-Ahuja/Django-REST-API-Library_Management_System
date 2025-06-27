from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

class BorrowlistPagination(PageNumberPagination):
    page_size = 4

class BookListPagination(LimitOffsetPagination):
    limit_query_param = 'size'
    offset_query_param = 'start'
    default_limit = 2
