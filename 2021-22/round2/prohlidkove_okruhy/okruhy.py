def main():
    [crossroads_count, roads_count, questions_count] = [int(num) 
        for num in input().split(" ")]

    edges = {str(i): [] for i in range(1, crossroads_count+1)}
    nodes = list(edges.keys())
    for _ in range(roads_count):
        [start_edge, target_edge] = input().split(" ")
        edges[start_edge].append(target_edge)
    questions = [(input().split(" ")) for _ in range(questions_count)]

    g = Graph(nodes, edges)
    g.set_group_to_every_node()
    connected_groups = g.find_connections_between_groups()

    for start, target in questions:
        if connected_groups[(g.nodes_groups[start], g.nodes_groups[target])]:
            print("Cesta existuje")
        else:
            print("Cesta neexistuje")


class Graph:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        self.reversed_edges = self.reverse_edges()
        self.nodes_groups = {node: None for node in self.nodes}

    def set_group_to_every_node(self):
        current_circuit = 0
        while current_circuit < len(self.nodes):
            # find starting node if possible
            starting_node = None
            for node in self.nodes:
                if not self.nodes_groups[node]:
                    starting_node = self.nodes[int(node)-1]
                    break
            if not starting_node:
                break
            # dict with visited nodes
            visited = {node: False for node in self.nodes}
            # list with all reachable nodes from starting_node
            stack = self.dfs(self.edges, starting_node, visited, [])

            # mark nodes that are unreachable from starting_node in original graph
            not_reachable = {node: True for node in self.nodes}
            for node in stack:
                not_reachable[node] = False
            
            # set current_circuit to all nodes that are reachable in both reversed
            # and original graph with current starting node aka are strongly connected
            for node in stack:
                if not not_reachable[node] and not self.nodes_groups[node]:
                    current_circuit += 1
                    self.dfs(self.reversed_edges, node, not_reachable, [],
                        circuit=current_circuit)

    def find_connections_between_groups(self):
        # create combinations of connections between groups when
        # there are always 3 groups
        connected_groups = {}
        for i in range(1, 4):
            for j in range(1, 4):
                connected_groups[(i, j)] = True if i == j else False
    
        # set all connected groups by looping through all edges
        for node, connected_nodes in self.edges.items():
            for connected_node in connected_nodes:
                connected_groups[(self.nodes_groups[node],
                    self.nodes_groups[connected_node])] = True
        return connected_groups

    def dfs(self, edges, current_node, visited, stack, circuit=None):
        stack.append(current_node)
        if circuit:
            self.nodes_groups[current_node] = circuit
        visited[current_node] = True
        for node in edges[current_node]:
            if not visited[node] and not self.nodes_groups[node]:
                self.dfs(edges, node, visited, stack, circuit)
        return stack

    def reverse_edges(self):
        reversed_edges = {node: [] for node in self.nodes}
        for node, connected_nodes in self.edges.items():
            for connected_node in connected_nodes:
                reversed_edges[connected_node].append(node)
        return reversed_edges


if __name__ == "__main__":
    main()