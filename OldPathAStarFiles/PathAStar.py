class AStar:
    def __init__(self, graph):
        self.graph = graph

    def search(self, start_node, goal_node):
        open_set = {start_node}
        closed_set = set()

        while open_set:
            current_node = min(open_set, key=lambda node: node.f)
            if current_node == goal_node:
                # Reconstruct the path
                path = []
                while current_node:
                    path.append(current_node)
                    current_node = current_node.parent
                return path[::-1]  # Reverse the path
            open_set.remove(current_node)
            closed_set.add(current_node)

            for neighbor in current_node.neighbors:
                if neighbor in closed_set:
                    continue
                tentative_g_score = current_node.g + 1  # Assuming cost of moving from one node to another is 1
                if neighbor not in open_set or tentative_g_score < neighbor.g:
                    neighbor.parent = current_node
                    neighbor.g = tentative_g_score
                    neighbor.h = neighbor.heuristic(goal_node)
                    neighbor.f = neighbor.g + neighbor.h
                    if neighbor not in open_set:
                        open_set.add(neighbor)

        # If open_set is empty but goal was not reached
        return None