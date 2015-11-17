import unittest
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from app.views import sign_up

class Test_SignUp_View(unittest.TestCase):

    def test_signup_root_url_resolves_to_sign_up_view(self):
        found = resolve('/signup')
        self.assertEqual(found.func, sign_up)

    def test_signup_page_returns_correct_data(self):
        request = HttpRequest()
        response = sign_up(request)
        # self.assertEqual(response.content['title'], 'Welcome')
        self.assertIn(b'Welcome', response.content)
        # self.assertTrue(response.content.endswith(b'</html>') )
