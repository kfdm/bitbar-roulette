#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
import configparser
import logging
import os
import sys
from urllib.parse import urlparse

import requests

if 'BitBar' not in os.environ:
    logging.basicConfig(level=logging.DEBUG)
else:
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8')

config = configparser.ConfigParser()
config.read(os.path.expanduser('~/.bitbarrc'))

user = config['roulette'].pop('user')
token = config['roulette'].pop('token')
api = config['roulette'].pop('api', 'https://api.github.com/search/issues')


class Issue(object):
    def __init__(self, raw):
        self.raw = raw
    def __getitem__(self, key):
        return self.raw[key]
    @property
    def labels(self):
        if self.raw['labels']:
            return [x['name'] for x in self.raw['labels']]
        return ''
    @property
    def short(self):
        url = urlparse(i['html_url'])
        short, _ = url.path.strip('/').split('/issues')
        return short


print(':gun:')
for title, query in config['roulette'].items():
    print('---')
    result = requests.get(api,
        auth=(user, token),
        params={'q': query.strip('"').strip("'")}
    ).json()
    print(title,'(',len(result['items']),')', '| refresh=true')
    for i in sorted(result['items'], key=lambda x: x['html_url']):
        i = Issue(i)
        url = urlparse(i['html_url'])
        print(i.short, i['title'], i.labels, '|', 'href=' + i['html_url'])
