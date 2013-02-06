from subprocess import Popen, PIPE
import os
import re
class Lame:
    def __init__(self, args, infile, outfile):
        self.infile = infile
        self.outfile = outfile
        self.args = args
        
    def run(self, callback):
        command = ["lame"]+self.args+[self.infile]+([self.outfile] if self.outfile else [])

        if self.outfile:
            if not os.path.exists(self.outfile):
 
                try:
                    os.makedirs(os.path.dirname(self.outfile))
                except OSError:
                    pass
 
        p = Popen(command, stderr=PIPE)
        while True:
            line = p.stderr.readline()
            if not line:
                break
            m = re.match(r".+\s+\(\s*(\d+)\%\)\|.+", line)
            if m:
                callback(int(m.group(1)))
        return self.outfile

class Flac:
    def __init__(self, args, infile, outfile=None):
        self.infile = infile
        self.outfile = outfile
        self.args = args
    def run(self, callback):
        command = ["flac"]+self.args+[self.infile]+(["-o", self.outfile] if self.outfile else [])
        if self.outfile:
            if not os.path.exists(self.outfile):
 
                try:
                    os.makedirs(os.path.dirname(self.outfile))
                except OSError:
                    pass
 
        p = Popen(command, stderr=PIPE)
        while True:
            line = p.stderr.read(128)
            if not line:
                break
            m = re.match(r".+: (\d+)\% complete", line)
            if m:
                callback(int(m.group(1)))
 
        if not self.outfile:
            self.outfile = re.sub('\.flac$', '.wav', self.infile)
        return self.outfile
