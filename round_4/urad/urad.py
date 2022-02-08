def main(filepath):
    with open(filepath, "r") as f:
        content = f.read().split("\n")

    line_index = 1
    with open(f"./round_4/urad/output.txt", "w", newline="") as f:
        while line_index < len(content) - 1:
            processes_count = int(content[line_index])
            task = content[line_index:line_index+processes_count+1]

            s = Simulation(processes_count)
            for i, process_line in enumerate(task[1:]):
                process_line = [int(num) for num in process_line.split(" ")]

                [offset, instructions_count] = process_line[:2]
                instructions = process_line[2:]
                for j, instruction in enumerate(instructions):
                    if (offset+j) % 256 != 0:
                        s.memory[(offset+j) % 256] = instruction

                s.initialize_process(i, offset)

            for _ in range(5000):
                s.simulate()
            line_index += processes_count + 1

            pc_sum = sum(process.pc for process in s.processes)
            f.write(" ".join([str(s.memory[42]), str(pc_sum), "\n"]))


class Simulation:
    instructions = [
        # unclassified
        ("nop",), ("pc_",),
        # local memory
        ("push", "arg"), ("pop",), ("swap",), ("dup",), ("pushsize",),
        # global memory
        ("load", "mem"), ("store", "mem"),
        # arithemtic
        ("add",), ("sub",), ("div",), ("pow",),
        # jump
        ("brz", "arg"), ("br3", "arg"), ("br7", "arg"), ("brge", "arg"), ("jmp", "arg"),
        # special
        ("armed_bomb",), ("bomb_", "mem"), ("teleport", "arg"), ("jantar", "mem")
    ]
    def __init__(self, processes_count):
        self.memory = [0] * 256
        self.processes_with_teleport = []
        self.processes = [None] * processes_count
        self.frozen_process = None

    def initialize_process(self, index, offset):
        self.processes[index] = Process(offset)

    def decode_instruction(self, instruction_num):
        bits = "{:032b}".format(instruction_num)
        argument, instruction_index = int(bits[8:24], 2), int(bits[24:], 2)
        return instruction_index, argument

    def simulate(self):
        for i, process in enumerate(self.processes):
            if process.active:
                instruction_index, argument = self.decode_instruction(self.memory[process.pc])
                if instruction_index >= len(self.instructions):
                    process.active = False
                else:
                    self.select_instruction(i, instruction_index, argument)
        self.teleport_processes()

    def select_instruction(self, process_index, instruction_index, argument):
        process = self.processes[process_index]
        instruction_info = self.instructions[instruction_index]
        instruction = getattr(process, instruction_info[0])

        if instruction_info[0] == "teleport":
            self.processes_with_teleport.append(process_index)
        elif len(instruction_info) == 2:
            if instruction_info[1] == "arg":
                instruction(argument)
            else:
                instruction(self.memory)
        else:
            instruction()

    def insert_frozen_process(self, active_ps):
        for i, p in enumerate(active_ps[:-1]):
            if p > self.frozen_process and active_ps[i+1] < self.frozen_process \
                or i + 2 == len(active_ps):
                active_ps.insert(i, self.frozen_process)
                return

    def teleport_processes(self):
        active_ps = [process for process in self.processes_with_teleport
            if self.processes[process].active]
        if self.frozen_process and self.frozen_process not in active_ps:
            self.insert_frozen_process(active_ps)
        self.processes_with_teleport = []

        if len(active_ps) == 1:
            self.frozen_process = active_ps[0]
            return
        elif len(active_ps) == 0:
            return
        
        self.frozen_process = None
        first_process_pc = self.processes[active_ps[0]].pc
        for i, process_i in enumerate(active_ps):
            if i + 1 >= len(active_ps):
                self.processes[process_i].teleport(first_process_pc)
            else:
                self.processes[process_i].teleport(self.processes[active_ps[i+1]].pc)


def instruction(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            current_pc = self.pc
            func(*args, **kwargs)
            self.pc = (self.pc + 1) % 256
            if len(self.local_memory) > self.memory_max:
                raise IndexError
        except (IndexError, ZeroDivisionError, ValueError):
            self.active = False
            self.pc = current_pc
    return wrapper

def global_memory_instruction(func):
    @instruction
    def global_instruction_wrapper(self, memory):
        address = self.local_memory.pop()
        if address == 666:
            self.active = False
        else:
            func(self, memory, address)
    return global_instruction_wrapper

def arithmetic_instruction(func):
    @instruction
    def arithmetic_wrapper(self):
        value1 = self.local_memory.pop()
        value2 = self.local_memory.pop()
        result = func(self, value1, value2) % (2 ** 32)
        self.local_memory.append(result)
    return arithmetic_wrapper

def jump_instruction(func):
    @instruction
    def jump_wrapper(self, value):
        jump_value = func(self)
        popped_value = self.local_memory.pop()
        popped_value2 = None
        if func.__name__ == "brge":
            popped_value2 = self.local_memory.pop()
        if jump_value == popped_value or popped_value2 and popped_value >= popped_value2:
            self.pc = (self.pc + value) % 256
    return jump_wrapper


class Process:
    memory_max = 16
    def __init__(self, offset):
        self.pc = offset
        self.local_memory = []
        self.active = True
        self.bomb = False

    @instruction
    def nop(self):
        return None

    @instruction
    def pc_(self):
        self.local_memory.append(self.pc)

    @instruction
    def push(self, value):
        self.local_memory.append(value)

    @instruction
    def pop(self):
        self.local_memory.pop()

    @instruction
    def swap(self):
        self.local_memory[-1], self.local_memory[-2] = self.local_memory[-2], self.local_memory[-1]

    @instruction
    def dup(self):
        self.local_memory.append(self.local_memory[-1])

    @instruction
    def pushsize(self):
        self.local_memory.append(len(self.local_memory))

    @global_memory_instruction
    def load(self, memory, address):
        value = memory[address%256]
        self.local_memory.append(value)

    @global_memory_instruction
    def store(self, memory, address):
        value = self.local_memory.pop()
        if address % 256 != 0:
            memory[address%256] = value

    @arithmetic_instruction
    def add(self, value1, value2):
        return value1 + value2

    @arithmetic_instruction
    def sub(self, value1, value2):
        return value1 - value2

    @arithmetic_instruction
    def div(self, value1, value2):
        return int(value1 / value2)

    @arithmetic_instruction
    def pow(self, value1, value2):
        return pow(value1, value2, (2 ** 32))

    @jump_instruction
    def brz(self):
        return 0

    @jump_instruction
    def br3(self):
        return 3

    @jump_instruction
    def br7(self):
        return 7

    @jump_instruction
    def brge(self):
        return None

    @instruction
    def jmp(self, value):
        self.pc = value % 256

    def armed_bomb(self):
        self.active = False

    @instruction
    def bomb_(self, memory):
        memory[self.pc] = 18

    @instruction
    def teleport(self, pc2):
        self.pc = pc2

    @instruction
    def jantar(self, memory):
        for bomb_place in (2, 4, 8):
            memory[(self.pc+bomb_place) % 256] = 19
            memory[(self.pc-bomb_place) % 256] = 19


if __name__ == "__main__":
    main("./round_4/urad/input.txt")