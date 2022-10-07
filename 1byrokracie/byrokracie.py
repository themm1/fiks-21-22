def main(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as input_file:
        content = input_file.read()
        content_list = content.split("\n")
        content_list = [line for line in content_list if line != ""]
        
    output = []
    i = 0
    while i + 1 < len(content_list):
        task_header = content_list[i+1].split(" ")
        [perm_numbers, rows, final_perm] = [int(item) for item in task_header]

        permissions = [perm.split(" ") for perm in content_list[i+2:i+rows+2]]

        dependecies = get_dependencies(permissions, perm_numbers)
        visited = [False for _ in range(perm_numbers)]
        ordered_permissions, cyclic = dfs([], dependecies, final_perm, visited)
        if cyclic:
            output.append("ajajaj")
        else:
            output.append("pujde to " + " ".join(ordered_permissions))
        i += rows + 1
    
    with open(output_file, "w", encoding="utf-8") as output_file:
        output_file.write("\n".join(output))


def get_dependencies(permissions, perm_numbers):
    dependecies = {i: [] for i in range(perm_numbers)}
    for perm_pair in permissions:
        dependecies[int(perm_pair[0])].append(int(perm_pair[1]))
    return dependecies

def dfs(ordered_permissions, dependecies, cur_perm, visited, cyclic=False):
    visited[cur_perm] = True
    for perm in dependecies[cur_perm]:
        if visited[perm] and str(perm) not in ordered_permissions:
            cyclic = True
        elif not visited[perm]:
            cyclic = dfs(ordered_permissions, dependecies, perm, visited, cyclic=cyclic)[1]
    if cyclic:
        return [], True
    ordered_permissions.append(str(cur_perm))
    return ordered_permissions, cyclic

if __name__ == "__main__":
    main("./round_1/byrokracie/io_example/input.txt",
        "./round_1/byrokracie/output.txt")