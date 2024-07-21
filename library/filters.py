from django.core import exceptions
from django.db.models import QuerySet

class SimpleGenericFilter():
    """ A simple generic filter mixin for Django Rest Framework ViewSets.
    This mixin is used to apply filters to the queryset based on query parameters. 
    """
    def apply_filters(self, default_queryset) -> QuerySet:
        """ Apply filters to the queryset based on query parameters. 
        Used in the get_queryset method of a ViewSet.
        
        Example:
        ```
        class BookViewSet(ModelViewSet, SimpleGenericFilter):
            queryset = Book.objects.all()
            serializer_class = BookSerializer

            def get_queryset(self):
                queryset = super(BookViewSet, self).get_queryset()
                return self.apply_filters(queryset)
        ```

        :param default_queryset: The default queryset to apply filters to.
        :type default_queryset: QuerySet
        :raises exceptions.BadRequest: If an invalid query parameter is provided.
        :return: The filtered queryset.
        :rtype: QuerySet
        """
        queryset = default_queryset
        for key, value in self.request.query_params.items():
            query_param = { key: value }
            try:
                queryset = queryset.filter(**query_param)
            except exceptions.FieldError:
                raise exceptions.BadRequest(f"Invalid query parameter: {key}")
        
        return queryset
     