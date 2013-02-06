import argparse, os, re
from betterphp.processors import Lame, Flac
from betterphp.client import Client
from betterphp.TagHandler import TagHandler
import sys
from colorama import init, Fore
from mutagen.flac import FLAC



init(autoreset=True)

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--retrieve', dest='retrieve', action='store_true')
parser.add_argument('--encode', dest='encode', action="store_true")
parser.add_argument('--v0', dest='v0', action='store_true')
parser.add_argument('--v2', dest='v2', action='store_true')
parser.add_argument('--320', dest='m320', action='store_true')
parser.add_argument('-i', dest='folder')
parser.add_argument('-o', dest='format')
parser.add_argument('--dry', dest="dry", action="store_true")
parser.add_argument("--ta", dest="artist")
parser.add_argument("--tl", dest="album")
parser.add_argument("--ty", dest="date")
parser.add_argument("--tg", dest="genre")


args = parser.parse_args()
def mkprogress(prefix):
    def progress(percent):
        msg = "Done!\n" if percent == 100 else "%d%%" % percent
        sys.stdout.write("\r%s%s" % (prefix, msg))
        sys.stdout.flush()
    return progress


if args.retrieve:
    c = Client("mcfitz2", "Cl0ser2g0d")
    c.login()
    c.retrieve(5)
elif args.encode and args.folder:
    folder = args.folder
    output = re.sub('/$', '', (args.format or os.path.basename(folder).strip() or folder)).lstrip()+"[%s]"
    if not os.path.exists(folder):
        raise Exception("Given path does not exist")
    if not os.path.isdir(folder):
        raise Exception("Given path is not a directory")
    to_remove = []
    for path,  directories, files in os.walk(folder):
        print Fore.YELLOW+"Processing directory %s" % path
        flac_files = sorted([f for f in files if f.endswith('.flac')])
        for i, f in enumerate(flac_files):
            print Fore.GREEN+"Processing file %d of %d: %s" % (i+1, len(flac_files)+1, f)
            root = folder
            relpath = os.path.join(path.replace(folder, ""), f)
            print "\tReading tags..."
            th = TagHandler(os.path.join(path, f), artist=args.artist, album=args.album, date=args.date, genre=args.genre)
            th.prompt()
            tag_args = th.gen_lame()
            flac = Flac(['-d', '-f'], os.path.join(path, f))
            infile = flac.run(mkprogress("\tDecompressing..."))
            to_remove.append(infile)
            
            if args.v0:
                outfile = os.path.join(output % "V0", re.sub("\.flac$", ".mp3",relpath))
                l = Lame(['-V0']+tag_args, infile, outfile)
                if not args.dry:
                    l.run(mkprogress("\tEncoding to V0..."))
            if args.v2:
                outfile = os.path.join(output % "V2", re.sub("\.flac$", ".mp3",relpath))
                l = Lame(['-V2']+tag_args, infile, outfile)
                if not args.dry:
                    l.run(mkprogress("\tEncoding to V2..."))
            if args.m320:
                outfile = os.path.join(output % "320", re.sub("\.flac$", ".mp3",relpath))
                l = Lame(['-b320']+tag_args, infile, outfile)
                if not args.dry:
                    l.run(mkprogress("\tEncoding to CBR320..."))
                        
    for filename in to_remove:
        os.remove(filename)
