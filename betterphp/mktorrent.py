import os
from subprocess import Popen, PIPE
class mktorrent:
    def __init__(self, announce, directory):
        self.directory = directory
        self.announce = announce
    def run(self):
        if os.path.exists(self.directory+".torrent"):
            os.remove(self.directory+".torrent")
        p = Popen(["mktorrent", "-p","-a", self.announce, self.directory], stdout=PIPE, stderr=PIPE)
        p.wait()
