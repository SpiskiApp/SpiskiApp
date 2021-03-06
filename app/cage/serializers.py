from cage.models import Inmate, List, ListItem, Prison
from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    SerializerMethodField,
)


class InmateSerializer(ModelSerializer):
    class Meta:
        model = Inmate
        exclude = ["id"]


class ListItemSerializer(ModelSerializer):
    class Meta:
        model = ListItem
        fields = ["first_name", "last_name", "patronymic", "birth_date", "comments"]


class ListSerializer(ModelSerializer):
    items = ListItemSerializer(many=True, default=list)

    class Meta:
        model = List
        exclude = ["id"]

    def create(self, validated_data):
        list_items_data = validated_data.pop("items")
        list_ = List.objects.create(**validated_data)

        list_items = [ListItem(list=list_, **item) for item in list_items_data]
        ListItem.objects.bulk_create(list_items)

        return list_


class PrisonSerializer(ModelSerializer):
    class Meta:
        model = Prison
        fields = "__all__"


class SearchResultSerializer(Serializer):
    type = SerializerMethodField()
    object = SerializerMethodField()

    def get_type(self, obj) -> str:
        if isinstance(obj, Inmate):
            return "inmate"
        elif isinstance(obj, ListItem):
            return "list_item"
        return "unknown"

    def get_object(self, obj) -> dict:
        if isinstance(obj, Inmate):
            return InmateSerializer(obj).data
        elif isinstance(obj, ListItem):
            return ListItemSerializer(obj).data
        return {}
