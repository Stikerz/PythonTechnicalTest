from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout
from rest_framework import status

from bonds.models import Bond
from bonds.tests.support.helpers.sample_data import BONDS, USERS
from bonds.tests.support.assertions import assert_valid_schema


class BondViewTest(TestCase):
    def setUp(self):
        user_instance = User(**USERS[0])
        user_instance.set_password("gamora")
        user_instance.save()
        bond_instance = Bond(**BONDS[0])
        bond_instance.user = user_instance
        bond_instance.save()

    def login(self) -> bool:
        user_login = self.client.login(username=USERS[0]["username"], password="gamora")
        return user_login

    def test_create_bond(self):
        legal_name = 'Saudi Credit Bureau'
        user_login = self.login()
        self.assertTrue(user_login)
        response = self.client.post("/origin/bonds/", data=BONDS[1])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(Bond.objects.all()), 2)
        assert_valid_schema(response.json(), "bonds_schema.json")
        self.assertEqual(response.json()['legal_name'], legal_name)

    def test_create_invalid_bond(self):
        user_login = self.login()
        self.assertTrue(user_login)
        response = self.client.post("/origin/bonds/", data=BONDS[2])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_unique_isin_bond(self):
        user_login = self.login()
        self.assertTrue(user_login)
        response = self.client.post("/origin/bonds/", data=BONDS[0])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["isin"][0], "bond with this isin already exists."
        )

    def test_get_bond(self):
        legal_name = 'GS1 Germany GmbH'
        user_login = self.login()
        self.assertTrue(user_login)
        response = self.client.get("/origin/bonds/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        assert_valid_schema(response.json(), "bonds_schema.json")
        self.assertEqual(response.json()[0]['legal_name'], legal_name)

    def test_get_bonds_filter(self):
        user_login = self.login()
        self.assertTrue(user_login)
        legal_name = "Saudi Credit Bureau"
        response = self.client.post("/origin/bonds/", data=BONDS[1])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(f"/origin/bonds/?legal_name={legal_name}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['legal_name'], legal_name)
        assert_valid_schema(response.json(), "bonds_schema.json")

    @mock.patch("bonds.utils.services.requests.get", side_effect=ConnectionError)
    def test_get_lei_name_connection_err(self, mock_request):
        user_login = self.login()
        self.assertTrue(user_login)
        with self.assertRaises(Exception):
            self.client.post("/origin/bonds/", data=BONDS[1])

    @mock.patch("bonds.utils.services.requests.get", side_effect=Timeout)
    def test_get_lei_name_timeout(self, mock_request):
        user_login = self.login()
        self.assertTrue(user_login)
        with self.assertRaises(Exception):
            self.client.post("/origin/bonds/", data=BONDS[1])

    @mock.patch("bonds.utils.services.requests.get", side_effect=HTTPError)
    def test_get_lei_name_http_err(self, mock_request):
        user_login = self.login()
        self.assertTrue(user_login)
        with self.assertRaises(Exception):
            self.client.post("/origin/bonds/", data=BONDS[1])

    @mock.patch("bonds.utils.services.requests.get", side_effect=RequestException)
    def test_get_lei_name_req_err(self, mock_request):
        user_login = self.login()
        self.assertTrue(user_login)
        with self.assertRaises(Exception):
            self.client.post("/origin/bonds/", data=BONDS[1])
