from beets.plugins import BeetsPlugin

from beets.mediafile import MediaFile, ListMediaField, ListStorageStyle, MediaField

class SplitPlugin(BeetsPlugin):
    def __init__(self):
        super(SplitPlugin, self).__init__()
        separator = self.config['separator'].get()
        fields = self.config['fields'].get()
        for f in fields:
            setattr(
                    MediaFile,
                    f,
                    MediaField(HackedStorageStyle(f.upper(), separator))
            )

class HackedStorageStyle(ListStorageStyle):
    def __init__(self, tag, separator):
        super(HackedStorageStyle, self).__init__(tag)
        self.separator = separator

    def set(self, mutagen_file, value):
        split = value.split(self.separator)
        trimmed = [s.strip() for s in split if s.strip() != '']
        self.set_list(mutagen_file, trimmed)
