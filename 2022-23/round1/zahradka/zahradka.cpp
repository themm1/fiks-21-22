#include <bits/stdc++.h>
using namespace std;

void color_field(vector<vector<int>> &colored_grid, string axes, int i, int j,
                 int c) {
    colored_grid[i][j] = c;
    int n = colored_grid.size();
    if (axes.find('-') < axes.length() && colored_grid[n - i - 1][j] == -1)
        color_field(colored_grid, axes, n - i - 1, j, c);

    if (axes.find('|') < axes.length() && colored_grid[i][n - j - 1] == -1)
        color_field(colored_grid, axes, i, n - j - 1, c);

    if (axes.find("\\") < axes.length() && colored_grid[j][i] == -1)
        color_field(colored_grid, axes, j, i, c);

    if (axes.find('/') < axes.length() &&
        colored_grid[n - j - 1][n - i - 1] == -1)
        color_field(colored_grid, axes, n - j - 1, n - i - 1, c);
}

int fields_to_modify_per_color(vector<vector<int>> &grid,
                               vector<pair<int, int>> &v) {
    vector<int> values;
    for (int i = 0; i < v.size(); i++)
        values.push_back(grid[v[i].first][v[i].second]);
    unordered_map<int, int> values_counts;
    for (auto value : values)
        values_counts[value]++;

    int current_max = 0, sum = 0;
    for (auto key_value : values_counts) {
        if (key_value.second > current_max)
            current_max = key_value.second;
        sum += key_value.second;
    }
    return sum - current_max;
}

int solve(vector<vector<int>> &grid, string &axes) {
    int n = grid.size();
    // initialize colored grid
    vector<vector<int>> colored_grid;
    for (int i = 0; i < n; i++) {
        colored_grid.push_back(vector<int>{});
        for (int j = 0; j < n; j++)
            colored_grid[i].push_back(-1);
    }

    // color grid
    int color = 0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (colored_grid[i][j] == -1) {
                color_field(colored_grid, axes, i, j, color);
                color++;
            }
        }
    }
    // group same color fields together
    unordered_map<int, vector<pair<int, int>>> colors;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++)
            colors[colored_grid[i][j]].push_back(pair<int, int>(i, j));
    }

    // count fields that have to be modify in order for grid to be symmetric
    // on given axes
    int fields_to_modify = 0;
    for (auto key_value : colors) {
        fields_to_modify += fields_to_modify_per_color(grid, key_value.second);
    }
    return fields_to_modify;
}

int main() {
    int t;
    cin >> t;
    for (int _ = 0; _ < t; _++) {
        int s;
        cin >> s;
        string axis;
        cin >> axis;
        int n;
        vector<vector<int>> grid;
        cin >> n;
        int g;
        for (int i = 0; i < n; i++) {
            grid.push_back(vector<int>{});
            for (int j = 0; j < n; j++) {
                cin >> g;
                grid[i].push_back(g);
            }
        }
        int answer = solve(grid, axis);
        cout << answer << endl;
    }
}
