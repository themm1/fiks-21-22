from decimal import Decimal

def main(input_file, output_file):
    with open(input_file, "r") as f:
        content = f.read().split("\n")

    output = []
    tasks_count = int(content[0])
    for task in content[1:tasks_count+1]:
        args = [int(arg) for arg in task.split(" ")]
        result = get_fields_count(*args)
        output.append(str(result))
    
    with open(output_file, "w", newline="") as f:
        f.writelines("\n".join(output))

def get_fields_count(x_size, y_size, x_coord, y_coord, layers_count):
    max_directions = [
        x_coord,                # max_left
        y_size - y_coord - 1,   # max_up
        x_size - x_coord - 1,   # max_right
        y_coord                 # mar_down
    ]

    fields = (layers_count + 1) ** 2

    for i, max_dir in enumerate(max_directions):
        pyramid_height = layers_count - max_dir
        if pyramid_height > 0:
            fields -= int(Decimal(pyramid_height) * (Decimal(pyramid_height) + 1) / 2)

        second_index = i + 1
        if second_index == len(max_directions):
            second_index = 0
        height = (max_dir + 1) + (max_directions[second_index] + 1)
        n = layers_count - height + 2
        if n > 0:
            fields += seq_formula(n)

    return fields

def seq_formula(n):
    m = int(n / 2)
    if n % 2 == 0:
        return m * (m - 1) + m
    else:
        return m * (m + 1)

if __name__ == "__main__":
    main("./round_3/sloni/io_example/input.txt", "./round_3/sloni/output.txt")