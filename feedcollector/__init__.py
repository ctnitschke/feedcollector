"""
Utility functions for merging feeds.
"""
from email.utils import mktime_tz, parsedate_tz
import hashlib
import json


try:
    # Check if lxml is present (preferred for nicer namespace handling)
    import lxml.etree as ET
except ImportError:
    # Else fall back to python etree
    import xml.etree.ElementTree as ET

def hash_feed_entry(entry):
    """
    Hash an xml subtree (a feed item).

    Args:
        entry: xml.etree.ElementTree.Element containing the subtree to hash.
    
    Returns:
        bytes containing the sha256 hash of the Element including its subtree.
    """
    m = hashlib.sha256()
    entry_bytes = ET.tostring(entry)
    m.update(entry_bytes)
    return m.digest()
        
def merge_rss_feeds(new_root, old_root):
    """
    Merge two rss feeds contained in xml.etree.ElementTree.ElementTrees.

    Args:
        new_root: xml.etree.ElementTree.ElementTree containing the
            rss feed considered as new.
        old_root: xml.etree.ElementTree.ElementTree containing the
            rss feed considered as reference.
    Returns:
        xml.etree.ElementTree.ElementTree with the merged rss feed,
        containing both old and new elements.
    """
    
    old_channel = old_root.find('channel')
    new_channel = new_root.find('channel')

    # Get guids for items that have it, else build item hash
    new_channel_guids = set()
    new_channel_hashes = set()

    for item in new_channel.findall('item'):
        guid = item.find('guid')

        if guid is not None:
            new_channel_guids.add(guid.text)
        else:
            digest = hash_feed_entry(item)
            new_channel_hashes.add(digest)
    
    for item in old_channel.findall('item'):

        # Check if item guid is present
        guid = item.find('guid')

        # If the item has a guid...
        if guid is not None:
            # ...and it is not in the new channel...
            if guid.text not in new_channel_guids:
                # ... append the item
                new_channel.append(item)
        # If not...
        else:
            # hash the damn thing...
            old_channel_hash = hash_feed_entry(item)
            # ... and if it's not in our safety net set...
            if old_channel_hash not in new_channel_hashes:
                # ... add it.
                new_channel.append(item)
                    
    return new_root


