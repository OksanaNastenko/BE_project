import json
import time
from unittest import TestCase
from api.users_api import UsersAPI

class UsersTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.users_api = UsersAPI()

    def _load_create_user_data(self):
        with open("test_data/create_user.json") as f:
            return json.load(f)

    def _assert_root_schema(self, root):
        self.assertIsInstance(root, dict)
        self.assertIn("page", root)
        self.assertIn("per_page", root)
        self.assertIn("total", root)
        self.assertIn("total_pages", root)
        self.assertIn("data", root)

        self.assertIsInstance(root["page"], int)
        self.assertIsInstance(root["per_page"], int)
        self.assertIsInstance(root["total"], int)
        self.assertIsInstance(root["total_pages"], int)
        self.assertIsInstance(root["data"], list)

    def _assert_user_schema(self, user):
        self.assertIsInstance(user, dict)
        self.assertIn("id", user)
        self.assertIn("email", user)
        self.assertIn("first_name", user)
        self.assertIn("last_name", user)
        self.assertIn("avatar", user)

        self.assertIsInstance(user["id"], int)
        self.assertIsInstance(user["email"], str)
        self.assertIsInstance(user["first_name"], str)
        self.assertIsInstance(user["last_name"], str)
        self.assertIsInstance(user["avatar"], (str, type(None)))

    def _assert_create_user_schema(self, user):
        self.assertIsInstance(user, dict)
        self.assertIn("id", user)
        self.assertIn("createdAt", user)

        self.assertIsInstance(user["id"], str)
        self.assertIsInstance(user["createdAt"], str)

    def test_get_users_has_correct_total(self):
        result = self.users_api.get_users()
        self.assertGreater(result["total"], 0)
        self.assertLessEqual(len(result["data"]), result["total"])

    def test_get_users_contains_pagination_schema(self):
        result = self.users_api.get_users()
        self._assert_root_schema(result)

    def test_get_users_contains_user_matching_schema(self):
        result = self.users_api.get_users()
        self.assertGreater(len(result["data"]), 0)
        self._assert_user_schema(result["data"][0])

    def test_post_user_creates_user_successfully(self):
        payload = self._load_create_user_data()
        result = self.users_api.post_user(payload)

        self.assertEqual(result["name"], payload["name"])
        self.assertEqual(result["job"], payload["job"])

        self._assert_create_user_schema(result)

    def test_post_user_response_time_is_under_limit(self):
        payload = self._load_create_user_data()
        limit_ms = 100

        start = time.time()
        self.users_api.post_user(payload)
        end = time.time()

        response_time_ms = (end - start) * 1000

        self.assertLess(response_time_ms, limit_ms)

