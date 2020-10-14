from rest_framework.serializers import ModelSerializer

from cage.models import Inmate, List, ListItem, Prison


class InmateSerializer(ModelSerializer):
    class Meta:
        model = Inmate
        exclude = ["id"]


class ListItemSerializer(ModelSerializer):
    class Meta:
        model = ListItem
        exclude = ["id", "list"]


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
