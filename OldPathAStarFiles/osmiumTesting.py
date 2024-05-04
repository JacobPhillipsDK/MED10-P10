import osmium
from collections import Counter
from Node import Node


class TagHandler(osmium.SimpleHandler):
    def __init__(self, tags, osm_file):
        super(TagHandler, self).__init__()
        self.nodes = []
        self.node_nodes = []
        self.node_ids = {}

        self.tags = tags
        self.load_file(osm_file)

    @staticmethod
    def filter_out(tag, value):
        # Define the tags you want to filter out
        filter_out_tags = [("highway", "traffic_signals"), ("highway", "emergency_access_point"),
                           ("highway", "elevator"),
                           ("highway", "elevator"), ("highway", "bus_stop"), ("highway", "service"),
                           ("highway", "street_lamp"), ("highway", "give_way")]
        return (tag, value) in filter_out_tags

    def load_file(self, osm_filename):
        self.apply_file(osm_filename)

    def node(self, n):
        for tag in self.tags:
            if tag in n.tags:
                if self.filter_out(tag, n.tags[tag]):
                    continue
                # node = Node(n.location.lat, n.location.lon, n.id)
                #                 # self.node_ids[n.id] = node
                self.nodes.append((tag, n.tags[tag]))
                node = Node(n.location.lat, n.location.lon, n.id)
                node.random_cost()
                node.tags = n.tags[tag]
                self.node_nodes.append(node)

    def way(self, o):
        for tag in self.tags:
            if tag in o.tags:
                if self.filter_out(tag, o.tags[tag]):
                    continue
                if o.id not in self.node_ids:
                    # If the way node is not yet in node_ids, create a new Node instance
                    node = Node(0, 0, o.id)  # Use dummy coordinates
                    self.nodes.append(node)
                    self.node_ids[o.id] = node
                else:
                    # If the way node is already in node_ids, fetch it
                    node = self.node_ids[o.id]
                node.tags = o.tags[tag]

    def relation(self, o):
        for tag in self.tags:
            if tag in o.tags:
                if self.filter_out(tag, o.tags[tag]):
                    continue
                if o.id not in self.node_ids:
                    # If the relation node is not yet in node_ids, create a new Node instance
                    node = Node(0, 0, o.id)  # Use dummy coordinates
                    self.nodes.append(node)
                    self.node_ids[o.id] = node
                else:
                    # If the relation node is already in node_ids, fetch it
                    node = self.node_ids[o.id]
                node.tags = o.tags[tag]


def main():
    tags_to_search = ["footway", "highway"]
    osm_filename = "../bounding_box_map_aalborg.osm.pbf"

    tag_handler = TagHandler(tags_to_search, osm_filename)


    print(f'Total number of nodes: {len(tag_handler.nodes)}')
    print(f"Total number of nodes_nodes: {len(tag_handler.node_nodes)}")

    # # Count all the tags
    # all_tags_counter = Counter(items)
    # for tag_value, count in all_tags_counter.items():
    #     tag, value = tag_value
    #     print(f"{tag}={value}: {count}")
    # print(f'Total number of tags: {len(items)}')
    #

if __name__ == "__main__":
    main()
