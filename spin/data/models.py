from django.db import models
from django.conf import settings

class Artist(models.Model) :
    artist_uri = models.CharField(max_length=200, null=True)
    artist_name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.artist_uri

class Song(models.Model) :
    track_uri = models.CharField(max_length=200)
    track_name = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.track_uri

class Playlist(models.Model) :
    name = models.CharField(max_length=200)
    songs = models.ManyToManyField(Song, related_name='playlist_songs')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Temp(models.Model) :
    name = models.CharField(max_length=200, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    uris = models.TextField(null=True)

    def __str__(self):
        return self.name