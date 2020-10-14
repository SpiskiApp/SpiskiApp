from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from cage.models import List, ListItem, Prison
from .factories import PrisonFactory


class ImportListViewTests(TestCase):
    def test_import_empty_list_1(self):
        empty_list = {
            "text": "list test",
            "origin": "list origin",
        }

        response = self.client.post(
            reverse("import_list"), data=empty_list, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(List.objects.count(), 1)
        self.assertEqual(ListItem.objects.count(), 0)

        imported_list = List.objects.first()
        self.assertEqual(imported_list.text, empty_list["text"])
        self.assertEqual(imported_list.origin, empty_list["origin"])
        self.assertIsNone(imported_list.prison)
        self.assertIsNone(imported_list.date)

    def test_import_empty_list_2(self):
        empty_list = {
            "text": "list test",
            "origin": "list origin",
            "date": datetime.now().isoformat(),
            "metadata": {"key": "value"},
        }

        response = self.client.post(
            reverse("import_list"), data=empty_list, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(List.objects.count(), 1)
        self.assertEqual(ListItem.objects.count(), 0)

        imported_list = List.objects.first()
        self.assertEqual(imported_list.text, empty_list["text"])
        self.assertEqual(imported_list.origin, empty_list["origin"])
        self.assertEqual(
            imported_list.date.timestamp(),
            datetime.fromisoformat(empty_list["date"]).timestamp(),
        )
        self.assertEqual(imported_list.metadata, empty_list["metadata"])
        self.assertIsNone(imported_list.prison)

    def test_import_empty_list_with_wrong_prison(self):
        empty_list = {
            "text": "list test",
            "origin": "list origin",
            "prison": 1,
        }

        response = self.client.post(
            reverse("import_list"), data=empty_list, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_import_empty_list_with_prison(self):
        prison: Prison = PrisonFactory()
        empty_list = {
            "text": "list test",
            "origin": "list origin",
            "prison": prison.id,
        }

        response = self.client.post(
            reverse("import_list"), data=empty_list, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        imported_list = List.objects.first()
        self.assertEqual(imported_list.prison, prison)

    def test_import_multiple_lists_same_prison(self):
        prison: Prison = PrisonFactory()

        for i in range(3):
            empty_list = {
                "text": "list test",
                "origin": "list origin",
                "prison": prison.id,
            }

            response = self.client.post(
                reverse("import_list"), data=empty_list, content_type="application/json"
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(List.objects.count(), 3)
        for imported_list in List.objects.all():
            self.assertEqual(imported_list.prison, prison)

    def test_import_with_list_items(self):
        list_payload = {
            "text": "list from <place>",
            "origin": "list <origin>",
            "items": [],
        }
        for i in range(5):
            list_payload["items"].append(
                {
                    "first_name": f"FirstName({i})",
                    "last_name": f"LastName({i})",
                }
            )

        response = self.client.post(
            reverse("import_list"), data=list_payload, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(List.objects.count(), 1)
        self.assertEqual(ListItem.objects.count(), 5)
