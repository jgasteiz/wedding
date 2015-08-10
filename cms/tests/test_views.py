# coding: utf-8
from django.core.urlresolvers import reverse

from wedding.models import get_email_class
from wedding.tests import AppEngineTestCase


class EmailViewsTestCase(AppEngineTestCase):
    def setUp(self):
        super(EmailViewsTestCase, self).setUp()
        self.email_class = get_email_class()

    def test_create_new_email(self):
        response = self.client.get(reverse('cms:create_email'))
        self.assertEqual(200, response.status_code)

        # Posting data will create an email in the database
        response = self.client.post(reverse('cms:create_email'), {
            'name': u'Test email',
            'html_en': u'<h1>Test</h1>',
            'html_es': u'<h1>Test</h1>',
            'html_pl': u'<h1>Test</h1>',
        })

        self.assertEqual(1, self.email_class.objects.all().count())
        self.assertRedirects(response, reverse('cms:emails'))

        email = self.email_class.objects.get()

        self.assertEqual(email.name, u'Test email')
        self.assertEqual(email.html_en, u'<h1>Test</h1>')
        self.assertEqual(email.html_es, u'<h1>Test</h1>')
        self.assertEqual(email.html_pl, u'<h1>Test</h1>')

    def test_update_email(self):
        email = self.email_class.objects.create(
            name=u'Test email',
            html_en=u'<h1>Test</h1>',
            html_es=u'<h1>Test</h1>',
            html_pl=u'<h1>Test</h1>',
        )

        response = self.client.get(reverse('cms:update_email', kwargs={'pk': email.pk}))
        self.assertEqual(200, response.status_code)

        # Posting data will update the email
        response = self.client.post(reverse('cms:update_email', kwargs={'pk': email.pk}), {
            'name': u'Test email EDITED',
            'html_en': u'<h1>Test EDITED</h1>',
            'html_es': u'<h1>Test EDITED</h1>',
            'html_pl': u'<h1>Test EDITED</h1>',
        })

        self.assertEqual(1, self.email_class.objects.all().count())
        self.assertRedirects(response, reverse('cms:emails'))

        email = self.email_class.objects.get()

        self.assertEqual(email.name, u'Test email EDITED')
        self.assertEqual(email.html_en, u'<h1>Test EDITED</h1>')
        self.assertEqual(email.html_es, u'<h1>Test EDITED</h1>')
        self.assertEqual(email.html_pl, u'<h1>Test EDITED</h1>')

    def test_delete_email(self):
        email = self.email_class.objects.create(
            name=u'Test email',
            html_en=u'<h1>Test</h1>',
            html_es=u'<h1>Test</h1>',
            html_pl=u'<h1>Test</h1>',
        )

        response = self.client.get(reverse('cms:delete_email', kwargs={'pk': email.pk}))
        self.assertEqual(200, response.status_code)

        # Posting data will update the email
        response = self.client.post(reverse('cms:delete_email', kwargs={'pk': email.pk}))

        self.assertEqual(0, self.email_class.objects.all().count())
        self.assertRedirects(response, reverse('cms:emails'))

    def test_preview_email(self):
        email = self.email_class.objects.create(
            name=u'Test email',
            html_en=u'<h1>This is the english content</h1>',
        )

        response = self.client.get(reverse('cms:preview_email', kwargs={'pk': email.pk}))
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.content, u'<h1>This is the english content</h1>')
