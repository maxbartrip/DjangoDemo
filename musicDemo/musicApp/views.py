from django.shortcuts import render
from .models import Song

# Create your views here.
def main(request):
    return render(request, "main.html")

def playlist(request):
    sort_option = request.GET.get('sort', 'name_a_z')

    if sort_option == 'name_z_a':
        songs = Song.objects.order_by('-title')  # Sort by title Z-A
    else:
        songs = Song.objects.order_by('title')   # Sort by title A-Z

    for song in songs:
        song.sorted_genres = sorted(song.genres.all(), key=lambda g: g.name)

    return render(request, "playlist.html", {'songs': songs, 'sort_option': sort_option})