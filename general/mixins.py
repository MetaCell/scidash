

class GetByHashOrCreateMixin():

    def create(self, validated_data):
        model = self.Meta.model

        instance, created = model.objects.get_or_create(**validated_data)

        return instance
