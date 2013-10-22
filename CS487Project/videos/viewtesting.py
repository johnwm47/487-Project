from django.test import TestCase
from Videos import Video

def testViewVideoExists(self):
		r = Videos.objects.get(pk=1)
		self.assertEqual(r.status_code, 200)
		self.assertEqual(list(r.context['video']), list(self.client.get(pk=1)))
		
def testViewVideoExists(self):
		r = Videos.objects.get(pk=1)
		self.assertEqual(r.status_code, 200)
		self.assertEqual(list(r.context['video']), [])

def testViewIncremented(self)
		r = 
		
def testViewNotIncremented(self)
		r = 