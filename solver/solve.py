import numpy as np
import copy
from solver.load_words import load_words


def recursiveCheck(trie, board, path, word, allPaths):
    # computes current place in 4x4 grid
    loc = path[len(path) - 1]
    yCord = int(loc / 4)
    xCord = loc % 4

    # tests cases for below, current, and above rows
    for yShift in [-1, 0, 1]:
        y = yCord + yShift

        # checks to make sure if above / below row exists, if not continue
        if y < 4 and y >= 0:

            # test cases for right, current, and left columns of test row
            for xShift in [-1, 0, 1]:
                x = xCord + xShift

                # checks to make sure if right / left column exists, if not continue
                if x < 4 and x >= 0:

                    # generates value for path "array"
                    pathLoc = 4 * y + x

                    # checks to make sure if its current element has been visited, if so, go different path
                    if pathLoc not in path.values():

                        # checks to make sure if current word snippit are prefixes to a word to save memory
                        if len(trie.keys(word)) > 0:

                            # makes copys to go around pythons pass by reference
                            newWord = copy.copy(word)
                            newWord += board[y][x]
                            newPath = copy.copy(path)
                            newPath[len(path)] = pathLoc

                            # if word exists and is > 2 letters, add
                            if len(newWord) > 2 and newWord in trie:
                                allPaths[newWord] = newPath

                            # recurse
                            allPaths = {**allPaths, **recursiveCheck(
                                trie, board, newPath, newWord, allPaths)}

                        # if not a prefix, end
                        else:
                            return allPaths

    return allPaths


def solve(board):
    trie = load_words()
    board2D = np.reshape(board, (4, 4))

    allPaths = {}

    for i in range(16):
        path = {0: i}
        word = ""
        word += board[i]
        allPaths = recursiveCheck(trie, board2D, path, word, allPaths)

    return allPaths


"""
testing code
board = ["A", "O", "L", "F", "R", "I", "I",
         "T", "S", "R", "E", "S", "E", "M", "H", "N"]

print(solve(board).keys())
"""
