from django.test import SimpleTestCase

from django.urls import resolve, get_resolver


class EcommerceTests(SimpleTestCase):
#
        def test_url_configuration_loads(self):
            resolver = get_resolver()
            self.assertIsNotNone(resolver)
#
        def test_admin_url_resolves(self):
            match = resolve("/admin/")
            self.assertEqual(match.url_name, "index")