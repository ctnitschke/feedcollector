"""
A simple program to dump updates from the same online feed into the same
file.

:copyright: (c) 2019 by Christian Thomas Nitschke
:license: Apache 2.0, see LICENSE for more details.
"""

import configparser
from email.utils import mktime_tz, parsedate_tz
import hashlib
import json
import os
import urllib

try:
    # Check if lxml is present (preferred for nicer namespace handling)
    import lxml.etree as ET
except ImportError:
    # Else fall back to python etree
    import xml.etree.ElementTree as ET

import requests

from . import rss
from . import rdf
from . import util

def main():
    
    try:
        datadir = os.path.join(os.environ['XDG_DATA_HOME'], 'feedcollector')
    except KeyError:
        datadir = os.path.join(os.environ['HOME'], '.local', 'share', 'feedcollector')

    if not os.path.isdir(datadir):
        os.mkdir(datadir)

    if os.path.isfile('feedcollector.opml'):
        config = ET.parse('feedcollector.opml')
    elif os.path.isfile(os.path.join(datadir, 'feedcollector.opml')):
        config = ET.parse(os.path.join(datadir, 'feedcollector.opml'))

    for feed in config.findall('.//outline[@xmlUrl]'):
        url = feed.attrib['xmlUrl']
        
        resp = requests.get(url)
        
        try:
            online_feed_tree = ET.ElementTree(ET.fromstring(resp.content))
            feed_type = ''
            root_tag = online_feed_tree.getroot().tag

            if 'rss' in root_tag.lower():
                feed_type = 'rss'
            elif 'rdf' in root_tag.lower():
                feed_type = 'rdf'
            elif 'feed' in root_tag.lower():
                feed_type = 'atom'
        except ET.ParseError:
            feed_type = 'json'
            
        if feed_type == 'rss':
            feed_url_parsed = urllib.parse.urlparse(url)
            feedname = util.build_filename_from_url(url)
            local_feed_filename = os.path.join(datadir, feedname + '.rss')

            if not os.path.isfile(local_feed_filename):
                online_feed_tree.write(local_feed_filename, encoding='utf-8')
            else:
                local_feed_tree = ET.parse(local_feed_filename)
                updated_feed_tree = rss.merge_feeds(online_feed_tree, local_feed_tree)
                updated_feed_tree.write(local_feed_filename, encoding='utf-8')

        elif feed_type == 'rdf':
            feed_url_parsed = urllib.parse.urlparse(url)
            feedname = util.build_filename_from_url(url)
            local_feed_filename = os.path.join(datadir, feedname + '.rss')

            if not os.path.isfile(local_feed_filename):
                online_feed_tree.write(local_feed_filename, encoding='utf-8')
            else:
                local_feed_tree = ET.parse(local_feed_filename)
                updated_feed_tree = rdf.merge_feeds(online_feed_tree, local_feed_tree)
                updated_feed_tree.write(local_feed_filename, encoding='utf-8')

if __name__ == '__main__':
    main()
