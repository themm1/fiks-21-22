import random
from pprint import pprint

def main():
    max_dif = 3
    for _ in range(1):
        input_arr = generate_input(10000, 200)
        input_arr = [2, 5, 6]
        input_arr.sort()
        # print(input_arr)
        group_best(input_arr, max_dif)
        # print()

def group_best(input_arr, max_dif):
    best_groups = [input_arr]
    for i in range(len(input_arr)):
        counter = 0
        groups = group_arr(input_arr[:i], max_dif)
        groups.extend(group_arr(input_arr[i:], max_dif))
        print(groups)
        if len(groups) < len(best_groups):
            counter += 1
            best_groups = groups
        if counter > 1:
            print(input_arr)
            pprint(groups)

def group_arr(input_arr, max_dif):
    groups = []
    if input_arr:
        min_num_index, min_num = 0, input_arr[0]

    for i, num in enumerate(input_arr):
        if num - min_num > max_dif:
            groups.append(input_arr[min_num_index:i])
            min_num, min_num_index = num, i
        if i == len(input_arr) - 1:
            groups.append(input_arr[min_num_index:])
    return groups

def generate_input(max_num, count):
    return [random.randint(0, max_num) for _ in range(count)]


if __name__ == "__main__":
    main()