from django.shortcuts import render
from django.db.models import Subquery, OuterRef
from .models import Song, Artist

# Create your views here.
def main(request):
    return render(request, "main.html")

def playlist(request):
    sort_option = request.GET.get("sort", "name_a_z")

    # Get primary artist for sorting by artist (First artist should always be primary artist)
    primary_artist = Subquery (Artist.objects.filter(songs=OuterRef("pk")).order_by("pk").values("name")[:1])

    if sort_option == "name_z_a":
        songs = Song.objects.order_by("-title") # Sort by title Z-A
    elif sort_option == "name_a_z":
        songs = Song.objects.order_by("title") # Sort by title A-Z
    elif sort_option == "newest":
        songs = Song.objects.order_by("-release_date") # Sort by newest
    elif sort_option == "oldest":
        songs = Song.objects.order_by("release_date") # Sort by oldest
    elif sort_option == "artist_a_z":
        songs = Song.objects.annotate(primary_artist_name=primary_artist).order_by("primary_artist_name")  # Sort by first artist A-Z
    elif sort_option == "artist_z_a":
        songs = Song.objects.annotate(primary_artist_name=primary_artist).order_by("-primary_artist_name")  # Sort by first artist Z-A
    else:
        songs = Song.objects.order_by("title") # Default to sorting A-Z

    for song in songs:
        song.sorted_genres = sorted(song.genres.all(), key=lambda g: g.name)

    return render(request, "playlist.html", {'songs': songs, 'sort_option': sort_option})