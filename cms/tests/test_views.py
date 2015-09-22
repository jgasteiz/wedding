# coding: utf-8
from django.core.urlresolvers import reverse

from wedding.models import get_email_class, Invitee
from wedding.tests import AppEngineTestCase


class SendEmailsViewTestCase(AppEngineTestCase):
    def setUp(self):
        super(SendEmailsViewTestCase, self).setUp()
        email_class = get_email_class()

        # Create some emails.
        self.email1 = email_class.objects.create(
            name=u'Test email 1',
            html_en=u'<h1>Test en</h1>',
            html_es=u'<h1>Test es</h1>',
        )
        self.email2 = email_class.objects.create(
            name=u'Test email 2',
            html_en=u'<h1>Test en</h1>',
            html_es=u'<h1>Test es</h1>',
        )

        # Create a few invitees
        self.invitee1 = Invitee.objects.create(
            first_name='Jon',
            last_name='Snow',
            email='jonsnow@thewall.com',
            language='en',
        )
        self.invitee2 = Invitee.objects.create(
            first_name='Daenerys',
            last_name='Targaryen',
            email='khaleesi@meereen.com',
            language='en',
        )

    def test_send_email_to_invitees(self):

        # Test sending the email 1 to both invitees
        payload = {
            'email': self.email1.pk,
            'invitees[]': [self.invitee1.pk, self.invitee2.pk],
        }
        response = self.client.post(reverse('cms:send_emails'), payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'OK')

        # Make sure both invitees got the email
        self.invitee1 = Invitee.objects.get(pk=self.invitee1.pk)
        self.assertEqual(self.invitee1.emails, str(self.email1.pk))
        self.invitee2 = Invitee.objects.get(pk=self.invitee2.pk)
        self.assertEqual(self.invitee2.emails, str(self.email1.pk))

    def test_not_send_same_email_twice(self):

        # Let's say invitee1 got email1 already.
        self.invitee1.emails = str(self.email1.pk)

        # Test sending the email 1 to both invitees
        payload = {
            'email': self.email1.pk,
            'invitees[]': [self.invitee1.pk],
        }
        response = self.client.post(reverse('cms:send_emails'), payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'OK')

        # Make sure nothing really changed
        self.invitee1 = Invitee.objects.get(pk=self.invitee1.pk)
        self.assertEqual(self.invitee1.emails, str(self.email1.pk))

        # Send email 2 now.
        payload = {
            'email': self.email2.pk,
            'invitees[]': [self.invitee1.pk],
        }
        response = self.client.post(reverse('cms:send_emails'), payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'OK')

        # Make sure invitee got email 2.
        self.invitee1 = Invitee.objects.get(pk=self.invitee1.pk)
        self.assertEqual(self.invitee1.emails, ','.join([str(self.email1.pk), str(self.email2.pk)]))


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
        })

        self.assertEqual(1, self.email_class.objects.all().count())
        self.assertRedirects(response, reverse('cms:emails'))

        email = self.email_class.objects.get()

        self.assertEqual(email.name, u'Test email')
        self.assertEqual(email.html_en, u'<h1>Test</h1>')
        self.assertEqual(email.html_es, u'<h1>Test</h1>')

    def test_update_email(self):
        email = self.email_class.objects.create(
            name=u'Test email',
            html_en=u'<h1>Test</h1>',
            html_es=u'<h1>Test</h1>',
        )

        response = self.client.get(reverse('cms:update_email', kwargs={'pk': email.pk}))
        self.assertEqual(200, response.status_code)

        # Posting data will update the email
        response = self.client.post(reverse('cms:update_email', kwargs={'pk': email.pk}), {
            'name': u'Test email EDITED',
            'html_en': u'<h1>Test EDITED</h1>',
            'html_es': u'<h1>Test EDITED</h1>',
        })

        self.assertEqual(1, self.email_class.objects.all().count())
        self.assertRedirects(response, reverse('cms:emails'))

        email = self.email_class.objects.get()

        self.assertEqual(email.name, u'Test email EDITED')
        self.assertEqual(email.html_en, u'<h1>Test EDITED</h1>')
        self.assertEqual(email.html_es, u'<h1>Test EDITED</h1>')

    def test_delete_email(self):
        email = self.email_class.objects.create(
            name=u'Test email',
            html_en=u'<h1>Test</h1>',
            html_es=u'<h1>Test</h1>',
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

        preview_url = '{}?language=en'.format(reverse('cms:preview_email', kwargs={'pk': email.pk}))
        response = self.client.get(preview_url)
        self.assertEqual(200, response.status_code)
        self.assertContains(response, u'<h1>This is the english content</h1>')
