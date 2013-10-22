"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

from django.test import TestCase, TransactionTestCase
from models import Video, Journal, Keyword, Author
from django.contrib.auth.models import User
from django.db.models import Count

class UploadTest(TestCase):
        fixtures = ['test_data.json'] # create user accounts

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

                f = open('../soccer.mp4')
                r2 = self.client.post('/videos/upload/', {'title':'Test', 'description':'Testd', 'url':'www.google.com', 'authors':(1), 'keywords':(1, 2), 'journal': 1, 'video': f})
                f.close()

                self.assertEqual(r2.templates[0].name, 'videos/upload_success.html')
                o = Video.objects.get(title='Test')
                self.assertEqual(o.description, 'Testd')
                self.assertEqual(o.url, 'http://www.google.com/')
                self.assertEqual(o.viewCount, 0)
                self.assertEqual(o.journal, Journal.objects.get(pk=1))

class SearchTest(TestCase):
	fixtures = ['test_data.json']

	def testSearchKeywordExists(self):		
		r = self.client.get('/videos/search/?query=test')
		self.assertEqual(r.status_code, 200)
		self.assertEqual(list(r.context['results']), list(Video.objects.filter(keywords__keyword='test')))
		
	def testSearchKeywordDoesNotExist(self):
		r = self.client.get('/videos/search/?query=potato')
		self.assertEqual(r.status_code, 200)
		self.assertEqual(list(r.context['results']), [])

	def testSearchMultipleKeywords(self):
		r = self.client.get('/videos/search/?query=test+vid')
		self.assertEqual(r.status_code, 200)
                res = Video.objects.filter(keywords__keyword ='test') | Video.objects.filter(keywords__keyword = 'vid')
                sres = res.annotate(matches=Count('keywords')).order_by('-matches')
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

class VideoTest(TestCase):
        fixtures = ['test_data'] # a default set of videos

        def testViewVideoExists(self):
		r = self.client.get("/videos/view/1/")
		self.assertEqual(r.status_code, 200)
		self.assertEqual(r.context['video'], Video.objects.get(pk=1))

        def testViewVideoNotExists(self):
		r = self.client.get("/videos/view/5/")
		self.assertEqual(r.status_code, 404)

        def testViewIncremented(self):
		v1 = Video.objects.get(pk=1)
		r = self.client.get("/videos/view/1/count")
		self.assertEqual(r.status_code, 200)
		v2 = Video.objects.get(pk=1)
		self.assertEqual(((v1.viewCount) + 1), v2.viewCount)

        def testViewNotExist(self):
		r = self.client.get("/videos/view/5/count")
		self.assertEqual(r.status_code, 404)

class RegistrationTest(TestCase):
    #fixtures = ['test_data.json']

    def test_register1(self):
        request = self.client.post('/accounts/register/', {'username': 'test1', 'email': 'test1@hawk.iit.edu', 'password1': '123456', 'password2': '123456'})
        self.assertTrue(self.client.login(username='test1', password='123456'))
        self.assertTrue(User.objects.get(username='test1').has_perm('videos.add_video'))

        r2 = self.client.get('/videos/upload/')
        self.assertEqual(r2.status_code, 200)

    def test_register2(self):
        request = self.client.post('/accounts/register/', {'username': 'test2', 'email': 'test2@hawk.iit', 'password1': '123456', 'password2': '123456'})
        self.assertTrue(self.client.login(username='test2', password='123456'))
        self.assertFalse(User.objects.get(username='test2').has_perm('videos.add_video'))

        r3 = self.client.get('/videos/upload/')
        self.assertEqual(r3.status_code, 302)

class LoginTest(TestCase):
    def test_details(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

class LogoutTest(TestCase):
    def test_details(self):
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 200)
