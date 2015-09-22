# coding: utf-8
from wedding.models import (
    Song,
    get_email_class,
)
from wedding.settings import LANGUAGES
from wedding.tests import AppEngineTestCase


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

    def test_email_ordering(self):
        email2 = self.email_class.objects.create(name='B second email')
        email1 = self.email_class.objects.create(name='A first email')
        email3 = self.email_class.objects.create(name='C third email')

        all_emails = self.email_class.objects.all()
        self.assertTrue(all_emails[0], email1)
        self.assertTrue(all_emails[1], email2)
        self.assertTrue(all_emails[2], email3)
