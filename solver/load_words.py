import os
import marisa_trie

file = "/solver/words.txt"
path = os.getcwd() + file


def load_words():
    with open(path) as word_file:
        words = word_file.read().split()

    trie = marisa_trie.Trie(words)

    return trie
