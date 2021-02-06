# This script has been created with the sole purpose of testing an algorithm
# which returns all the possible ways a student has of choosing the different
# laboratory groups

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class EsiLab:
    name: str
    incompatible_esi_class: EsiLab = None
    elegible: bool = True

    def __str__(self):
        return self.name


@dataclass
class StackFrame:
    lab: EsiLab
    index: int
    first_time: bool = True


def iterative_all_combinations(labs: List[List[EsiLab]]) -> List[List[EsiLab]]:
    solutions = []
    stack = [StackFrame(lab, 0) for lab in labs[0]]
    temp = []

    while len(stack) != 0:
        current_frame = stack.pop()
        current_lab = current_frame.lab

        if not current_lab.elegible:
            continue

        if current_frame.first_time:
            if current_lab.incompatible_esi_class is not None:
                current_lab.incompatible_esi_class.elegible = False

            current_frame.first_time = False
            stack.append(current_frame)
            temp.append(current_lab)

            next_index = current_frame.index + 1
            if next_index == len(labs):
                solutions.append(temp[:])
            else:
                for next_lab in labs[next_index]:
                    stack.append(StackFrame(next_lab, next_index))

        else:
            if current_lab.incompatible_esi_class is not None:
                current_lab.incompatible_esi_class.elegible = True

            temp.pop()

    return solutions


def recursive_all_combinations(labs: List[List[EsiLab]]) -> List[List[EsiLab]]:
    solutions = []
    get_combinations(0, labs, [], solutions)
    return solutions


def get_combinations(current_index: int, labs: List[List[EsiLab]], stack: List, solutions: List) -> None:
    if current_index == len(labs):
        solutions.append(stack[:])
    else:
        for lab in labs[current_index]:
            if not lab.elegible:
                continue

            if lab.incompatible_esi_class is not None:
                lab.incompatible_esi_class.elegible = False

            stack.append(lab)
            get_combinations(current_index + 1, labs, stack, solutions)
            stack.pop()

            if lab.incompatible_esi_class is not None:
                lab.incompatible_esi_class.elegible = True


def create_esi_labs_from_info(schedule_information: Dict) -> List[List[EsiLab]]:
    labs = []
    temp = {}

    for subject_name in schedule_information["subjects"]:
        lab_in_subject = []
        for i in range(1, 3):
            lab_name = f"{subject_name} {i}"
            temp[lab_name] = EsiLab(lab_name)
            lab_in_subject.append(temp[lab_name])

        labs.append(lab_in_subject)

    for first_lab, second_lab in schedule_information["incompatibilities"]:
        temp[first_lab].incompatible_esi_class = temp[second_lab]
        temp[second_lab].incompatible_esi_class = temp[first_lab]

    return labs


# this corresponds to the schedule of group A
# I consider two labs incompatible when they happen at the same time,
# so you are forced to choose

# there is no problem with this representation in the case of first year students schedule
# for other years this representation has to change
group_A_labs = {
    "subjects": [
        "Redes", "Algebra", "Eco", "SistInformacion", "Programacion"
    ],
    "incompatibilities": [
        ("Eco 1", "SistInformacion 1"),
        ("SistInformacion 2", "Algebra 1"),
        ("Programacion 1", "Eco 2"),
        ("Programacion 2", "Redes 2")
    ]
}

esi_labs = create_esi_labs_from_info(group_A_labs)
all_combinations_recursive = recursive_all_combinations(esi_labs)
all_combinations_iterative = iterative_all_combinations(esi_labs)

print("Recursive result:")
for combination in all_combinations_recursive:
    print(" - ".join(map(str, combination)))

print("\nIterative result:")
for combination in all_combinations_iterative:
    print(" - ".join(map(str, combination)))
