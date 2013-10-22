from django.test import TestCase
from Videos import Video

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
		# get the video through the python api, store as variable
                # visit "/videos/view/1/count"
                # make sure status code correct
                # get the video through the python api AGAIN
                # make sure that video.viewCount has incremented
		
        def testViewNotExist(self)
		# mirror testViewVideoNotExist, change URL
