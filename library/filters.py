from django.core import exceptions
from django.db.models import QuerySet

class SimpleGenericFilter():
    def apply_filters(self, default_queryset) -> QuerySet:
        queryset = default_queryset
        for key, value in self.request.query_params.items():
            query_param = { key: value }
            try:
                queryset = queryset.filter(**query_param)
            except exceptions.FieldError:
                raise exceptions.BadRequest(f"Invalid query parameter: {key}")
        
        return queryset
     