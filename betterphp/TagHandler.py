from mutagen.flac import FLAC
class TagHandler:
    def __init__(self, filename, **kwargs):#artist=None, album=None, date=None, genre=None):
        self.tag = FLAC(filename)
        self.tags = {key:value for key, value in kwargs.iteritems() if value}
    def prompt(self):
        for field in ['artist', 'title', 'date', 'album', 'tracknumber']:
            if not field in self.tags.keys():
                if self.tag.get(field, None):
                    self.tags[field] = self.tag[field][0]
                else:
                    print "Please provide a value for %s" % field
                    self.tags[field] = raw_input("> ")
    def gen_lame(self):
        args = ('--ta|"%(artist)s"|--tt|"%(title)s"|--tl|"%(album)s"|--ty|"%(date)s"|--tn|"%(tracknumber)s"' % self.tags).split('|')
        if self.tags.get('genre', None):
            args += ['--tg', self.tags['genre']]
        return args
if __name__ == "__main__":
    import sys
    t = TagHandler(sys.argv[1])
    t.prompt()
    print t.gen_lame()
