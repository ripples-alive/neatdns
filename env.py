import json
import os
import socket

import requests

ALEXA_TOP_1M_URL = 'https://s3.amazonaws.com/alexa-static/top-1m.csv.zip'

if os.path.exists('config.json'):
    with open('config.json', 'r') as f:
        config = json.load(f)
    TMP_FOLDER = config['TMP_FOLDER']
    POISONING_DOMAINS_LIST = config['POISONING_DOMAINS_LIST']
    BIND_QUEEY_LOG_PATH = config['BIND_QUEEY_LOG_PATH']
    BIND_RESOLVE_LOG_PATH = config['BIND_RESOLVE_LOG_PATH']
else:
    TMP_FOLDER = '/tmp/neatdns_new'
    POISONING_DOMAINS_LIST = 'domain_list_poisoning.json'
    BIND_QUEEY_LOG_PATH = '/tmp/named/query.log'
    BIND_RESOLVE_LOG_PATH = '/tmp/named/resolver.log'

TLD_LIST_PATH = os.path.join(TMP_FOLDER, 'tld_list.json')

if not os.path.exists(TMP_FOLDER):
    os.mkdir(TMP_FOLDER, 0o700)

if not os.path.exists(POISONING_DOMAINS_LIST):
    with open(POISONING_DOMAINS_LIST, 'w') as f:
        f.write('[]')

if os.path.exists(TLD_LIST_PATH):
    with open(TLD_LIST_PATH, 'r') as f:
        TLD_LIST = json.load(f)
else:
    resp = requests.get('https://data.iana.org/TLD/tlds-alpha-by-domain.txt')
    lines = resp.text.splitlines()
    lines.pop(0)
    TLD_LIST = [x.lower() for x in lines]
    with open(TLD_LIST_PATH, 'w') as f:
        json.dump(TLD_LIST, f)

nameserver_config = 'nameserver %s\n' % socket.gethostbyname('example.com')
RESOLVE_CONF_FNAME = os.path.join(TMP_FOLDER, 'resolv.conf')
with open(RESOLVE_CONF_FNAME, 'w') as f:
    f.write(nameserver_config)
