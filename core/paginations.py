from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'per_page'
    max_page_size = 1000

    def get_page_number(self, request, paginator):
        page_number = request.query_params.get(self.page_query_param, 1)

        if page_number in self.last_page_strings:
            return paginator.num_pages

        # DRF already handles invalid page numbers, so no need to catch exceptions
        return super().get_page_number(request, paginator)

    def get_paginated_response(self, data):
        return Response({
            'pagination': {
                'items_count': self.page.paginator.count,
                'pages_count': self.page.paginator.num_pages,
                'current_page': self.page.number,
                'per_page': self.get_page_size(self.request),
            },
            'results': data,
        })
