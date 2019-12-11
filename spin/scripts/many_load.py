# python3 manage.py runscript many_load

import csv
from data.models import Artist, Song

def run():
    fhand = open('data/spin_data.csv')
    reader = csv.reader(fhand)

    Artist.objects.all().delete()
    Song.objects.all().delete()

    next(reader)
    for row in reader:
        print(row)
        artist, created = Artist.objects.get_or_create(artist_uri=row[0], artist_name=row[1])
        # add entry
        s = Song(track_uri=row[2], track_name=row[3], artist=artist)
        s.save()