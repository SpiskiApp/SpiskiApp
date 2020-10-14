from rest_framework.generics import CreateAPIView, ListCreateAPIView

from cage.models import Inmate, ListItem, List, Prison
from cage.serializers import InmateSerializer, ListSerializer


class ListImportInmatesView(ListCreateAPIView):
    queryset = Inmate.objects.order_by("pk").all()

    def get_serializer(self, *args, **kwargs):
        kwargs.pop("many", None)

        return InmateSerializer(*args, many=True, **kwargs)


class ListImportView(CreateAPIView):
    queryset = List.objects.order_by("pk").all()
    serializer_class = ListSerializer
