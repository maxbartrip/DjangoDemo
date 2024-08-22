from django.db import models

# Create your models here.

class Artist(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Song(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    artists = models.ManyToManyField(Artist, related_name='songs')
    genres = models.ManyToManyField(Genre, related_name='songs')

    def __str__(self):
        # Get a list of artist names associated with the song
        artist_names = ', '.join(artist.name for artist in self.artists.all())
        # Get a list of genre names associated with the song
        genre_names = ', '.join(genre.name for genre in self.genres.all())
        # Format the string as "Song Title (Genre1, Genre2) by Artist1, Artist2 (released yyyy-mm-dd)"
        return f"{self.title} ({genre_names}) by {artist_names} (released {self.release_date})"