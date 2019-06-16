class GetOrCreateMixin():
    def create(self, validated_data):
        model = self.Meta.model

        instance, created = model.objects.get_or_create(**validated_data)

        return instance


class GetByKeyOrCreateMixin():
    def create(self, validated_data):
        model = self.Meta.model
        relations, reverse_relations = self._extract_relations(validated_data)

        self.update_or_create_direct_relations(
            validated_data,
            relations,
        )

        key = validated_data.get(self.key)

        if key != '':
            try:
                model_instance = model.objects.get(**{self.key: key})
                instance = super(GetByKeyOrCreateMixin,
                                 self).update(model_instance, validated_data)
            except model.DoesNotExist:
                instance = super(GetByKeyOrCreateMixin,
                                 self).create(validated_data)
        else:
            if not validated_data.get('id', False):
                instance = super(GetByKeyOrCreateMixin,
                                 self).create(validated_data)
            else:
                model_instance = model.objects.get(pk=validated_data.get('id'))
                instance = super(GetByKeyOrCreateMixin,
                                 self).update(model_instance, validated_data)

        self.update_or_create_reverse_relations(instance, reverse_relations)

        return instance
