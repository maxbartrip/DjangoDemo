from django.shortcuts import render
from .models import Song

# Create your views here.
def main(request):
    return render(request, "main.html")

def playlist(request):
    songs = Song.objects.all()
    return render(request, "playlist.html", {'songs': songs})