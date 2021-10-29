import random
from pprint import pprint

def generate_input(animals_count_range, sponsors_offset, max_sponsored_animals_ratio):
    animals_ids = read_txt("animals.txt")
    sponsors_names = read_txt("sponsors.txt")

    animals_count = random.randint(animals_count_range[0], animals_count_range[1])
    sponsors_count = random.randint(animals_count-sponsors_offset, animals_count+sponsors_offset)

    animals = {}
    i = 0
    possible_choices = animals_ids
    for _ in range(animals_count):
        choice = random.choice(possible_choices)
        animals[str(i)] = str(choice)
        possible_choices.remove(choice)
        i += 1
        
    sponsors = {}
    possible_sponsor_choices = sponsors_names
    for _ in range(sponsors_count):
        sponsor_name = random.choice(possible_sponsor_choices)
        sponsored_animals_count = random.randint(1, round(animals_count/max_sponsored_animals_ratio))
        sponsored_animals = []
        possible_sponsor_choices.remove(sponsor_name)

        possible_animal_choices = list(animals.keys())
        for _ in range(sponsored_animals_count):
            choice = random.choice(possible_animal_choices)
            sponsored_animals.append(str(choice))
            possible_animal_choices.remove(choice)

        sponsor_row = [str(sponsor_name), str(sponsored_animals_count)]
        sponsor_row.extend(sponsored_animals)
        sponsors[sponsor_name] = (" ".join(sponsor_row))

    animals = [f"{key} {value}" for key, value in animals.items()]
    sponsors = [value for value in sponsors.values()]
    write_input(animals, sponsors)

def write_input(animals, sponsors):
    with open("./round_1/sponzori/input.txt", "w", encoding="utf-8") as f:
        lines = [" ".join([str(len(animals)), str(len(sponsors))])]
        lines.extend(animals)
        lines.extend(sponsors)
        f.write("\n".join(lines))

def read_txt(filename):
    with open(f"./round_1/sponzori/{filename}", "r", encoding="utf-8") as input_file:
        content = input_file.read()
        animals = content.split("\n")
        animals = [line for line in animals if line != ""]
    return animals

if __name__ == "__main__":
    generate_input([6, 9], 2, 2)