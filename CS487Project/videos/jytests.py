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

    def test_register1(self):
        request = self.client.post('/accounts/register/', {'username': 'test1', 'email': 'test1@hawk.iit.edu', 'password1': '123456', 'password2': '123456'})
        self.assertTrue(self.client.login(username='test1', password='123456'))
        r2 = self.client.get('/videos/upload/')
        self.assertEqual(r2.status_code, 200)
        r2 = self.client.get('/videos/search/')
        self.assertEqual(r2.status_code, 200)

    def test_register2(self):
        request = self.client.post('/accounts/register/', {'username': 'test2', 'email': 'test2@hawk.iit', 'password1': '123456', 'password2': '123456'})
        self.assertTrue(self.client.login(username='test2', password='123456'))
        r3 = self.client.get('/videos/upload/')
        self.assertEqual(r3.status_code, 302)
        r3 = self.client.get('/videos/search/')
        self.assertEqual(r3.status_code, 200)
