#!/usr/bin/env python3
import os
import sys
import requests
from bs4 import BeautifulSoup
import urllib.parse
import getpass
import argparse


class Maktabkhooneh:
    def __init__(self, u, p):
        self.u = u
        self.p = p
        self.socket = requests.Session()

    def login(self):
        email = self.u
        passwd = self.p
    
        ua = r"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)" \
             r" Chrome/69.0.3497.100 Safari/537.36 OPR/56.0.3051.52"
    
        s = self.socket

        s.headers.update({'User-Agent': ua,
                          'Host': 'maktabkhooneh.org',
                          'origin': 'https://maktabkhooneh.org',
                          'Referer': 'https://maktabkhooneh.org/'})
    
        r = s.get('https://maktabkhooneh.org')
        b = BeautifulSoup(r.text, 'html.parser')
        data = {
            'csrfmiddlewaretoken': b.select('input[name=csrfmiddlewaretoken]')[0]['value'],
            'email': email,
            'password': passwd
        }
        h = {
            'X-Requested-With': 'XMLHttpRequest',
            'Pragma': 'no-cache'
        }
        r = s.post('https://maktabkhooneh.org/login', data=data, headers=h)
        res = r.json()
        if res['status'] == 'success':
            return True
        return False
   
    def get_links(self, url):
        content = self.socket.get(url).text
        soup = BeautifulSoup(content, 'html.parser')
        links = soup.select('a.lesson-links')
        for link in links:
            u = urllib.parse.urljoin(url, link['href'])
            s_content = self.socket.get(u).text
            s_soup = BeautifulSoup(s_content, 'html.parser')
            hq_dlink = s_soup.select('a.hq-video-dl')
            lq_dlink = s_soup.select('a.video-dl')
            if len(hq_dlink) > 0:
                dlink = hq_dlink[0]
            else:
                dlink = lq_dlink[0]
            print(dlink['href'])


def main():
    parser = argparse.ArgumentParser(description='Get maktabkhooneh.com download links')
    parser.add_argument('urls', metavar='urls', type=str, nargs='+',
                        help='URLs to courses')
    parser.add_argument('-u', '--username', dest='username', action='store', help='Username', required=True)
    parser.add_argument('-p', '--password', dest='passwd', action='store', default=None, help='Username')

    args = parser.parse_args()
    passwd = args.passwd
    if passwd is None:
        getpass.getpass("Password: ")

    M = Maktabkhooneh(args.username, passwd)
    if not M.login():
        print("Bad User/Password", file=sys.stderr)
        exit(os.EX_DATAERR)

    for url in args.urls:
        M.get_links(url)
     

if __name__ == "__main__":
    main()
