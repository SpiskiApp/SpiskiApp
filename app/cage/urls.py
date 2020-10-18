from cage import views
from django.conf.urls import url

urlpatterns = (
    url("inmates/?", views.ListImportInmatesView.as_view(), name="inmates_list"),
    url("lists/?", views.ListImportView.as_view(), name="import_list"),
)
