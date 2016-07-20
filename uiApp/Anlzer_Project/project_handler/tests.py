__author__ = 'mpetyx'

from django.test import TestCase

from django.test import TestCase
from selenium import webdriver
from models import Project



class S3CustomStorageTestCase(TestCase):

    def setUp(self):
        self.project = Project()

    def test_group_user(self):
        response = self.client.get('/api/group/%d/user/%d' % (self.group.id, self.user.id))
        # print(response)
        # pprint(response.__dict__)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response._container), 1)


    def tearDown(self):
        self.project.delete()
        self.browser.quit()
