import argparse
import os
import re
import sys
from betterphp.processors import Lame, Flac
from betterphp.client import Client
from betterphp.TagHandler import TagHandler
from betterphp.Job import Job
from betterphp.mktorrent import mktorrent
import json

config = {}
if os.path.exists(os.path.join(os.path.dirname(__file__),"config.json")):
    with open(os.path.join(os.path.dirname(__file__),"config.json"), 'r') as c:
        try:
            config = json.load(c)
        except ValueError as e: 
            print "Could not parse config file", e
            exit(1)
        

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-r', dest='retrieve')
parser.add_argument('--v0', dest='v0', action='store_true')
parser.add_argument('--v2', dest='v2', action='store_true')
parser.add_argument('--320', dest='m320', action='store_true')
parser.add_argument('-i', dest='folder')
parser.add_argument('--dry', dest="dry", action="store_true")
parser.add_argument("--ta", dest="artist")
parser.add_argument("--tl", dest="album")
parser.add_argument("--ty", dest="date")
parser.add_argument("--tg", dest="genre")
parser.add_argument("-a", dest="announce")
parser.add_argument("-u", dest="user")
parser.add_argument("-p", dest="password")
parser.add_argument("-n", dest="num", type=int)
args = parser.parse_args()


DIR_FORMAT = config.get('DIR_FORMAT') or "%(artist)s - %(album)s (%(date)s) [%(format)s]"
TRACK_FORMAT = config.get('TRACK_FORMAT') or "%(tracknumber)02d. %(title)s.%(extension)s"

args.announce = config.get('announce') or args.announce
args.v0 =  args.v0 or config.get('V0')
args.v2 = args.v2 or config.get('V2')
args.m320 = args.m320 or config.get('320')
args.user = args.user or config.get("user")
args.password = args.password or config.get("password")
args.num = args.num or 1

def get_out_dir(fmt, fmt_dict):
    format_dict['format'] = fmt
    return DIR_FORMAT % fmt_dict
    
def make_lame(filename, fmt_dict, fmt):
    format_dict['format'] = fmt
    outfile = os.path.join(get_out_dir(fmt, fmt_dict), relpath, TRACK_FORMAT % fmt_dict)
    l = Lame(fmt, tag_args, re.sub(r'\.flac$', r'.mp3', filename), outfile)
    l.outdir = get_out_dir(fmt, fmt_dict)
    return l
if args.retrieve:
    c = Client(args.user, args.password)
    c.login()
    c.retrieve(args.num, args.retrieve)
elif (args.v0 or args.v2 or args.m320) and args.folder:
    folder = args.folder
    if not os.path.exists(folder):
        raise Exception("Given path does not exist")
    if not os.path.isdir(folder):
        raise Exception("Given path is not a directory")
    to_remove = []
    to_process = sorted([os.path.join(path, f) for path,  directories, files in os.walk(folder) for f in sorted([f for f in files if f.endswith('.flac')])])
    for i,f in enumerate(to_process):
        print "Processing file %02d/%02d: %s" % (i+1, len(to_process), os.path.basename(f))
        root = folder
        relpath = f.replace(folder, "").replace(f, "")
        th = TagHandler(f, artist=args.artist, album=args.album, date=args.date, genre=args.genre)
        th.prompt()
        tag_args = th.gen_lame()
        flac = Flac(['-d', '-f'], f)
        format_dict = th.tags
        format_dict['extension'] = "mp3"
        lames = []
        torrent_dirs = []
        if args.v0:
            l = make_lame(f, format_dict, "V0")
            torrent_dirs.append(l.outdir)
            lames.append(l)
        if args.v2:
            l = make_lame(f, format_dict, "V2")
            torrent_dirs.append(l.outdir)
            lames.append(l)
        if args.m320:
            l = make_lame(f, format_dict, "320")
            torrent_dirs.append(l.outdir)
            lames.append(l)
        Job(flac, lames).run()

    sys.stdout.write("Creating torrents...")
    if args.announce:
        for directory in torrent_dirs:
            m = mktorrent(args.announce, directory)
            m.run()
    print "Done!"
                      


