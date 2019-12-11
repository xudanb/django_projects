from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect

from data.models import Artist, Song, Playlist

class MainView(LoginRequiredMixin, View):
    template_name = 'search/main.html'

    def get(self, request) :
        # playlist
        playlist, created = Playlist.objects.get_or_create(name='temp', owner=request.user)
        # add song
        track_uri = request.GET.get('u')
        if track_uri!=None:
            song = get_object_or_404(Song, track_uri=track_uri)
            if song!=None:
                playlist.songs.add(song)
                playlist.save()
        ctx = {'playlist':playlist}
        return render(request, self.template_name, ctx)

    def post(self, request) :
        name = request.POST.get('n')
        if name!='':
            new, created = Playlist.objects.get_or_create(name=name, owner=request.user)
            temp = get_object_or_404(Playlist, name='temp', owner=request.user)
            for song in temp.songs.all():
                new.songs.add(song)
            new.save()
            temp.songs.clear()
            temp.save()
        return redirect('/play')

class ResultsView(LoginRequiredMixin, View):
    template_name = 'search/results.html'

    def get(self, request):
        query = request.GET.get('q')
        type = request.GET.get('t')
        if len(query)<2: query='ahwojsadiq'
        if type=='artist':
            results = Artist.objects.filter(artist_name__icontains=query)
        elif type=='song':
            results = Song.objects.filter(track_name__icontains=query)
        else:
            results = Song.objects.filter(track_name__icontains='ahwojsadiq')
        ctx = {'type':type, 'results':results}
        return render(request, self.template_name, ctx)

    def post(self, request) :
        playlist = get_object_or_404(Playlist, name='temp', owner=request.user)
        track_uri = request.POST.get('u')
        if track_uri!=None:
            song = get_object_or_404(Song, track_uri=track_uri)
            if song!=None:
                playlist.songs.add(song)
                playlist.owner = request.user
                playlist.save()
        return redirect('/search')