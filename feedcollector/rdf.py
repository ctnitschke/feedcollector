"""
Module for handling of RSS (as in RDF Site Summary) feeds

:copyright: (c) 2019 by Christian Thomas Nitschke
:license: Apache 2.0, see LICENSE for more details.
"""
try:
    # Check if lxml is present (preferred for nicer namespace handling)
    import lxml.etree as ET
except ImportError:
    # Else fall back to python etree
    import xml.etree.ElementTree as ET


def merge_feeds(new_root, old_root):
    """
    Merge two rdf RSS feeds contained in xml.etree.ElementTree.ElementTrees.

    Args:
        new_root: xml.etree.ElementTree.ElementTree containing the
            rss feed considered as new.
        old_root: xml.etree.ElementTree.ElementTree containing the
            rss feed considered as reference.
    Returns:
        xml.etree.ElementTree.ElementTree with the merged feed,
        containing both old and new elements.
    """

    new_item_ids = set()

    new_root_elem = new_root.getroot()
    
    new_item_seq = new_root.find((
        '{http://purl.org/rss/1.0/}channel/'
        '{http://purl.org/rss/1.0/}items/'
        '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Seq'
    ))
    
    for item in new_root.findall('{http://purl.org/rss/1.0/}item'):
        new_item_ids.add(item.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about'])

    for item in old_root.findall('{http://purl.org/rss/1.0/}item'):
        item_id = item.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about']

        if item_id not in new_item_ids:
            new_root_elem.append(item)
            ET.SubElement(
                new_item_seq,
                '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}li',
                {
                    '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource':
                    item_id,
                })

    return new_root
