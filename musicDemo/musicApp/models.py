from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Artist(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
    def clean(self):
        # Normalize the name to lower case for uniqueness check
        normalized_name = self.name.lower()
        if Genre.objects.exclude(pk=self.pk).filter(name__iexact=normalized_name).exists():
            raise ValidationError('Genre with this Name already exists')
        super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

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