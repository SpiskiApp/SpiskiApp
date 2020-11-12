from cage.models import Inmate, List, ListItem
from cage.serializers import InmateSerializer, ListSerializer, SearchResultSerializer
from django.db.models.query import Q
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView
from rest_framework.response import Response


class ListImportInmatesView(ListCreateAPIView):
    queryset = Inmate.objects.order_by("pk").all()

    def get_serializer(self, *args, **kwargs):
        kwargs.pop("many", None)

        return InmateSerializer(*args, many=True, **kwargs)


class ListImportView(CreateAPIView):
    queryset = List.objects.order_by("pk").all()
    serializer_class = ListSerializer


class SearchPeopleView(ListAPIView):
    serializer_class = SearchResultSerializer

    def list(self, request, *args, **kwargs):
        query_param = self.request.query_params["q"]

        inmates = Inmate.objects.filter(
            Q(first_name__icontains=query_param) | Q(last_name__icontains=query_param)
        ).order_by("pk")
        list_items = ListItem.objects.filter(
            Q(first_name__icontains=query_param) | Q(last_name__icontains=query_param)
        ).order_by("pk")
        inmates_serializer = self.get_serializer(inmates, many=True)
        list_items_serializer = self.get_serializer(list_items, many=True)

        return Response(inmates_serializer.data + list_items_serializer.data)
