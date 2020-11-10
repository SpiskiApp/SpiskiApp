from datetime import date, datetime
from typing import Any, Dict

from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized
from rest_framework import status

from .factories import InmateFactory, ListItemFactory


class SearchPeopleViewTests(TestCase):
    def gen_search_result(
        self, obj_type: str, first_name: str, last_name: str, birth_date: date
    ) -> dict:
        obj: Dict[str, Any] = {
            "type": obj_type,
            "object": {
                "first_name": first_name,
                "last_name": last_name,
                "patronymic": "",
                "birth_date": birth_date.isoformat(),
            },
        }
        if obj_type == "inmate":
            obj["object"]["metadata"] = {}
        else:
            obj["object"]["comments"] = None

        return obj

    def test_empty(self):
        response = self.client.get(reverse("search_people"), data={"q": "abc"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data, [])

    # Inmate

    @parameterized.expand(
        [
            ("inmate",),
            ("list_item",),
        ]
    )
    def test_no_results_found(self, obj_type: str):
        for i in range(5):
            if obj_type == "inmate":
                InmateFactory(
                    first_name=f"obj_{i}_first_name", last_name=f"obj_{i}_last_name"
                )
            else:
                ListItemFactory(
                    first_name=f"obj_{i}_first_name", last_name=f"obj_{i}_last_name"
                )

        response = self.client.get(reverse("search_people"), data={"q": "abc"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data, [])

    @parameterized.expand(
        [
            ("inmate",),
            ("list_item",),
        ]
    )
    def test_some_results_found(self, obj_type: str):
        n_objects = 5
        birth_date = datetime.now().date()

        for i in range(n_objects):
            if obj_type == "inmate":
                InmateFactory(
                    first_name=f"obj_{i}_first_name",
                    last_name=f"obj_{i}_last_name",
                    birth_date=birth_date,
                )
            else:
                ListItemFactory(
                    first_name=f"obj_{i}_first_name",
                    last_name=f"obj_{i}_last_name",
                    birth_date=birth_date,
                )

        response = self.client.get(reverse("search_people"), data={"q": "obj"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(
            data,
            [
                self.gen_search_result(
                    obj_type, f"obj_{i}_first_name", f"obj_{i}_last_name", birth_date
                )
                for i in range(n_objects)
            ],
        )

    @parameterized.expand(
        [
            ("inmate",),
            ("list_item",),
        ]
    )
    def test_ignore_birth_date(self, obj_type: str):
        n_objects = 5
        birth_date = date(2020, 10, 10)

        for i in range(n_objects):
            if obj_type == "inmate":
                InmateFactory(
                    first_name=f"obj_{i * 10}_first_name",
                    last_name=f"obj_{i * 10}_last_name",
                    birth_date=birth_date,
                )
            else:
                ListItemFactory(
                    first_name=f"obj_{i * 10}_first_name",
                    last_name=f"obj_{i * 10}_last_name",
                    birth_date=birth_date,
                )

        response = self.client.get(reverse("search_people"), data={"q": "20"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(
            data,
            [
                self.gen_search_result(
                    obj_type, "obj_20_first_name", "obj_20_last_name", birth_date
                )
            ],
        )

    @parameterized.expand(
        [
            ("inmate",),
            ("list_item",),
        ]
    )
    def test_by_first_name(self, obj_type: str):
        n_objects = 5
        birth_date = datetime.now().date()

        for i in range(n_objects):
            if obj_type == "inmate":
                InmateFactory(
                    first_name=f"obj_{i}_first_name",
                    last_name=f"obj_{i}_last_name",
                    birth_date=birth_date,
                )
            else:
                ListItemFactory(
                    first_name=f"obj_{i}_first_name",
                    last_name=f"obj_{i}_last_name",
                    birth_date=birth_date,
                )

        response = self.client.get(reverse("search_people"), data={"q": "1_first_name"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(
            data,
            [
                self.gen_search_result(
                    obj_type, "obj_1_first_name", "obj_1_last_name", birth_date
                )
            ],
        )

    @parameterized.expand(
        [
            ("inmate",),
            ("list_item",),
        ]
    )
    def test_by_last_name(self, obj_type: str):
        n_objects = 5
        birth_date = datetime.now().date()

        for i in range(n_objects):
            if obj_type == "inmate":
                InmateFactory(
                    first_name=f"obj_{i}_first_name",
                    last_name=f"obj_{i}_last_name",
                    birth_date=birth_date,
                )
            else:
                ListItemFactory(
                    first_name=f"obj_{i}_first_name",
                    last_name=f"obj_{i}_last_name",
                    birth_date=birth_date,
                )

        response = self.client.get(reverse("search_people"), data={"q": "1_first_name"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(
            data,
            [
                self.gen_search_result(
                    obj_type, "obj_1_first_name", "obj_1_last_name", birth_date
                )
            ],
        )

    def test_mixed(self):
        n_objects = 5
        birth_date = datetime.now().date()

        for i in range(n_objects):
            InmateFactory(
                first_name=f"inmate_obj_{i}_first_name",
                last_name=f"inmate_obj_{i}_last_name",
                birth_date=birth_date,
            )
            ListItemFactory(
                first_name=f"list_item_obj_{i}_first_name",
                last_name=f"list_item_obj_{i}_last_name",
                birth_date=birth_date,
            )

        response = self.client.get(reverse("search_people"), data={"q": "obj"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(
            data,
            [
                self.gen_search_result(
                    "inmate",
                    f"inmate_obj_{i}_first_name",
                    f"inmate_obj_{i}_last_name",
                    birth_date,
                )
                for i in range(n_objects)
            ]
            + [
                self.gen_search_result(
                    "list_item",
                    f"list_item_obj_{i}_first_name",
                    f"list_item_obj_{i}_last_name",
                    birth_date,
                )
                for i in range(n_objects)
            ],
        )
