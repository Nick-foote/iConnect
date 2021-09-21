from rest_framework import serializers


class URIBaseModelSerializer(serializers.ModelSerializer):
    """Base Serializer returning the URI of the object from the model's
    get_absolute_url field (if set up)"""
    uri = serializers.SerializerMethodField(read_only=True)

    def get_uri(self, obj):
        obj_url = obj.get_absolute_url()
        context = self.context.get('request')
        if context:
            return context.build_absolute_uri(obj_url)
        return None