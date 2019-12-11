from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404

from data.models import Playlist, Temp

class MainView(LoginRequiredMixin, View):
    template_name = 'play/main.html'

    def get(self, request) :
        owner = request.user
        ctx = {'owner':owner}
        return render(request, self.template_name, ctx)

class StartView(LoginRequiredMixin, View):
    template_name = 'play/start.html'
    def get(self, request) :
        name = request.GET.get('n')
        if name!=None:
            owner = request.user
            playlist = get_object_or_404(Playlist, name=name, owner=owner)
            uris = ''
            songs = playlist.songs.all()
            for song in songs:
                uris += song.track_uri + ','
            uris = uris[:-1]
            temp, created = Temp.objects.get_or_create(name='temp', owner=request.user)
            temp.uris = uris
            temp.save()
        temp = get_object_or_404(Temp, name='temp', owner=request.user)
        ctx = {'temp':temp}
        return render(request, self.template_name, ctx)