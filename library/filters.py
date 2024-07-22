from django.core import exceptions
from rest_framework.request import Request
from django.db.models import QuerySet
from rest_framework.filters import BaseFilterBackend


class SimpleGenericFilter(BaseFilterBackend):
    """A simple generic filter backend for Django Rest Framework ViewSets."""

    def filter_queryset(self, request: Request, queryset: QuerySet, view) -> QuerySet:
        """Filters the queryset based on query parameters.
        It inherits from BaseFilterBackend and overrides the filter_queryset method
        to be used as a filter backend for Django Rest Framework ViewSets.

        :param request: The request object.
        :type request: Request
        :param queryset: The queryset to be filtered.
        :type queryset: QuerySet
        :param view: The view object.
        :type view: ModelViewSet
        :raises exceptions.BadRequest: If an invalid query parameter is provided.
        :return: The filtered queryset.
        :rtype: QuerySet
        """
        for key, value in request.query_params.items():
            query_param = {key: value}
            try:
                queryset = queryset.filter(**query_param)
            except exceptions.FieldError:
                raise exceptions.BadRequest(f"Invalid query parameter: {key}")

        return queryset
