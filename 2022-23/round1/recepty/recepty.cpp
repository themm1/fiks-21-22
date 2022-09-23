#include <bits/stdc++.h>
using namespace std;

struct edge {
  string target;
  int needed_count;
};

struct node {
  vector<edge> edges;
  int produced_count;
  int wanted_count = 0;
};

int dfs(
    unordered_map<string, node> &graph, unordered_map<string, int> 
    &made_counts, string node, int in_edge_val, int total) {
  
  int total_before_dfs = total;
  for (auto e : graph[node].edges)
    if (made_counts[e.target] == -1) {
      total += dfs(graph, made_counts, e.target, e.needed_count, total);
    } else {
      total += made_counts[e.target] * e.needed_count;
    }
  int needed_count = total - total_before_dfs + graph[node].wanted_count;
  if (graph[node].produced_count == 0)
    return needed_count;
  int made_count = ceil(
    (float)needed_count / (float)graph[node].produced_count);
  made_counts[node] = made_count;
  return made_count * in_edge_val;
}

unordered_map<string, int> solve(unordered_map<string, node> &orig_graph) {
  // copies original graph, but without edges and collects raw materials
  set<string> raw_materials;
  unordered_map<string, node> graph;
  for (auto kv : orig_graph) {
    if (orig_graph[kv.first].produced_count == 0)
      raw_materials.insert(kv.first);
    graph[kv.first] = kv.second;
    graph[kv.first].edges = vector<edge>();
  }

  // makes reversed graph
  for (auto kv : orig_graph) {
    for (auto orig_edge : kv.second.edges) {
      edge new_edge = edge{kv.first, orig_edge.needed_count};
      graph[orig_edge.target].edges.push_back(new_edge);
    }
  }
  
  unordered_map<string, int> counts;
  for (auto raw_material : raw_materials) {
    unordered_map<string, int> made_counts;
    for (auto kv : graph)
      made_counts[kv.first] = -1;
    counts[raw_material] = dfs(graph, made_counts, raw_material, 1, 0);
  }
  return counts;
}

int main() {
  int u; cin >> u;
  for (int _ = 0; _ < u; _++) {
    int r; cin >> r;
    unordered_map<string, node> graph;
    for (int i = 0; i < r; i++) {
      int n; cin >> n;
      vector<edge> edges;
      for (int j = 0; j < n; j++) {
        int c; cin >> c;
        string s; cin >> s;
        edges.push_back(edge {s, c});
        if (graph.find(s) == graph.end())
          graph[s] = node {vector<edge>(), 0};
      }
      int c; cin >> c;
      string s; cin >> s;
      graph[s] = node {edges, c};
    }

    int p; cin >> p;
    for (int i = 0; i < p; i++) {
      int c; cin >> c;
      string s; cin >> s;
      graph[s].wanted_count = c;
    }
    // print_recipes(graph);
    unordered_map<string, int> answer = solve(graph);
    cout << answer.size() << endl;
    vector<string> answer_vector;
    for (auto kv : answer)
      answer_vector.push_back(kv.first);
    sort(answer_vector.begin(), answer_vector.end());
    for (auto raw_material: answer_vector)
      cout << answer[raw_material] << " " << raw_material << endl;
  }
}