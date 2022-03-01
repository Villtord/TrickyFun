from typing import List
from copy import copy, deepcopy


def shift_generator(board, shift_x, shift_y):
    """Get offset value from board defined by shift_x and shift_y"""
    while True:
        for i in range(len(board)):
            for j in range(len(board[i])):
                if 0 <= i + shift_x < len(board) and 0 <= j + shift_y < len(board[i]):
                    yield board[i + shift_x][j + shift_y]
                else:
                    yield None

def generators_list(board):
    """Returs list of 8 generators to get 2D surrounding values"""
    gen_list = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            gen_list.append(shift_generator(board, x, y))
    return gen_list

def solution(board):
    # check the board
    final_board_ = deepcopy(board)
    gen_list = generators_list(board)
    for i,row in enumerate(board):
        for j,column in enumerate(row):
            result = {0: 0, 1: 0}
            for g in gen_list:
                value = next(g)
                if value != None:
                    result[value] += 1
            result[column] -= 1
            # print(result)
            if column == 0:
                if result[1] == 3:
                    final_board_[i][j] = 1
            else:
                if 2 > result[1] or result[1] > 3:
                    final_board_[i][j] = 0
    return final_board_


assert (solution([[1, 0], [1, 0]]) == [[0, 0], [0, 0]])
assert (solution([[1, 1], [1, 0]]) == [[1, 1], [1, 1]])
assert (solution([[1, 1, 1], [1, 1, 1], [1, 1, 1]]) == [[1, 0, 1], [0, 0, 0], [1, 0, 1]])
print('Yey!')
