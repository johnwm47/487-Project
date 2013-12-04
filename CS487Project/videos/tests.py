"""
Test benchmark guidelines:
        Force errors where they are supposed to appear
                404
                redirects due to lack of authorization
        Make sure there are no 500s
        Make sure all pages that should load load properly
        Make sure all filters result in the correct result set
These guidelines were chosen because they cover all of the critical aspects of the system.

"""

from django.test import TestCase, TransactionTestCase
from models import Video, Journal, Keyword, Author
from django.contrib.auth.models import User
from django.db.models import Count

# tests the video upload page
# if this fails, check videos.views.uploadFile, videos/templates/videos/upload.html, videos/templates/videos/upload_success.html
class UploadTest(TestCase):
        fixtures = ['test_data.json'] # create test videos

        def test_login_redirect(self):
                # test redirect to login page for normal user
                self.assertTrue(self.client.login(username='nu', password='nu'))
                r = self.client.get('/videos/upload/')
                self.assertEqual(r.status_code, 403)

        def test_upload(self):
                # test to make sure upload page works for uploader
                self.assertTrue(self.client.login(username='up', password='up'))
                r = self.client.get('/videos/upload/')
                self.assertEqual(r.status_code, 200)

                f = open('../soccer.mp4')
                r2 = self.client.post('/videos/upload/', {'title':'Test', 'description':'Testd', 'url':'www.google.com', 'authors':(1), 'keywords':(1, 2), 'journal': 1, 'video': f})
                f.close()

                o = Video.objects.get(title='Test')
                self.assertRedirect(o.get_absolute_url())
                self.assertEqual(o.description, 'Testd')
                self.assertEqual(o.url, 'http://www.google.com/')
                self.assertEqual(o.viewCount, 0)
                self.assertEqual(o.journal, Journal.objects.get(pk=1))

class EditTest(TestCase):
    fixtures = ['test_data.json']

    def testNotAuthorized(self):
        self.assertTrue(self.client.login(username='nu', password='nu'))
        r = self.client.get('/videos/1/edit')
        self.assertEqual(r.status_code, 403)

    def testAdmin(self):
        self.assertTrue(self.client.login(username='admin', password='admin'))
        r = self.client.get('/videos/1/edit')
        self.assertEqual(r.status_code, 200)

    def testUploader(self):
        self.assertTrue(self.client.login(username='up', password='up'))
        r = self.client.get('/videos/1/edit')
        self.assertEqual(r.status_code, 200)

    def testChange(self):
        v = Video.objects.get(pk=1)
        self.assertTrue(self.client.login(username="admin", password="admin"))
        r = self.client.post(v.get_absolute_url(), {'title': 'Changed title'})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Video.objects.get(pk=1).title, 'Changed title')

class RatingTest(TestCase):
    fixtures = ['test_data.json']

    def testNotAuthorized(self):
        r = self.client.get('/videos/1/rate/star')
        self.assertequal(r.status_code, 403)

    def testAuthorized(self):
        self.assertTrue(self.client.login(username='nu', password='nu'))
        r = self.client.get('/videos/1/rating/star')
        self.assertEqual(r.status_code, 200)

    def testSubmit(self):
        self.assertTrue(self.client.login(username='nu', password='nu'))
        v = Video.objects.get(pk=1)
        r = self.client.post("%s/rating/star" % v.get_absolute_url(), {'rating': '1'})

        self.assertEqual(v.star.get(rater=User.objects.get(username='nu')).rating, 1)

# tests the search pages
# if this fails, check videos.views.searchResult, videos/templates/videos/search.html
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

        def testViewIncementedLogin(self):
                self.client.login(username="nu", password="nu")
                v1 = Video.objects.get(pk=1)
                try:
                    v1u = v1.user_views.get(user=self.client).count
                except ObjectDoesNotExist:
                    v1u = 0

                r = self.client.get("/videos/view/1/count")
                self.assertEqual(r.status_code, 200)

                v2 = Video.objects.get(pk=1)
                v2u = v2.user_views.get(user=self.client).count

                self.assertEqual(v1.viewCount + 1, v2.viewCount)
                self.assertEqual(v1u + 1, v2u)

        def testViewNotExist(self):
		r = self.client.get("/videos/view/5/count")
		self.assertEqual(r.status_code, 404)

# tests the registration page
# if this fails, check CS487Project.views.register, videos/templates/registration/register.html
class RegistrationTest(TestCase):
    def test_register1(self):
        request = self.client.post('/accounts/register/', {'username': 'test1', 'email': 'test1@hawk.iit.edu', 'password1': '123456', 'password2': '123456'})
        self.assertTrue(self.client.login(username='test1', password='123456'))
        self.assertTrue(User.objects.get(username='test1').has_perm('videos.add_video'))

    def test_register2(self):
        request = self.client.post('/accounts/register/', {'username': 'test2', 'email': 'test2@hawk.iit', 'password1': '123456', 'password2': '123456'})
        self.assertTrue(self.client.login(username='test2', password='123456'))
        self.assertFalse(User.objects.get(username='test2').has_perm('videos.add_video'))

# tests the login page. The login view is a built-in component that has already been tested, therefore we only need to make sure that the template renders
# if this fails, check /videos/templates/registration/login.html
class LoginTest(TestCase):
    def test_details(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

# tests the logout page. The logout view is a built-in component that has already been tested, therefore we only need to make sure that the template renders
# if this fails, check /videos/templates/registration/logout.html
class LogoutTest(TestCase):
    def test_details(self):
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 200)
