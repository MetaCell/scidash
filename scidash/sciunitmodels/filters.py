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

    def by_model_url(self, queryset, name, value):
        model_name = None
        if "githubusercontent" not in value and "github" in value:
            string1 = value[0 : value.index("/blob/")]
            string2 = value[(value.index("/blob/") + 5) : len(value)]
            github_user = string1[(string1[0 : string1.rfind("/")].rfind("/") + 1) : string1.rfind("/")]
            repository = string1[(string1.rfind("/") + 1) : len(string1)]
            value = "https://raw.githubusercontent.com/" + github_user + "/" + repository + string2
        url = urlparse(value)
        model_name = os.path.basename(url.path)
        model_path = os.path.join(settings.DOWNLOADED_MODEL_DIR, model_name)

        helpers.download_and_save_model(model_path, value)

        model_classes = models.ModelClass.objects.filter(
            import_path__isnull=False
        )

        matching_classes = [
            kls.pk for kls in model_classes
            if helpers.check_capabilities(model_path, kls.import_path)
        ]

        return queryset.filter(pk__in=matching_classes)
