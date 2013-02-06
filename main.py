import argparse, os, re, time
from betterphp.processors import Lame, Flac
from betterphp.client import Client
from betterphp.TagHandler import TagHandler
from betterphp.Job import Job
import sys
from colorama import init, Fore
from mutagen.flac import FLAC

DIR_FORMAT = "%(artist)s - %(album)s (%(date)s) [%(format)s]"
TRACK_FORMAT = "%(tracknumber)02d. %(title)s.%(extension)s"
init(autoreset=True)

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--retrieve', dest='retrieve', action='store_true')
parser.add_argument('--encode', dest='encode', action="store_true")
parser.add_argument('--v0', dest='v0', action='store_true')
parser.add_argument('--v2', dest='v2', action='store_true')
parser.add_argument('--320', dest='m320', action='store_true')
parser.add_argument('-i', dest='folder')
parser.add_argument('--dry', dest="dry", action="store_true")
parser.add_argument("--ta", dest="artist")
parser.add_argument("--tl", dest="album")
parser.add_argument("--ty", dest="date")
parser.add_argument("--tg", dest="genre")


args = parser.parse_args()

def make_lame(filename, format_dict, format):
    format_dict['format'] = format
    outfile = os.path.join(DIR_FORMAT % format_dict, relpath, TRACK_FORMAT % format_dict)
    l = Lame(format, tag_args, re.sub(r'\.flac$', r'.mp3', filename), outfile)
    return l
if args.retrieve:
    c = Client("mcfitz2", "Cl0ser2g0d")
    c.login()
    c.retrieve(5)
elif args.encode and args.folder:
    folder = args.folder
    if not os.path.exists(folder):
        raise Exception("Given path does not exist")
    if not os.path.isdir(folder):
        raise Exception("Given path is not a directory")
    to_remove = []
    to_process = sorted([os.path.join(path, f) for path,  directories, files in os.walk(folder) for f in sorted([f for f in files if f.endswith('.flac')])])
    for f in to_process:
        print Fore.GREEN+"Processing"+ os.path.basename(f)
        root = folder
        relpath = f.replace(folder, "").replace(f, "")
        th = TagHandler(f, artist=args.artist, album=args.album, date=args.date, genre=args.genre)
        th.prompt()
        tag_args = th.gen_lame()
        flac = Flac(['-d'], f)
        format_dict = th.tags
        format_dict['extension'] = "mp3"
        lames = []
        if args.v0:
            lames.append(make_lame(f, format_dict, "V0"))
        if args.v2:
            lames.append(make_lame(f, format_dict, "V2"))
        if args.m320:
            lames.append(make_lame(f, format_dict, "320"))
        Job(flac, lames).run()

