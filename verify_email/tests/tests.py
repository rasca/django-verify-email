import datetime

from django.test import TestCase
from django.test.client import RequestFactory
from django.core import mail


from verify_email.models import Verification
from verify_email.forms import VerifyEmailForm


class VerificationModelTests(TestCase):
    def setUp(self):
        self.v1 = Verification.objects.create(email='test@test.com')
        self.v2 = Verification.objects.create(email='test@test.com')

    def test_hash_creation(self):
        self.assertEqual(len(self.v1.hash), 64)
        self.assertNotEqual(self.v1.hash, self.v2.hash)

    def test_validate(self):
        # check for non existing hash
        self.assertFalse(Verification.objects.validate(hash='NOHASH'))

        v1hash = self.v1.hash
        v2hash = self.v2.hash

        # check correct hash and no constraints
        self.assertTrue(Verification.objects.validate(hash=v1hash))

        # check expiration_period
        self.assertTrue(Verification.objects.validate(hash=v1hash,
                         expiration_period=datetime.timedelta(weeks=1)))
        self.assertFalse(Verification.objects.validate(hash=v1hash,
                         expiration_period=datetime.timedelta(weeks=0)))

        # check expires_on_usage
        self.assertTrue(Verification.objects.validate(hash=v2hash,
                         expires_on_usage=True))
        self.assertFalse(Verification.objects.validate(hash=v2hash,
                         expires_on_usage=True))

    def test_used(self):

        # check that it's marked as used
        self.assertFalse(self.v1.used)

        Verification.objects.validate(hash=self.v1.hash)

        self.assertTrue(Verification.objects.get(hash=self.v1.hash).used)


class DecoratorTests(TestCase):
    urls = 'verify_email.tests.urls'

    def setUp(self):
        self.v1 = Verification.objects.create(email='test1@test.com')
        self.v2 = Verification.objects.create(email='test2@test.com')

    def test_no_parameters(self):
        response = self.client.get('/simple-view/')
        self.assertEqual(response.content, 'None')

        response = self.client.get('/simple-view/?hash=NOHASH')
        self.assertEqual(response.content, 'None')

        response = self.client.get('/simple-view/?hash=%s' % self.v1.hash)
        self.assertEqual(response.content, 'test1@test.com')

    def test_with_view(self):
        response = self.client.get('/other-view/')
        self.assertEqual(response.content, 'VERIFY')

        response = self.client.get('/simple-view/?hash=%s' % self.v1.hash)
        self.assertEqual(response.content, 'test1@test.com')


class VerifyEmailFormTests(TestCase):
    def test_form(self):
        factory = RequestFactory()
        data = {'email': 'test1@test.com', }
        form = VerifyEmailForm(data)
        self.assertTrue(form.is_valid())

        self.assertEqual(Verification.objects.count(), 0)

        request = factory.get('/test/')
        form.save(request, 'verification_email2.html', 'subject')

        self.assertEqual(Verification.objects.count(), 1)
        self.assertTrue(len(mail.outbox), 1)


class TemplateTests(TestCase):
    urls = 'verify_email.tests.urls'

    def test_templates(self):
        data = {'email': 'test1@test.com', }
        response = self.client.post('/other-view2/', data)
        self.assertTrue(len(mail.outbox), 1)
        self.assertTrue(mail.outbox[0].subject, 'YOUR SUBJECT HERE2')
        self.assertTrue(mail.outbox[0].body, 'TEMPLATE')
