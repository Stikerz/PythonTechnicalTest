from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.utils import json

from bonds.serializers import UserSerializer
from bonds.tests.support.helpers.sample_data import USERS


class UserViewTest(TestCase):
    def setUp(self):
        user_instance = User(**USERS[0])
        user_instance.set_password("gamora")
        user_instance.save()

    def login(self) -> bool:
        user_login = self.client.login(
            username=USERS[0]["username"], password="gamora"
        )
        return user_login

    def test_create_valid_user(self):
        user_login = self.login()
        self.assertTrue(user_login)
        response = self.client.post(
            "/origin/users/",
            data=json.dumps(USERS[1]),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_user(self):
        user_login = self.login()
        self.assertTrue(user_login)
        response = self.client.post(
            "/origin/users/",
            data=json.dumps(USERS[2]),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_list(self):
        user_login = self.login()
        self.assertTrue(user_login)
        response = self.client.get("/origin/users/")
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_detailed(self):
        user_login = self.login()
        self.assertTrue(user_login)
        response = self.client.get("/origin/users/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_user_detailed(self):
        user_login = self.login()
        self.assertTrue(user_login)
        response = self.client.get("/origin/users/6/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_user(self):
        user_login = self.login()
        self.assertTrue(user_login)
        response = self.client.put(
            "/origin/users/1/",
            data=json.dumps(USERS[1]),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invalid_data(self):
        user_login = self.login()
        self.assertTrue(user_login)
        response = self.client.put(
            "/origin/users/1/",
            data=json.dumps(USERS[2]),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_teacher(self):
        user_login = self.login()
        self.assertTrue(user_login)
        response = self.client.delete("/origin/users/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
