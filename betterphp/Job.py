import sys, os
def mkprogress(prefix):
    def progress(percent):
        msg = "Done!\n\r" if percent == 100 else "%d%%" % percent
        sys.stdout.write("\r%s%s" % (prefix, msg))
        sys.stdout.flush()
    return progress
class Job:
    def __init__(self, flac, lames):
        self.flac = flac
        self.lames = lames
        self.filename = self.flac.infile
    def run(self):
        infile = self.flac.run(callback=mkprogress("\tDecompressing..."))
        for lame in self.lames:
            lame.infile = infile
            lame.run(callback=mkprogress("\tEncoding to %s..." % lame.format))
        os.remove(infile)
        
