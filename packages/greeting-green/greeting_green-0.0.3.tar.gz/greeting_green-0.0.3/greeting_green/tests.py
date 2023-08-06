from django.test import TestCase

from django.urls import reverse


class IndexViewTests(TestCase):

    def test_index(self):
        response = self.client.get(reverse("greeting_green:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello Warise!!")
        self.assertQuerySetEqual(response.context["Hello"], "Hello Warise!!")
