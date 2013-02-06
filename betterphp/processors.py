from subprocess import Popen, PIPE
import os
import re
import logging
import sys
class Lame:
    def __init__(self, format, args, infile, outfile):
        self.infile = infile
        self.outfile = outfile
        self.format = format
        self.args = args
        self.last_progress = 0
        arg_map = {"V0":"-V0", "V2":"-V2", "320":"-b320"}
        self.args.append(arg_map[format])
    def run(self, callback=None):
        
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
#            sys.stdout.write(line)
            if not line:
                break
            m = re.match(r".+\s+\(\s*(\d+)\%\)\|.+", line)
            if m:
                if callback:
                    if int(m.group(1)) != self.last_progress:
                        self.last_progress = int(m.group(1))
                        callback(int(m.group(1)))
        return self.outfile

class Flac:
    def __init__(self, args, infile, outfile=None):
        self.infile = infile
        self.outfile = outfile
        self.args = args
    def run(self, callback=None):
        
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
 #           sys.stdout.write(line)
            if not line:
                break
            m = re.match(r".+: (\d+)\% complete", line)
            if m:
                if callback:
                    callback(int(m.group(1)))
                        
        if not self.outfile:
            self.outfile = re.sub('\.flac$', '.wav', self.infile)
        return self.outfile
