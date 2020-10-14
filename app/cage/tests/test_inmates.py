from copy import copy
from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from cage.models import Inmate
from .factories import InmateFactory


class InmatesViewTests(TestCase):
    def test_get_all_inmates(self):
        for i in range(5):
            InmateFactory()

        response = self.client.get(reverse("inmates_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 5)

    def test_create_single_inmate(self):
        inmate_payload = {
            "last_name": "Last Name",
            "first_name": "First Name",
            "patronymic": "Patronymic",
            "birth_date": datetime.now().date().isoformat(),
        }
        response = self.client.post(
            reverse("inmates_list"),
            data=[inmate_payload],
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Inmate.objects.count(), 1)

        response = self.client.get(reverse("inmates_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        inmate_payload["metadata"] = {}
        self.assertEqual(response.json(), [inmate_payload])

        # with metadata
        new_inmate_payload = copy(inmate_payload)
        new_inmate_payload["metadata"] = {"key": "value", "value": "key"}
        response = self.client.post(
            reverse("inmates_list"),
            data=[new_inmate_payload],
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(reverse("inmates_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(), [inmate_payload, new_inmate_payload])

    def test_create_multiple_inmates(self):
        inmates_payload = [
            {
                "last_name": "Last Name",
                "first_name": "First Name",
                "patronymic": "Patronymic",
                "birth_date": datetime.now().date().isoformat(),
                "metadata": {},
            },
            {
                "last_name": "Last Name (2)",
                "first_name": "First Name (2)",
                "patronymic": "Patronymic (2)",
                "birth_date": (datetime.now().date() - timedelta(days=10)).isoformat(),
                "metadata": {"age": 42},
            },
        ]
        response = self.client.post(
            reverse("inmates_list"),
            data=inmates_payload,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(reverse("inmates_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), inmates_payload)
