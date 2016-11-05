import numpy as np

class WordAdjacencyGraph(object):
    def __init__(self, passage):
        words = map(lambda x: x.lower(), filter(lambda x: x not in ",.\"?!", passage).split(" "))
        self.word_order = sorted(set(words))
        self.word_lookup = dict(zip(self.word_order, range(len(self.word_order))))
        self.n_uniques = len(self.word_order)
        self.matrix = np.zeros((self.n_uniques, self.n_uniques))

        for i in range(len(words)-1):
            current = words[i]
            next = words[i+1]
            self.matrix[self.word_lookup[current], self.word_lookup[next]] += 1

        for i in range(self.n_uniques):
            self.matrix[i, :] = self.matrix[i, :] / np.sum(self.matrix[i, :])

    def p(self, next, current):
        return self.matrix[self.word_lookup[current], self.word_lookup[next]]

    def simplified_transition(self, current):
        c_i = self.word_lookup[current]
        row = self.matrix[c_i, :]
        nonzero = [i for i in range(self.n_uniques) if row[i] != 0]
        words = [self.word_order[i] for i in nonzero]
        return dict(zip(words, row[nonzero]))



if __name__ == "__main__":
    f = open("test_passage.txt", 'r')
    passage = f.read()

    wa = WordAdjacencyGraph(passage)
    print wa.matrix
    print wa.simplified_transition("this")
