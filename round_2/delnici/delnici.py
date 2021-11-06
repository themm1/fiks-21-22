import math
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict


def main():
    with open("./round_2/delnici/io_example/input.txt", "r", encoding="utf-8") as f:
        lines = f.read()
        content = lines.split("\n")

    output = []
    current_row = 1
    while current_row + 1 < len(content):
        langs_count = int(content[current_row])
        trans_count = int(content[current_row+langs_count+1])
        task_end_row = current_row + langs_count + trans_count + 3
        translation = Translators(content[current_row:task_end_row+1])
        output.extend(translation.output)
        current_row = task_end_row

    with open("./round_2/delnici/output.txt", "w", encoding="utf-8", newline="") as f:
        f.writelines("\n".join(output))


class Translators:
    def __init__(self, content):
        self.content = content
        self.output = []

        self.langs_count = int(content[0])
        self.trans_count = int(content[self.langs_count+1])
        self.langs = [lang for lang in self.content[1:self.langs_count+1]]
        [self.start_lang, self.fin_lang] = content[self.langs_count+self.trans_count+2].split(" ")

        self.edges = defaultdict(lambda: math.inf)
        self.graph = {lang: {} for lang in self.langs}

        self.paths = {lang: {
            "price": math.inf, "path": [], "visited": False
        } for lang in self.langs}
        self.paths[self.start_lang]['price'] = 0
        self.populate_graph()
        self.populate_paths(self.start_lang)

        self.result = self.paths[self.fin_lang]
        if self.result['path']:
            self.result['path'].append(self.fin_lang)
        # self.check_result(only_on_diff_results=True)

        self.populate_output()

    def populate_graph(self):
        for translator in self.content[self.langs_count+2:self.langs_count+self.trans_count+2]:
            line = translator.split(" ")
            price = int(line[1])

            for i in range(2, len(line)-1):
                for j in range(i+1, len(line)):
                    if self.edges[(line[i], line[j])] > price:

                        self.edges[(line[i], line[j])] = price
                        self.graph[line[i]][line[j]] = price
                        self.graph[line[j]][line[i]] = price

                    if self.edges[(line[j], line[i])] < self.edges[(line[i], line[j])]:

                        self.edges[(line[i], line[j])] = self.edges[(line[j], line[i])]
                        self.graph[line[i]][line[j]] = self.edges[(line[j], line[i])]
                        self.graph[line[j]][line[i]] = self.edges[(line[j], line[i])]

                        self.edges.pop((line[j], line[i]))

                    if self.edges[(line[j], line[i])] > self.edges[(line[i], line[j])]:
                        self.edges.pop((line[j], line[i]))

        self.edges = {key: val for key, val in self.edges.items() if val != math.inf}

    def populate_paths(self, current_lang):
        self.paths[current_lang]['visited'] = True

        for lang, price in self.graph[current_lang].items():
            if self.paths[lang]['price'] > self.paths[current_lang]['price'] + price:
                self.paths[lang]['price'] = self.paths[current_lang]['price'] + price

                self.paths[lang]['path'] = []
                self.paths[lang]['path'].extend(self.paths[current_lang]['path'])
                self.paths[lang]['path'].append(current_lang)
                
        next_lang = self.min_distance()
        if next_lang != None:
            self.populate_paths(next_lang)

    def min_distance(self):
        min_dist_lang = None
        for lang, info in self.paths.items():
            if not info['visited']:
                if min_dist_lang == None or info['price'] < self.paths[min_dist_lang]['price']:
                    min_dist_lang = lang
        return min_dist_lang

    def populate_output(self):
        if self.result['price'] != math.inf:
            self.output.append(f"To nas bude stat {self.result['price']},-.")
            self.output.append(f"Pocet prekladu: {len(self.result['path'])-1}.")
            for lang in self.result['path']:
                self.output.append(lang)
            # pprint(output[-len(paths[fin_lang]['path'])-3:])
        else:
            self.output.append("Takove prekladatele nemame.")
            # pprint(output[-1])

    def check_result(self, show_plot=True, only_on_diff_results=True):
        shortest = self.create_networkx_graph()
        shortest_dist = self.shortest_path_price()

        if shortest != self.result['path'] and \
            shortest_dist != self.result['price']:
            print("my:", self.result['path'], ",", self.result['price'])
            print("networkx:", shortest, ",", shortest_dist)
            if show_plot and only_on_diff_results:
                plt.show()
        if show_plot and not only_on_diff_results:
            plt.show()

    def create_networkx_graph(self):
        G = nx.Graph()
        for lang in self.langs:
            G.add_node(lang)

        for key, value in self.edges.items():
            G.add_edge(key[0], key[1], color="black", weight=value)

        pos = nx.spring_layout(G)
        labels = nx.get_edge_attributes(G, "weight")
        nx.draw(G, pos, with_labels=True)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        try:
            shortest_path = nx.shortest_path(G, source=self.start_lang, target=self.fin_lang, weight="weight")
            path_edges = list(zip(shortest_path, shortest_path[1:]))
            nx.draw_networkx_nodes(G, pos, nodelist=shortest_path, node_color="r")
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="r", width=10)
            plt.axis("equal")
        except Exception:
            shortest_path = []
            nx.draw_networkx_nodes(G, pos, nodelist=[self.start_lang, self.fin_lang], node_color="r")

        return shortest_path

    def shortest_path_price(self):
        price_sum = 0
        if self.result['path']:
            prev_lang = self.result['path'][0]
            for lang in self.result['path'][1:]:
                price_sum += self.graph[prev_lang][lang]
                prev_lang = lang
            return price_sum
        return math.inf


if __name__ == "__main__":
    main()