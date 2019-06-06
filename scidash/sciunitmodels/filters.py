import os
import zipfile
from urllib.parse import urlparse
import json

from django.conf import settings
from django_filters import rest_framework as filters
import requests
import logging

import scidash.sciunitmodels.helpers as helpers
import scidash.sciunitmodels.models as models


db_logger = logging.getLogger('db')


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

    def filter_from_neuromldb(self, info, queryset, model_id):
        model_info = requests.get(info.get('api'))

        if model_info.status_code != 200:
            db_logger.error(f'Can\'t get model_info for url {info.get("api")}')
            return queryset.filter(pk__in=[])
        else:
            model_info = json.loads(model_info.text)

        root_file = model_info.get('model', {}).get('File_Name', None)

        if root_file is None:
            db_logger.error(f'Can\'t get model_info for url {info.get("api")}')
            return queryset.filter(pk__in=[])

        zip_url = info.get('zip')

        model_zip_path = os.path.join(
            settings.DOWNLOADED_MODEL_DIR, f'{model_id}.zip'
        )

        response = requests.get(zip_url, allow_redirects=True)

        if response.status_code == 404:
            db_logger.info(f'Model zip not found with id {model_id}')
            return queryset.filter(pk__in=[])

        with open(model_zip_path, 'wb') as f:
            f.write(response.content)

        model_path = os.path.join(
            settings.DOWNLOADED_MODEL_DIR, f'{model_id}'
        )

        zip_ref = zipfile.ZipFile(model_zip_path, 'r')
        zip_ref.extractall(model_path)
        zip_ref.close()

        model_path = os.path.join(model_path, root_file)

        model_classes = models.ModelClass.objects.filter(
            import_path__isnull=False
        )

        matching_classes = [
            kls.pk for kls in model_classes
            if helpers.check_capabilities(model_path, kls.import_path)
        ]

        return queryset.filter(pk__in=matching_classes)

    def by_model_url(self, queryset, name, value):
        processor = helpers.URLProcessor(value)
        url = processor.get_file_url()

        if not isinstance(url, dict):
            return self.filter_from_github(url, queryset)
        else:
            return self.filter_from_neuromldb(url, queryset, processor.model_id)
