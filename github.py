#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
import configparser
import logging
import os
import sys
from urllib.parse import urlparse, urlencode

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
link = config['roulette'].pop('link', 'https://github.com/issues')


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


print(':slot_machine:')
for title, query in config['roulette'].items():
    params={'q': query.strip('"').strip("'")}
    print('---')
    result = requests.get(api,
        auth=(user, token),
        params=params
    ).json()
    print(title,'(',len(result['items']),')', '| refresh=true')
    print(query, '| alternate=true href={}?{}'.format(link, urlencode(params)))
    for i in sorted(result['items'], key=lambda x: x['html_url']):
        i = Issue(i)
        url = urlparse(i['html_url'])
        print(i.short, i['title'], i.labels, '|', 'href=' + i['html_url'])
