import requests
import re
import sys
from bs4 import BeautifulSoup as BS


class Client:
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.session = requests.session()
    def login(self):
        sys.stdout.write("Logging in...")
        sys.stdout.flush()
        self.session.post("https://ssl.what.cd/login.php", data={"username":"mcfitz2", "password":"Cl0ser2g0d"})
        sys.stdout.write("Done!\n")
    def retrieve(self, num, destination=None):
        html = BS(self.session.get("https://ssl.what.cd/better.php",params={"method":"transcode", "type":"3"}).text)
        cd = re.compile('\w+; filename="(.+\.torrent)"')
        i = 0
        for tr in html.findAll('tr'):
            if i > 5:
                break
            artist = tr.td.find('a', {"href":re.compile(r"artist.php.+")})
            if artist:
                try:
                    url = dict(tr.td.find('a', {"href":re.compile(r"torrents.php\?action=download"),"title":"Download" }).attrs)['href']
                    r = requests.get("http://what.cd/%s" % url)
                    base_filename = filename = cd.match(r.headers['Content-Disposition']).group(1)
                    if destination:
                        filename = os.path.join(destination, base_filename)
                    print "Retrieving %s"  % base_filename
                    with open(filename, 'wb') as torrent:
                        torrent.write(r.content)
                        i += 1
                except UnicodeEncodeError:
                    continue
                except AttributeError:
                    continue
