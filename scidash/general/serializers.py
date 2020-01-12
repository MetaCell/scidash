from rest_framework import serializers, fields

from scidash.general.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', )


class SerializerWritableMethodField(fields.ModelField):
    """
    A writable (ModelField base) SerializerMethodField that get its
    representation from calling a method on the parent serializer class. The
    method called will be of the form "get_{field_name}", and should take a
    single argument, which is the object being serialized.

    For example:

    class ExampleSerializer(self):
        class_name = SciDashSerializerWritableMethodField(
                model_field=TestClass()._meta.get_field('class_name'))

        def get_class_name(self, obj):
            return ...  # Calculate some data to return.
    """

    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        super(SerializerWritableMethodField, self).__init__(**kwargs)

    def bind(self, field_name, parent):
        # In order to enforce a consistent style, we error if a redundant
        # 'method_name' argument has been used. For example:
        # my_fld = serializer.SerializerMethodField(method_name='get_my_fld')
        default_method_name = 'get_{field_name}'.format(field_name=field_name)
        assert self.method_name != default_method_name, (
            "It is redundant to specify `%s` on SerializerMethodField '%s' in "
            "serializer '%s', because it is the same as the default method "
            "name. Remove the `method_name` argument." %
            (self.method_name, field_name, parent.__class__.__name__)
        )

        # The method name should default to `get_{field_name}`.
        if self.method_name is None:
            self.method_name = default_method_name

        super(SerializerWritableMethodField, self).bind(
            field_name, parent)

    def to_representation(self, value):
        method = getattr(self.parent, self.method_name)
        return method(value)
