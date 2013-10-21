from django.test import TestCase




class RegistrationTest(TestCase):
    def test_details(self):
        response = self.client.get('/accounts/register/')

        self.assertEqual(response.status_code, 200)

class LoginTest(TestCase):
    def test_details(self):
        response = self.client.get('/accounts/login/')

        self.assertEqual(response.status_code, 200)

class LogoutTest(TestCase):
    def test_details(self):
        response = self.client.get('/accounts/logout/')

        self.assertEqual(response.status_code, 200)
