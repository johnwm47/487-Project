from django.test import TestCase, TransactionTestCase
from models import Video

class RegistrationTest(TestCase):
    fixtures = ['test_data.json']

    def test_uploader(self):
         self.assertTrue(self.client.login(username='su', password='su'))
         r = self.client.get('/videos/upload/')
         self.assertEqual(r.status_code, 200)

    def test_user(self):
         self.assertTrue(self.client.login(username='nu', password='nu'))
         r1 = self.client.get('/videos/upload/')
         self.assertEqual(r1.status_code, 302)

