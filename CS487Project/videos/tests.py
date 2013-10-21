"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

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

class SearchTest(TestCase):
	fixtures = ['test_data.json']

	def testSearchKeywordExists(self):		
		r = self.client.get('/videos/search/?query=test')
		self.assertEqual(r.status_code, 200)
#                print type(r.context['results'])
 #               print type(Video.objects.filter(keywords__keyword='test'))
  #              print type(r.context['results'][1])
   #             print type(Video.objects.filter(keywords__keyword='test')[1])
		self.assertEqual(list(r.context['results']), list(Video.objects.filter(keywords__keyword='test')))
		
	def testSearchKeywordDoesNotExist(self):
		r = self.client.get('/videos/search/?query=potato')
		self.assertEqual(r.status_code, 200)
    #            print type(r.context['results'])
     #           print type(Video.objects.filter(keywords__keyword='potato'))
		self.assertEqual(list(r.context['results']), [])

	def testSearchMultipleKeywords(self):
		r = self.client.get('/videos/search/?query=test+vid')
		self.assertEqual(r.status_code, 200)
                res = Video.objects.filter(keywords__keyword ='test') | Video.objects.filter(keywords__keyword = 'vid')
                sres = res.annotate(matches=Count('keywords')).order_by('-matches')
      #          print type(r.context['results'])
       #         print type(sres)
		self.assertEqual(list(r.context['results']), list(sres))

	def testSearchAuthor(self):
		r = self.client.get('/videos/search/?aquery=kristen')
		self.assertEqual(r.status_code, 200)
		self.assertEqual(list(r.context['results']), list(Video.objects.filter(authors__name='kristen')))

	def testSearchAuthorDoesNotExist(self):
		r = self.client.get('/videos/search/?aquery=steve')
		self.assertEqual(r.status_code, 200)
		self.assertEqual(list(r.context['results']), [])

	def testSearchJournal(self):
		r = self.client.get('/videos/search/?jquery=test+journal')
		self.assertEqual(r.status_code, 200)
		self.assertEqual(list(r.context['results']), list(Video.objects.filter(journal__name='test journal')))

	def testSearchJournalDoesNotExist(self):
		r = self.client.get('/videos/search/?jquery=potato')
		self.assertEqual(r.status_code, 200)
		self.assertEqual(list(r.context['results']), [])

	def testSearchKeywordAndJournal(self):
		r = self.client.get('/videos/search/?query=test&aquery=&jquery=test+journal')
		self.assertEqual(r.status_code, 200)
		self.assertEqual(list(r.context['results']), list(Video.objects.filter(keywords__keyword='test').filter(journal__name='test journal')))

	def testSearchKeywordAndJournalKeywordDoesNotExist(self):
		r = self.client.get('/videos/search/?query=potato&aquery=&jquery=test+journal')
		self.assertEqual(r.status_code, 200)
		self.assertEqual(list(r.context['results']), [])

	def testSearchKeywordAndJournalJournalDoesNotExist(self):
		r = self.client.get('/videos/search/?query=test&aquery=&jquery=science+journal')
		self.assertEqual(r.status_code, 200)
		self.assertEqual(list(r.context['results']), [])

	def testSearchKeywordAndJournalNeitherExist(self):
		r = self.client.get('/videos/search/?query=potato&aquery=&jquery=science+journal')
		self.assertEqual(r.status_code, 200)
		self.assertEqual(list(r.context['results']), [])

	def testSearchKeywordAndAuthor(self):
		r = self.client.get('/videos/search/?query=test&aquery=kristen&jquery=')
		self.assertEqual(r.status_code, 200)
		self.assertEqual(list(r.context['results']), list(Video.objects.filter(keywords__keyword='test').filter(authors__name='kristen')))

	def testSearchKeywordAndAuthorKeywordDoesNotExist(self):
		r = self.client.get('/videos/search/?query=potato&aquery=kristen&jquery=')
		self.assertEqual(r.status_code, 200)
		self.assertEqual(list(r.context['results']), [])

	def testSearchKeywordAndAuthorAuthorDoesNotExist(self):
		r = self.client.get('/videos/search/?query=test&aquery=steve&jquery=')
		self.assertEqual(r.status_code, 200)
		self.assertEqual(list(r.context['results']), [])

	def testSearchKeywordAndAuthorNeitherExist(self):
		r = self.client.get('/videos/search/?query=potato&aquery=steve&jquery=')
		self.assertEqual(r.status_code, 200)
		self.assertEqual(list(r.context['results']), [])

	def testSearchAuthorAndJournal(self):
		r = self.client.get('/videos/search/?query=&aquery=kristen&jquery=test+journal')
		self.assertEqual(r.status_code, 200)
		self.assertEqual(list(r.context['results']), list(Video.objects.filter(authors__name='kristen').filter(journal__name='test journal')))

	def testSearchAuthorAndJournalAuthorDoesNotExist(self):
		r = self.client.get('/videos/search/?query=&aquery=steve&jquery=test+journal')
		self.assertEqual(r.status_code, 200)
		self.assertEqual(list(r.context['results']), [])

	def testSearchAuthorAndJournalJournalDoesNotExist(self):
		r = self.client.get('/videos/search/?query=&aquery=kristen&jquery=science+journal')
		self.assertEqual(r.status_code, 200)
		self.assertEqual(list(r.context['results']), [])

	def testSearchAuthorAndJournalNeitherExist(self):
		r = self.client.get('/videos/search/?query=&aquery=steve&jquery=science+journal')
		self.assertEqual(r.status_code, 200)
		self.assertEqual(list(r.context['results']), [])

	def testSearchAll(self):
		r = self.client.get('/videos/search/?query=test&aquery=kristen&jquery=test+journal')
		self.assertEqual(r.status_code, 200)
		self.assertEqual(list(r.context['results']), list(Video.objects.filter(keywords__keyword='test').filter(authors__name='kristen').filter(journal__name='test journal')))

	def testSearchAllKeywordDoesNotExist(self):
		r = self.client.get('/videos/search/?query=potato&aquery=kristen&jquery=test+journal')
		self.assertEqual(r.status_code, 200)
		self.assertEqual(list(r.context['results']), [])

	def testSearchAllAuthorDoesNotExist(self):
		r = self.client.get('/videos/search/?query=test&aquery=steve&jquery=test+journal')
		self.assertEqual(r.status_code, 200)
		self.assertEqual(list(r.context['results']), [])

	def testSearchAllJournalDoesNotExist(self):
		r = self.client.get('/videos/search/?query=test&aquery=kristen&jquery=science+journal')
		self.assertEqual(r.status_code, 200)
		self.assertEqual(list(r.context['results']), [])

	def testSearchAllKeywordAndAuthorDoesNotExist(self):
		r = self.client.get('/videos/search/?query=potato&aquery=steve&jquery=test+journal')
		self.assertEqual(r.status_code, 200)
		self.assertEqual(list(r.context['results']), [])

	def testSearchAllKeywordAndJournalDoesNotExist(self):
		r = self.client.get('/videos/search/?query=potato&aquery=kristen&jquery=science+journal')
		self.assertEqual(r.status_code, 200)
		self.assertEqual(list(r.context['results']), [])

	def testSearchAllAuthorAndJournalDoesNotExist(self):
		r = self.client.get('/videos/search/?query=test&aquery=steve&jquery=science+journal')
		self.assertEqual(r.status_code, 200)
		self.assertEqual(list(r.context['results']), [])

	def testSearchAllNoneExist(self):
		r = self.client.get('/videos/search/?query=potato&aquery=steve&jquery=science+journal')
		self.assertEqual(r.status_code, 200)
		self.assertEqual(list(r.context['results']), [])
