from beets.plugins import BeetsPlugin
from beets.ui import Subcommand
import musicbrainzngs
import discogs_client
import re
import functools
from beets import mediafile
from beets.dbcore import types

discogs_extra_init = Subcommand(
        'discogs-extra',
        help='Initialize all albums with extra discogs data.')

class DiscogsData(BeetsPlugin):
    def __init__(self):
        super(DiscogsData, self).__init__()
        self.item_types = {
            'performer': types.STRING
        }

        self.discogs_client = discogs_client.Client(
                'github.com/SimonPersson/beets-plugins/0.1',
                user_token= self.config['token'].get()
        )
        self.separator = self.config['separator'].get()
        self.register_listener('album_imported', self.album_imported)
        try:
            self.add_media_field('performer', mediafile.MediaField(
                mediafile.StorageStyle('PERFORMER')
            ))
        except Exception:
            pass
        discogs_extra_init.func = self.all_album_init

    def commands(self):
        return [discogs_extra_init]

    def album_imported(self, album):
        release_group_id = album.get('mb_releasegroupid')
        release_id = album.get('mb_albumid')
        discogs_urls = get_discogs_urls(release_id, release_group_id)
        if len(discogs_urls) > 0:
            discogs_url = sorted(discogs_urls)[0]
            album.discogs_url = discogs_url
            (year, labels, performers) = self.get_discogs_data(discogs_url)
            if album['original_year'] > year:
                album.original_year = year
            album.label = self.separator.join(labels)
            performer = self.separator.join(performers)
            album.performer = performer
            album.store()
            for item in album.items():
                item.performer = performer
                item.write()
                item.store()

    def all_album_init(self, lib, opts, args):
        for album in lib.albums():
            print(f'Importing discogs data for {album}')
            try:
                self.album_imported(album)
            except Exception as e:
                print(f"Something went wrong: {e}") 


    @functools.lru_cache(maxsize=1024)
    def get_discogs_data(self, url):
        if 'master' in url:
                master = self.discogs_client.master(url.split('/')[-1]).main_release
        else:
                release = self.discogs_client.release(url.split('/')[-1])
                master = release
                try:
                    master = release.master.main_release
                except Exception:
                    pass

        year=master.year
        labels = [label.name for label in master.labels]
        credits = master.data['extraartists']
        credits = [f"{c['name']} ({c['role']})" for c in credits if is_musician(c['role'])]

        return (year, labels, credits)

@functools.lru_cache(maxsize=1024)
def get_discogs_urls(release_id, release_group_id):
    discogs_urls=[]
    try:
        release = musicbrainzngs.get_release_by_id(release_id, includes=['url-rels'])
        discogs_urls += [u['target'] for u in release['release']['url-relation-list'] if u['type']=='discogs']
    except Exception as e:
        pass

    try:
        release_group = musicbrainzngs.get_release_group_by_id(release_group_id, includes=['url-rels'])
        discogs_urls += [u['target'] for u in release_group['release-group']['url-relation-list'] if u['type']=='discogs']
    except Exception as e:
        pass
    return discogs_urls

def is_musician(credit):
    return any((i in credit.lower() for i in instruments))

# This is obviously not a complete list of instruments, but pretty much covers
# my library of mostly jazz.
instruments = [ 'accordion', 'bass', 'sax', 'bass', 'bassoon', 'bells',
        'strings', 'bongos', 'congas', 'timbales', 'cello', 'clarinet',
        'percussion', 'cornet', 'drum', 'guitar', 'piano', 'horn', 'flute',
        'vibraphone', 'harmonica', 'harp', 'organ', 'tambura', 'timpani',
        'keyboard', 'maracas', 'oboe', 'percussion', 'trombone', 'trombone',
        'tuba', 'trumpet', 'tambourine', 'vocals', 'viola', 'violin']
