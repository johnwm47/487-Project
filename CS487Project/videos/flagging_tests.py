from django.test import TestCase, TransactionTestCase
from models import Flag, Video
from django.contrib.auth.models import User
from django.db.models import Count

class VideoFlagTest(TestCase):
    
    def test_video_flag_login(self):
        r = self.client.get('/videos/video/1/flag/')
        self.assertEqual(r.status_code, 404)

    def test_video_flag_login_su(self):
        self.assertTrue(self.client.login(username='su', password='su'))
        r = self.client.get('/videos/video/1/flag/')
        self.assertEqual(r.status_code, 200)
        request = self.client.post('/videos/video/1/flag/', {'description': 'Test'})
        self.assertEqual(request.status_code, 200)

    def test_comment_flag_login(self):
        r = self.client.get('/videos/comment/1/flag/')
        self.assertEqual(r.status_code, 404)

    def test_comment_flag_login_su(self):
        self.assertTrue(self.client.login(username='su', password='su'))
        r = self.client.get('/videos/comment/1/flag/')
        self.assertEqual(r.status_code, 200)
        request = self.client.post('/videos/comment/1/flag/', {'description': 'Test'})
        self.assertEqual(request.status_code, 200)
