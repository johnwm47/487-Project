from __future__ import absolute_import

import time

from django.conf import settings

from django_comments.forms import CommentForm
from django_comments.models import Comment

from . import CommentTestCase
from ..models import Article


class CommentFormTests(CommentTestCase):
    def testInit(self):
        f = CommentForm(Article.objects.get(pk=1))
        self.assertEqual(f.initial['content_type'], str(Article._meta))
        self.assertEqual(f.initial['object_pk'], "1")
        self.assertNotEqual(f.initial['security_hash'], None)
        self.assertNotEqual(f.initial['timestamp'], None)

    def testValidPost(self):
        a = Article.objects.get(pk=1)
        f = CommentForm(a, data=self.getValidData(a))
        self.assertTrue(f.is_valid(), f.errors)
        return f



    def testTimestampTampering(self):
        self.tamperWithForm(timestamp=str(time.time() - 28800))

    def testSecurityHashTampering(self):
        self.tamperWithForm(security_hash="Nobody expects the Spanish Inquisition!")

    def testContentTypeTampering(self):
        self.tamperWithForm(content_type="auth.user")

    def testObjectPKTampering(self):
        self.tamperWithForm(object_pk="3")


    def testGetCommentObject(self):
        f = self.testValidPost()
        c = f.get_comment_object()
        self.assertTrue(isinstance(c, Comment))
        self.assertEqual(c.content_object, Article.objects.get(pk=1))
        self.assertEqual(c.comment, "This is my comment")
        c.save()
        self.assertEqual(Comment.objects.count(), 1)

    
