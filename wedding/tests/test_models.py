# coding: utf-8
from wedding.models import (
    Invitee,
    Song,
    get_email_class,
    get_email_content,
)
from wedding.settings import LANGUAGES
from wedding.tests import AppEngineTestCase


class InviteeTestCase(AppEngineTestCase):
    def setUp(self):
        super(InviteeTestCase, self).setUp()
        self.invitee = Invitee.objects.create(
            first_name=u'Jóhn',
            last_name=u'Dóę',
            email='test@example.com',
            language='en',
            inviter='javi',
        )

    def test_get_language(self):
        self.assertEqual(self.invitee.get_language(), 'English')

    def test_get_invitation_status(self):
        self.assertEqual(self.invitee.get_invitation_status(), 'No RSVP')

    def test_get_inviter(self):
        self.assertEqual(self.invitee.get_inviter(), 'Javi')

    def test_fullname(self):
        self.assertEqual(self.invitee.fullname, u'Jóhn Dóę')

    def test_token_should_get_created_on_save(self):
        invitee = Invitee(
            first_name=u'Craźy',
            last_name=u'Łunatic',
            email='some@test.com',
            language='en',
            inviter='javi',
        )
        self.assertEqual(invitee.token, '')
        invitee.save()
        self.assertTrue(invitee.token is not None)
        token = invitee.token
        invitee.save()
        self.assertEqual(invitee.token, token)


class SongTestCase(AppEngineTestCase):
    def test_artist_name_capitalised(self):
        artist_name = 'acdc'
        Song.objects.create(
            name='You Shook Me All Night Long',
            artist=artist_name,
            submitted_by='javi@test.com'
        )
        song = Song.objects.get()
        self.assertEqual(song.artist, 'Acdc')


class EmailTestCase(AppEngineTestCase):
    def setUp(self):
        super(EmailTestCase, self).setUp()
        self.email_class = get_email_class()

    def test_email_class_has_html_field_per_language(self):
        all_field_names = self.email_class._meta.get_all_field_names()
        for language_key, language_name in LANGUAGES:
            self.assertTrue('html_{}'.format(language_key) in all_field_names)

    def test_email_unicode(self):
        email = self.email_class(name='Email test')
        self.assertTrue(email, 'Email test')

    def test_get_email_content(self):
        email = self.email_class(name='Email test')
        setattr(email, 'html_en', 'Email title')
        setattr(email, 'html_es', 'Titulo del email')
        email.save()

        english_email = get_email_content(email=email, language='en')
        spanish_email = get_email_content(email=email, language='es')

        self.assertTrue('Email title' in english_email)
        self.assertTrue('<head>' in english_email)
        self.assertTrue('Titulo del email' in spanish_email)
        self.assertTrue('<head>' in english_email)

    def test_email_ordering(self):
        email2 = self.email_class.objects.create(name='B second email')
        email1 = self.email_class.objects.create(name='A first email')
        email3 = self.email_class.objects.create(name='C third email')

        all_emails = self.email_class.objects.all()
        self.assertTrue(all_emails[0], email1)
        self.assertTrue(all_emails[1], email2)
        self.assertTrue(all_emails[2], email3)
