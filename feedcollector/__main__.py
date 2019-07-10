"""
A simple program to dump updates from the same online feed into the same
file.
"""

import configparser
from email.utils import mktime_tz, parsedate_tz
import hashlib
import json
import os

try:
    # Check if lxml is present (preferred for nicer namespace handling)
    import lxml.etree as ET
except ImportError:
    # Else fall back to python etree
    import xml.etree.ElementTree as ET

import requests


from . import merge_rss_feeds

def main():
    try:
        confdir = os.environ['XDG_CONFIG_HOME']
    except KeyError:
        confdir = os.path.join(os.environ['HOME'], '.config')

    try:
        datadir = os.path.join(os.environ['XDG_DATA_HOME'], 'feedcollector')
    except KeyError:
        datadir = os.path.join(os.environ['HOME'], '.local', 'share', 'feedcollector')

    if not os.path.isdir(datadir):
        os.mkdir(datadir)
        
    config = configparser.ConfigParser()

    if os.path.isfile('feedcollector.conf'):
        config.read('feedcollector.conf')
    elif os.path.isfile(os.path.join(confdir, 'feedcollector.conf')):
        config.read(os.path.join(confdir, 'feedcollector.conf'))

    for feed in config.sections():
        url = config.get(feed, 'url')
        feed_type = config.get(feed, 'type')
        
        resp = requests.get(url)
        
        if feed_type == 'rss':
            online_feed_tree = ET.fromstring(resp.content)

            local_feed_filename = os.path.join(datadir, feed + '.rss')

            if not os.path.isfile(local_feed_filename):
                ET.ElementTree(online_feed_tree).write(local_feed_filename, encoding='utf-8')
            else:
                local_feed_tree = ET.parse(local_feed_filename)

                updated_feed_tree = merge_rss_feeds(online_feed_tree, local_feed_tree)
                ET.ElementTree(updated_feed_tree).write(local_feed_filename, encoding='utf-8')

if __name__ == '__main__':
    main()
