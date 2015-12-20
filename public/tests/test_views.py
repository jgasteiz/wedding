# coding: utf-8
from django.core.urlresolvers import reverse

from wedding.constants import CONFIRMED, DECLINED, NO_RSVP
from wedding.models import Invitee
from wedding.tests import AppEngineTestCase


class RsvpViewsTestCase(AppEngineTestCase):
    def setUp(self):
        super(RsvpViewsTestCase, self).setUp()
        self.invitee = Invitee.objects.create(
            first_name=u'Jóhn',
            last_name=u'Dóę',
            email='test@example.com',
            language='en',
            inviter='javi',
        )

    def test_rsvp_should_not_render_any_form_without_invitee_token(self):
        response = self.client.get(reverse('public:rsvp'))
        self.assertEqual(200, response.status_code)
        self.assertNotContains(response, '<form')
        self.assertEquals(response.context['invitee'], None)

    def test_rsvp_with_token_should_redirect(self):
        response = self.client.get('{}?invitee={}'.format(reverse('public:rsvp'), self.invitee.token))

        # It should redirect to rsvp without the GET parameter
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('public:rsvp'))

    def test_should_render_rsvp_form_if_valid_token(self):
        response = self.client.get('{}?invitee={}'.format(reverse('public:rsvp'), self.invitee.token), follow=True)

        self.assertEqual(200, response.status_code)
        self.assertContains(response, '<form')
        self.assertEquals(response.context['invitee'], self.invitee)

    def test_should_not_render_rsvp_form_if_invalid_token(self):
        response = self.client.get('{}?invitee={}'.format(reverse('public:rsvp'), 'this-is-invalid'), follow=True)

        self.assertEqual(200, response.status_code)
        self.assertNotContains(response, '<form')
        self.assertEquals(response.context['invitee'], None)

    def test_should_have_invitee_token_in_session(self):
        self.client.get('{}?invitee={}'.format(reverse('public:rsvp'), self.invitee.token), follow=True)
        self.assertEqual(self.client.session.get('invitee'), unicode(self.invitee.token))

    def test_should_change_invitee_invitation_status(self):
        # Before posting anything the invitee should be NO_RSVP and no plusone.
        invitee = Invitee.objects.get(id=self.invitee.id)
        self.assertEqual(invitee.invitation_status, NO_RSVP)
        self.assertEqual(invitee.has_plusone, False)

        # Before authenticating, posting data should do nothing and redirect to the same url.
        response = self.client.post(reverse('public:rsvp'), data={
            'are_you_coming': True,
            'bringing_plusone': True,
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('public:rsvp'))
        invitee = Invitee.objects.get(id=self.invitee.id)
        self.assertEqual(invitee.invitation_status, NO_RSVP)
        self.assertEqual(invitee.has_plusone, False)

        # Authenticate through the user token.
        self.client.get('{}?invitee={}'.format(reverse('public:rsvp'), self.invitee.token), follow=True)

        # Update status of invitee to CONFIRMED and yes to plusone.
        response = self.client.post(reverse('public:rsvp'), data={
            'are_you_coming': True,
            'bringing_plusone': True,
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('public:rsvp_thanks'))

        invitee = Invitee.objects.get(id=self.invitee.id)
        self.assertEqual(invitee.invitation_status, CONFIRMED)
        self.assertEqual(invitee.has_plusone, True)

        # Now decline the invitation.
        response = self.client.post(reverse('public:rsvp'), data={
            'are_you_coming': False,
            'bringing_plusone': False,
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('public:rsvp_thanks'))

        invitee = Invitee.objects.get(id=self.invitee.id)
        self.assertEqual(invitee.invitation_status, DECLINED)
        self.assertEqual(invitee.has_plusone, False)
