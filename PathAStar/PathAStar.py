from collections import deque
import math

class AStarPathfinder:
    def __init__(self, graph):
        self.graph = graph

    def heuristic(self, node1, node2):
        """Euclidean distance heuristic"""
        return math.sqrt((node1.latitude - node2.latitude) ** 2 + (node1.longitude - node2.longitude) ** 2)

    def find_path(self, start_node, end_node, is_drivable=True):
        open_set = deque([(0, start_node)])
        closed_set = set()
        start_node.g = 0
        start_node.calculate_total_cost()

        while open_set:
            current_node = open_set.popleft()[1]

            if current_node == end_node:
                path = self.reconstruct_path(current_node)
                return path

            closed_set.add(current_node)

            for neighbor in current_node.neighbors:
                if neighbor in closed_set:
                    continue

                if is_drivable and 'highway' not in neighbor.tags:
                    continue

                tentative_g_cost = current_node.g + self.heuristic(current_node, neighbor)

                if neighbor not in open_set or tentative_g_cost < neighbor.g:
                    neighbor.parent = current_node
                    neighbor.g = tentative_g_cost
                    neighbor.h = self.heuristic(neighbor, end_node)
                    neighbor.calculate_total_cost()

                    if neighbor not in open_set:
                        open_set.append((neighbor.f, neighbor))

        return None

    def reconstruct_path(self, end_node):
        path = []
        node = end_node
        while node:
            path.append(node)
            node = node.parent
        return list(reversed(path))