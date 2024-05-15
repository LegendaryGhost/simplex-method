from fractions import Fraction
from math import inf


def pivot(matrix: list[list[Fraction]], pivot_x: int, pivot_y: int):
    pivot_element = matrix[pivot_x][pivot_y]

    for i in range(len(matrix[pivot_x])):
        matrix[pivot_x][i] = matrix[pivot_x][i] / pivot_element

    for i in range(len(matrix)):
        if i != pivot_x:

            coefficient = matrix[i][pivot_y]
            for j in range(len(matrix[0])):
                matrix[i][j] -= matrix[pivot_x][j] * coefficient


def print_matrix(matrix: list[list[Fraction]]):
    print("[")
    for row in matrix:
        print("\t[{}]".format(", ".join("{:>6}".format(str(element)) for element in row)))
    print("]")


def find_pivot(matrix: list[list[Fraction]], find_max: bool) -> tuple[int, int]:
    """
    Find the pivot element and its coordinates in the matrix.

    Args:
    - matrix: The input matrix
    - find_max: Whether to find the maximum or minimum element

    Returns:
    - pivot_x: The row index of the pivot element
    - pivot_y: The column index of the pivot element
    """
    if find_max:
        pivot_y = matrix[-1].index(max(matrix[-1][:-1]))
    else:
        pivot_y = matrix[-1].index(min(matrix[-1][:-1]))

    pivot_column = [matrix[i][pivot_y] for i in range(len(matrix) - 1)]
    last_column = [matrix[i][-1] for i in range(len(matrix) - 1)]

    if not contains_positive(pivot_column):
        return -1, -1

    pivot_x = -1
    pivot_ratio = inf
    for i in range(len(pivot_column)):
        if pivot_column[i] > 0:
            if last_column[i] / pivot_column[i] < pivot_ratio:
                pivot_x = i
                pivot_ratio = last_column[i] / pivot_column[i]

    return pivot_x, pivot_y


def maximize(matrix: list[list[Fraction]], variables: list[str], base_variables: list[str]) -> None:
    while contains_positive(matrix[-1][:-1]):
        pivot_x, pivot_y = find_pivot(matrix, find_max=True)
        base_variables[pivot_x] = variables[pivot_y]
        pivot(matrix, pivot_x, pivot_y)
        print_simplex_table(matrix, variables, base_variables)


def minimize(matrix: list[list[Fraction]], variables: list[str], base_variables: list[str]) -> None:
    while contains_negative(matrix[-1][:-1]):
        pivot_x, pivot_y = find_pivot(matrix, find_max=False)
        base_variables[pivot_x] = variables[pivot_y]
        pivot(matrix, pivot_x, pivot_y)
        print_simplex_table(matrix, variables, base_variables)


def contains_positive(line: list[Fraction]) -> bool:
    return not all(element <= 0 for element in line)


def contains_negative(line: list[Fraction]) -> bool:
    return not all(element >= 0 for element in line)


def print_simplex_table(matrix: list[list[Fraction]], variables: list[str], base_variables: list[str]) -> None:
    table_header = "       |{} |".format(" | ".join("{:>6}".format(str(element)) for element in variables))
    print("|" + ("-" * (len(table_header) + 8)) + "|")
    print("|" + table_header + (" " * 8) + "|")
    print("|" + ("-" * (len(table_header) + 8)) + "|")
    for i in range(len(matrix) - 1):
        print("|{:>6}".format(base_variables[i]), end="")
        print(" |{}".format(" | ".join("{:>6}".format(str(element)) for element in matrix[i])) + " |")
    print("|" + ("-" * (len(table_header) + 8)) + "|")
    print("|" + ("" * 7), end="")
    print((" " * 7) + "|{}".format(" | ".join("{:>6}".format(str(element)) for element in matrix[-1])) + " |")
    print("|" + ("-" * (len(table_header) + 8)) + "|")
    print("\n")


def two_phase_simplex(matrix: list[list[Fraction]], objective: dict[str, Fraction], variables: list[str],
                      base_variables: list[str], artificial_variables: list[str], find_max: bool = True) -> None:
    print_simplex_table(matrix, variables, base_variables)
    for base in base_variables:
        pivot(matrix, base_variables.index(base), variables.index(base))
    print_simplex_table(matrix, variables, base_variables)

    print("Phase 1: Min {}".format(" + ".join(artificial_variables)))
    minimize(matrix, variables, base_variables)
    if matrix[-1][-1] != 0:
        return None

    for artificial in artificial_variables:
        index = variables.index(artificial)
        del variables[index]
        for row in matrix:
            del row[index]

    new_last_row = [Fraction(0) for _ in range(len(variables) + 1)]
    obj_str = []
    for variable in objective.keys():
        variable_index = variables.index(variable)
        new_last_row[variable_index] = objective[variable]
        obj_str.append(str(objective[variable]) + " * " + str(variable))
    matrix[-1] = new_last_row
    obj_str = " + ".join(obj_str)

    for base in base_variables:
        pivot(matrix, base_variables.index(base), variables.index(base))

    print("Phase 2: ", end="")
    if find_max:
        print("Max " + obj_str)
        print_simplex_table(matrix, variables, base_variables)
        maximize(matrix, variables, base_variables)
    else:
        print("Min" + obj_str)
        print_simplex_table(matrix, variables, base_variables)
        minimize(matrix, variables, base_variables)


# Test subject 1
# matrix1 = [
#     [Fraction(6), Fraction(10), Fraction(-1), Fraction(0), Fraction(0), Fraction(1), Fraction(0), Fraction(60)],
#     [Fraction(8), Fraction(25), Fraction(0), Fraction(-1), Fraction(0), Fraction(0), Fraction(1), Fraction(200)],
#     [Fraction(2), Fraction(8), Fraction(0), Fraction(0), Fraction(1), Fraction(0), Fraction(0), Fraction(80)],
#     [Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(1), Fraction(1), Fraction(0)]
#     # [Fraction(-14), Fraction(-35), Fraction(1), Fraction(1), Fraction(1), Fraction(0), Fraction(0), Fraction(-260)]
# ]
# objective1 = {
#     "x1": Fraction(12),
#     "x2": Fraction(20),
# }
# variables1 = ["x1", "x2", "E1", "E2", "E3", "a1", "a2"]
# base_variables1 = ["a1", "a2", "E3"]
# artificial_variables1 = ["a1", "a2"]


# Test subject 2
# matrix1 = [
#     [Fraction(2), Fraction(-1), Fraction(-1), Fraction(0), Fraction(1), Fraction(15)],
#     [Fraction(1), Fraction(1), Fraction(0), Fraction(0), Fraction(0), Fraction(10)],
#     [Fraction(2), Fraction(-1), Fraction(0), Fraction(1), Fraction(0), Fraction(20)],
#     [Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(1), Fraction(0)]
# ]
# objective1 = {
#     "x1": Fraction(4),
#     "x2": Fraction(3)
# }
# variables1 = ["x1", "x2", "E1", "E2", "a1"]
# base_variables1 = ["a1", "x2", "E2"]
# artificial_variables1 = ["a1"]


# Test subject 3
# matrix1 = [
#     [Fraction(1), Fraction(0), Fraction(1), Fraction(0), Fraction(0), Fraction(3000)],
#     [Fraction(0), Fraction(1), Fraction(0), Fraction(1), Fraction(0), Fraction(4000)],
#     [Fraction(1), Fraction(1), Fraction(0), Fraction(0), Fraction(1), Fraction(5000)],
#     [Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0)]
#     # [Fraction(6, 5), Fraction(17, 10), Fraction(0), Fraction(0), Fraction(0), Fraction(0)]
# ]
# objective1 = {
#     "xp": Fraction(6, 5),
#     "xc": Fraction(17, 10)
# }
# variables1 = ["xp", "xc", "E1", "E2", "E3"]
# base_variables1 = ["E1", "E2", "E3"]
# artificial_variables1 = []


# Test subject 4
matrix1 = [
    [Fraction(2), Fraction(4), Fraction(1), Fraction(0), Fraction(16)],
    [Fraction(3), Fraction(2), Fraction(0), Fraction(1), Fraction(12)],
    [Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0)]
    # [Fraction(6, 5), Fraction(17, 10), Fraction(0), Fraction(0), Fraction(0), Fraction(0)]
]
objective1 = {
    "x1": Fraction(7),
    "x2": Fraction(6)
}
variables1 = ["x1", "x2", "E1", "E2"]
base_variables1 = ["E1", "E2"]
artificial_variables1 = []

two_phase_simplex(matrix1, objective1, variables1, base_variables1, artificial_variables1)
# print_simplex_table(matrix1, variables1, base_variables1)
# maximize(matrix1, variables1, base_variables1)
