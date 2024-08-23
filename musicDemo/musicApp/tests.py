from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import models
from musicApp.models import Song, Artist, Genre
import datetime

# Create your tests here.

class ArtistTest(TestCase):
    def setUp(self):
        Artist.objects.create(name="Queen")
    
    def testName(self):
        queen = Artist.objects.get(name="Queen")
        self.assertEqual(str(queen), "Queen")

class GenreTest(TestCase):
    def setUp(self):
        Genre.objects.create(name="Rock")
    
    def testName(self):
        rock = Genre.objects.get(name="Rock")
        self.assertEqual(str(rock), "Rock")

    def testDuplicate(self):
        with self.assertRaises(ValidationError):
            duplicate=Genre(name="Rock")
            duplicate.full_clean()

    def testCase(self):
        with self.assertRaises(ValidationError):
            lowerCase=Genre(name="rock")
            lowerCase.full_clean()

class SongTest(TestCase):
    def setUp(self):
        genre = Genre.objects.create(name="Rock")
        artist = Artist.objects.create(name="Queen")
        date = datetime.date(1975, 10, 31)
        self.song = Song.objects.create(title="Bohemian Rhapsody", release_date=date)
        self.song.artists.add(artist)
        self.song.genres.add(genre)

    def testCreation(self):
        self.assertEqual(self.song.title, "Bohemian Rhapsody")
        self.assertEqual(self.song.release_date, datetime.date(1975, 10, 31))
        self.assertIn("Queen", self.song.artists.values_list('name', flat=True))
        self.assertIn("Rock", self.song.genres.values_list('name', flat=True))

    def testStr(self):
        song = Song.objects.get(title="Bohemian Rhapsody")
        self.assertEqual(str(song), "Bohemian Rhapsody (Rock) by Queen (released 1975-10-31)")

    def testManyGenres(self):
        song = Song.objects.get(title="Bohemian Rhapsody")
        newGenre = Genre.objects.create(name="Opera")
        song.genres.add(newGenre)
        self.assertEqual(str(song), "Bohemian Rhapsody (Rock, Opera) by Queen (released 1975-10-31)")

    def testManyArtists(self):
        newArtist1 = Artist.objects.create(name="Elton John")
        newArtist2 = Artist.objects.create(name="Axl Rose")
        song = Song.objects.get(title="Bohemian Rhapsody")
        song.artists.add(newArtist1, newArtist2)
        self.assertEqual(str(song), "Bohemian Rhapsody (Rock) by Queen, Elton John, Axl Rose (released 1975-10-31)")