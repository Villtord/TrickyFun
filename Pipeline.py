# generates random net NxN of integers from 0 to 10 and calculates the most efficient path
# to walk from left edge to right edge (marked with #) with penalty for each visited integer equal to it's value.

import random

import numpy as np


class Cell:
    def __init__(self):
        """
        cost_list is a dict having "cost" and "path" values
        :param N:
        """
        self.cost = None
        self.path = None
        self.visited = False


def get_path(my_cell_matrix, i, j):
    """
    Trace back full path from end to start cell
    :param my_cell_matrix: N by N nested list of Cell objects
    :param i: i of last cell
    :param j: j of last cell
    :return: [[i, j], ]
    """
    i_curr, j_curr = i, j
    i_next = i_curr
    path = [[i_curr, j_curr]]
    while i_next != 0:
        i_next = int(my_cell_matrix[i_curr][j_curr].path.split(';')[0].split(',')[0])
        j_next = int(my_cell_matrix[i_curr][j_curr].path.split(';')[0].split(',')[1])
        path.append([i_next, j_next])
        i_curr, j_curr = i_next, j_next
    return path


def check_queue(my_cell_matrix):
    """
    Find out first element of queue based on known costs
    :param my_cell_matrix: N by N nested list of Cell objects
    :return: {'cost': None, 'x': None, 'y': None}
    """
    top_queue = {'cost': None, 'x': None, 'y': None}
    for _i in range(len(my_cell_matrix)):
        for _k in range(len(my_cell_matrix[_i])):
            if my_cell_matrix[_i][_k].cost:
                if not my_cell_matrix[_i][_k].visited:
                    # print(f'comparing costs for node {_i} {_k}, visited? {my_cell_matrix[_i][_k].visited}')
                    if top_queue['cost'] is None:
                        top_queue['cost'] = my_cell_matrix[_i][_k].cost
                        top_queue['x'], top_queue['y'] = _i, _k
                    else:
                        if top_queue['cost'] > my_cell_matrix[_i][_k].cost:
                            top_queue['cost'] = my_cell_matrix[_i][_k].cost
                            top_queue['x'], top_queue['y'] = _i, _k
    if top_queue['cost'] is None:
        return None
    return top_queue


# main part is a Dijkstra algorithm
def find_path(layout_):
    """
    Dijkstra algorithm
    :param layout_: N_ by N_ nested list
    :return: {'cost': , 'path': ''}
    """
    field = np.array(layout_)
    field = field.transpose()
    result_ = {'cost': None, 'path': ''}
    for j_stop in range(len(layout_)):
        for j_start in range(len(layout_)):
            cell_matrix = [[Cell() for i in range(len(layout_))] for x in range(len(layout_))]
            # starting point
            i, j = 0, j_start
            cell_matrix[i][j].cost = field[i][j]
            while not (i == N - 1 and j == j_stop):
                for k, l in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                    if N - 1 >= i + k >= 0 and N - 1 >= j + l >= 0:
                        if not cell_matrix[i + k][j + l].visited:
                            if cell_matrix[i + k][j + l].cost:
                                if cell_matrix[i + k][j + l].cost > cell_matrix[i][j].cost + field[i + k][j + l]:
                                    cell_matrix[i + k][j + l].cost = cell_matrix[i][j].cost + field[i + k][j + l]
                                    cell_matrix[i + k][j + l].path = f'{i},{j};{i + k},{j + l}'
                            else:
                                cell_matrix[i + k][j + l].cost = cell_matrix[i][j].cost + field[i + k][j + l]
                                cell_matrix[i + k][j + l].path = f'{i},{j};{i + k},{j + l}'
                cell_matrix[i][j].visited = True
                top = check_queue(cell_matrix)
                if top is not None:
                    i, j = int(top['x']), int(top['y'])
                else:
                    break
            my_path = get_path(cell_matrix, i, j)
            if result_['cost'] is None or cell_matrix[i][j].cost < result_['cost']:
                result_['cost'] = cell_matrix[i][j].cost
                result_['path'] = my_path
    return result_


N = 5
layout = [[None for i in range(N)] for x in range(N)]
for i in range(N):
    for j in range(N):
        layout[i][j] = random.randint(0, 10)

# get the result
result = find_path(layout)

# mark path with stars
for i in result['path']:
    layout[i[1]][i[0]] = '#' + str(layout[i[1]][i[0]])

# make some pretty printing of path
for i in range(len(layout)):
    for j in range(len(layout[i])):
        if str(layout[i][j])[0] != '#':
            if len(str(layout[i][j])) == 1:
                layout[i][j] = ' ' + str(layout[i][j])
            else:
                layout[i][j] = str(layout[i][j])
    print(layout[i])
# print final cost
print(f'Optimal cost: {result["cost"]}')
