from collections import defaultdict

def main(filename, outputfile):
    with open(filename, "r") as f:
        content = f.read().split("\n")
    
    [nations_count, days_count] = [int(item) for item in content[0].split(" ")]
    edges = defaultdict(list)
    for pair in content[1:nations_count]:
        [start, target] = [int(item) for item in pair.split(" ")]
        edges[start].append(target)
        edges[target].append(start)

    g = Graph(edges, nations_count)

    with open(outputfile, "w", newline="") as f:
        for i, question in enumerate(content[nations_count:]):
            nodes = [int(node) for node in question.split(" ")[1:]]
            initial_dist = sum([g.tree[node].height for node in nodes])
            weighted_nodes = g.weight_tree_nodes(nodes)
            best_dist = g.find_best_dist(weighted_nodes, initial_dist, len(nodes))
            f.write(str(initial_dist - best_dist) + "\n")


class Node:
    def __init__(self, node, height, parent, connected_nodes):
        self.node = node
        self.height = height
        self.parent = parent
        if node != parent:
            connected_nodes.remove(parent)
        self.children = connected_nodes

    def __repr__(self):
        return str(self.__dict__)


class Graph:
    def __init__(self, edges, nodes_count):
        self.nodes = range(1, nodes_count+1)
        self.edges = edges
        self.tree = self.populate_tree({}, 1, 1, 0, {node: False for node in self.nodes})

    def populate_tree(self, tree, parent_node, current_node, height, visited):
        visited[current_node] = True
        tree[current_node] = Node(
            current_node, height, parent_node, list(self.edges[current_node])
        )
        for node in self.edges[current_node]:
            if not visited[node]:
                self.populate_tree(tree, current_node, node, height+1, visited)
        height -= 1
        return tree

    def weight_tree_nodes(self, nodes):
        wighted_nodes = defaultdict(lambda: 0)
        for start_node in nodes:
            current_node = start_node
            while True:
                wighted_nodes[current_node] += 1
                if current_node == 1:
                    break
                current_node = self.tree[current_node].parent
        return wighted_nodes

    def find_best_dist(self, weighted_nodes, current_dist, special_nodes_count):
        current_node = 1
        distances = {node: None for node in weighted_nodes}
        visited = {node: False for node in weighted_nodes}

        distances[current_node] = current_dist
        visited[current_node] = True
        visited_count = 1

        while visited_count < len(weighted_nodes):
            if not visited[current_node]:
                prev_dist = distances[self.tree[current_node].parent]
                current_dist = prev_dist - (2 * weighted_nodes[current_node]) + special_nodes_count
                distances[current_node] = current_dist
                visited_count += 1
                visited[current_node] = True
            for node in self.tree[current_node].children:
                if visited.get(node) == False:
                    current_node = node
                    break
            else:
                current_node = self.tree[current_node].parent
        return min(distances.values())


if __name__ == "__main__":
    main("./round_4/krmeni/input.txt", "./round_4/krmeni/output.txt")