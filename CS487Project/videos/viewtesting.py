from django.test import TestCase
from videos.models import Video

class VideoTest(TestCase):
        fixtures = ['test_data'] # a default set of videos

        def testViewVideoExists(self):
		r = self.client.get("/videos/view/1/")
		self.assertEqual(r.status_code, 200)
		self.assertEqual(r.context['video'], Videos.objects.get(pk=1) # the list() part is only needed for a queryset. These are individual objects, therefore it is unnecessary). This is comparing the video that is rendered in the template with the video in the database, retrieved through the Python API
		
        def testViewVideoNotExists(self):
		r = self.client.get("/videos/view/5/")
		self.assertEqual(r.status_code, 404)

        def testViewIncremented(self)
		r = self.client.get("/videos/view/1/count/")
		self.assertRedirects(r, '/videos/view/1/count/')
		self.assertEqual(r.status_code, 200)
		r2 = self.client.get("/videos/view/1/count/")
        # make sure that video.viewCount has incremented
		# not sure about that one
		
        def testViewNotExist(self)
		
		r = self.client.get("/videos/view/5/")
		self.assertRedirects(r, '/videos/view/5/count')
		self.assertEqual(r.status_code, 404)
		# is this one correct?