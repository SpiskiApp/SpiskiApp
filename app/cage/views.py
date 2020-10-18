from cage.models import Inmate, List, ListItem, Prison
from cage.serializers import InmateSerializer, ListSerializer
from rest_framework.generics import CreateAPIView, ListCreateAPIView


class ListImportInmatesView(ListCreateAPIView):
    queryset = Inmate.objects.order_by("pk").all()

    def get_serializer(self, *args, **kwargs):
        kwargs.pop("many", None)

        return InmateSerializer(*args, many=True, **kwargs)


class ListImportView(CreateAPIView):
    queryset = List.objects.order_by("pk").all()
    serializer_class = ListSerializer
