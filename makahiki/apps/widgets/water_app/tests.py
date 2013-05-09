"""
This file demonstrates writing tests in Makahiki. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your widget.

"""
from django.test import TestCase
from water_app.models import Question

class QuestionTests(TestCase):

    fixtures = ['default_questions']

    def testQuestions(self):
        s = Question.objects.get(pk=1)
        self.assertEquals(s.query, '??')
        s.query = '??'
        s.save()