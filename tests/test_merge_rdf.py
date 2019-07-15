import pytest

try:
    from lxml.etree import ElementTree as ET
except ImportError:
    from xml.etree import ElementTree as ET

import feedcollector

def test_merge():
    old_tree = ET.parse('tests/data/rdf-old.rss')
    new_tree = ET.parse('tests/data/rdf-new.rss')

    merged_tree = feedcollector.rdf.merge_feeds(new_tree, old_tree)
    output_string = ET.tostring(merged_tree.getroot(), encoding='unicode')

    assert 'first' in output_string
    assert 'second' in output_string
    assert 'third' in output_string
    assert 'fourth' in output_string
    assert 'fifth' in output_string
    assert 'sixth' in output_string
    assert 'seventh' in output_string
