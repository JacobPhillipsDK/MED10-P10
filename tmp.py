import xml.etree.ElementTree as ET
from collections import deque
from math import sqrt
import osmnx as ox

def parse_osm_xml(file_path):
    """
    Parse the OSM XML file and return a dictionary of nodes and a list of ways.
    """
    nodes = {}
    ways = []

    tree = ET.parse(file_path)
    root = tree.getroot()

    for node in root.iter('node'):
        node_id = int(node.attrib['id'])
        lat = float(node.attrib['lat'])
        lon = float(node.attrib['lon'])
        nodes[node_id] = (lat, lon)

    for way in root.iter('way'):
        way_nodes = []
        for nd in way.iter('nd'):
            node_id = int(nd.attrib['ref'])
            if node_id in nodes:
                way_nodes.append(node_id)

        if way_nodes:
            highway = None
            for tag in way.iter('tag'):
                if tag.attrib['k'] == 'highway':
                    highway = tag.attrib['v']
                    break

            if highway in ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'unclassified', 'residential']:
                ways.append((way_nodes, highway))

    return nodes, ways


class Node:
    def __init__(self, node_id, lat, lon):
        self.node_id = node_id
        self.lat = lat
        self.lon = lon
        self.edges = []


    def add_edge(self, edge):
        self.edges.append(edge)
