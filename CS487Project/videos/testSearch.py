from django.test import TestCase
from videos.models import Video
from django.contrib.auth.models import User
from django.test.client import RequestFactory

class SearchTest(TestCase):
	fixtures = ['test_data.json']

	def SearchKeywordExists(self):		
		r = self.client.get('/videos/search?query=test')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(r.context['results'], Video.objects.filter(title="testvid"))
		
	def SearchKeywordDoesNotExist(self):
		r = self.client.get('/videos/search?query=potato')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(r.context['results'], [])

	def SearchMultipleKeywords(self):
		r = self.client.get('/videos/search?query=test+vid')
