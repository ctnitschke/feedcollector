"""
Utility functions
"""
import hashlib

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
