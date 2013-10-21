from django.test import TestCase
from videos.models import Video
from django.contrib.auth.models import User
from django.test.client import RequestFactory

from django.test import TestCase, TransactionTestCase
from models import Video
from django.db.models import Count

class UploadTest(TestCase):
        #fixtures = ['initial_data.json'] # create user accounts

        def test_login_redirect(self):
                # test redirect to login page for normal user
                self.assertTrue(self.client.login(username='nu', password='nu'))
                r = self.client.get('/videos/upload/')
                self.assertRedirects(r, '/accounts/login/?next=/videos/upload/')

        def test_upload(self):
                # test to make sure upload page works for uploader
                self.assertTrue(self.client.login(username='up', password='up'))
                r = self.client.get('/videos/upload/')
                self.assertEqual(r.status_code, 200)

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class SearchTest(TestCase):
	fixtures = ['test_data.json']

	def testSearchKeywordExists(self):		
		r = self.client.get('/videos/search/?query=test')
		self.assertEqual(r.status_code, 200)
                print type(r.context['results'])
                print type(Video.objects.filter(keywords__keyword='test'))
                print type(r.context['results'][1])
                print type(Video.objects.filter(keywords__keyword='test')[1])
		self.assertQuerysetEqual(r.context['results'], Video.objects.filter(keywords__keyword='test'))
		
	def testSearchKeywordDoesNotExist(self):
		r = self.client.get('/videos/search/?query=potato')
		self.assertEqual(r.status_code, 200)
                print type(r.context['results'])
                print type(Video.objects.filter(keywords__keyword='potato'))
		self.assertQuerysetEqual(r.context['results'], Video.objects.filter(keywords__keyword='potato'))

	def testSearchMultipleKeywords(self):
		r = self.client.get('/videos/search/?query=test+vid')
		self.assertEqual(r.status_code, 200)
                res = Video.objects.filter(keywords__keyword ='test') | Video.objects.filter(keywords__keyword = 'vid')
                sres = res.annotate(matches=Count('keywords')).order_by('-matches')
                print type(r.context['results'])
                print type(sres)
		self.assertQuerysetEqual(r.context['results'], sres)
