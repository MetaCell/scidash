from django_filters import rest_framework as filters

import scidash.sciunitmodels.models as models


class ModelInstanceFilter(filters.FilterSet):
    class_name = filters.CharFilter(
        name='model_class__class_name', lookup_expr='icontains'
    )

    tags = filters.CharFilter(name='tags__name', lookup_expr='icontains')

    name = filters.CharFilter(name='name', lookup_expr='icontains')

    timestamp_from = filters.IsoDateTimeFilter(
        name='timestamp', lookup_expr='gte'
    )

    timestamp_to = filters.IsoDateTimeFilter(
        name='timestamp', lookup_expr='lte'
    )

    class Meta:
        model = models.ModelInstance
        fields = [
            'name', 'class_name', 'tags', 'timestamp_from', 'timestamp_to'
        ]
