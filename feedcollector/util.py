"""
Utility functions
"""
import hashlib
import string
from urllib.parse import urlparse

try:
    # Check if lxml is present (preferred for nicer namespace handling)
    import lxml.etree as ET
except ImportError:
    # Else fall back to python etree
    import xml.etree.ElementTree as ET

def hash_xml_subtree(subtree):
    """
    Hash an xml subtree (such as a feed item).

    Args:
        subtree: xml.etree.ElementTree.Element containing the subtree to hash.
    
    Returns:
        bytes containing the sha256 hash of the Element including its subtree.
    """
    m = hashlib.sha256()
    subtree_bytes = ET.tostring(subtree)
    m.update(subtree_bytes)
    return m.digest()

def build_filename_from_url(
        url
):
    """
    Turn feed url into a useful filename

    Args:
        url: feed url string

    Returns:
        filename-safe unique string derived from url
    """
    parsed_url = urlparse(url)

    m = hashlib.sha256()
    m.update(url.encode('utf-8'))

    url_noport = parsed_url.netloc.partition(':')[0]
    return url_noport + '-' + m.hexdigest()
