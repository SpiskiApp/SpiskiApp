from typing import Callable, Optional, Sequence

from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group
from django.db import models
from django.urls import reverse
from django.utils.html import format_html

from auth.constants import UserGroup
from cage.models import List, ListItem


class VolunteerAdminSite(AdminSite):
    site_header = "Volunteer admin"

    def has_permission(self, request) -> bool:
        volunteer_group = Group.objects.get_by_natural_key(UserGroup.VOLUNTEER.value)
        return request.user.groups.filter(pk=volunteer_group.pk).exists()


def linkify(field_name: str) -> Callable[[models.Model], str]:
    """
    Converts a foreign key value into clickable links.

    If field_name is 'parent', link text will be str(obj.parent)
    Link will be admin url for the admin url for obj.parent.id:change

    per https://stackoverflow.com/a/53092940
    """

    def _linkify(obj: models.Model) -> str:
        linked_obj = getattr(obj, field_name)
        if linked_obj is None:
            return "-"

        app_label = linked_obj._meta.app_label
        model_name = linked_obj._meta.model_name
        view_name = f"admin:{app_label}_{model_name}_change"
        link_url = reverse(view_name, args=[linked_obj.pk])

        return format_html('<a href="{}">{}</a>', link_url, linked_obj)

    _linkify.short_description = field_name  # type: ignore
    return _linkify


class ListItemAdmin(admin.ModelAdmin):
    list_display = ("full_name", "birth_date")
    ordering = ("last_name", "first_name", "patronymic")

    def full_name(self, obj: ListItem) -> str:
        return f"{obj.last_name} {obj.first_name} {obj.patronymic}"

    def linked_list(self, obj: ListItem) -> str:
        return linkify("list")(obj)

    def get_readonly_fields(
        self, request, obj: Optional[models.Model] = None
    ) -> Sequence[str]:
        if obj:
            return "linked_list", "last_name", "first_name", "patronymic"
        else:
            return tuple()

    def get_fields(self, request, obj=None):
        if obj:
            return "linked_list", "last_name", "first_name", "patronymic"
        else:
            return "list", "last_name", "first_name", "patronymic", "birth_date"


class ListAdmin(admin.ModelAdmin):
    exclude = ("metadata",)
    field = ("origin", "prison", "date", "text")

    def get_readonly_fields(
        self, request, obj: Optional[models.Model] = None
    ) -> Sequence[str]:
        if obj:
            return "origin", "prison", "date", "text"
        else:
            return tuple()


volunteer_admin = VolunteerAdminSite(name="volunteer_admin")

volunteer_admin.register(ListItem, ListItemAdmin)
volunteer_admin.register(List, ListAdmin)
