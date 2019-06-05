import os
from urllib.parse import urlparse

from django.conf import settings
from django_filters import rest_framework as filters

import scidash.sciunitmodels.helpers as helpers
import scidash.sciunitmodels.models as models


class ModelInstanceFilter(filters.FilterSet):
    class_name = filters.CharFilter(
        name='model_class__class_name', lookup_expr='icontains'
    )

    tags = filters.CharFilter(name='tags__name', lookup_expr='icontains')

    name = filters.CharFilter(name='name', lookup_expr='icontains')

    owner = filters.CharFilter(name='owner__username', lookup_expr='icontains')

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


class ModelClassFilter(filters.FilterSet):
    model_url = filters.CharFilter(method='by_model_url')

    class Meta:
        model = models.ModelClass
        fields = [
            'model_url',
        ]

    def filter_from_github(self, url: str, queryset):
        url = urlparse(url)
        model_name = os.path.basename(url.path)
        model_path = os.path.join(
            settings.DOWNLOADED_MODEL_DIR, model_name
        )

        helpers.download_and_save_model(model_path, url)

        model_classes = models.ModelClass.objects.filter(
            import_path__isnull=False
        )

        matching_classes = [
            kls.pk for kls in model_classes
            if helpers.check_capabilities(model_path, kls.import_path)
        ]

        return queryset.filter(pk__in=matching_classes)

    def by_model_url(self, queryset, name, value):
        url = helpers.URLProcessor(value).get_file_url()

        if not isinstance(url, dict):
            return self.filter_from_github(url, queryset)
        else:
            return self.filter_from_nml(url, queryset)
