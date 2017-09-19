
import sys
from sys import argv

class Person:
    def __init__(self, name):
        self.name = name
        self.preferences = []
        self.next_proposal = 0
        self.engaged_to = None

    def rank_of(self, person):
        return self.preferences.index(person.name)

    def engage(m, w):
        w.engaged_to = m
        m.engaged_to = w


def read_people(input_file):
    if not input_file:
        exit(1)

    K = []
    L = []

    with open(input_file) as f:
        # read the number of matches from first line
        num_matches = int(f.readline())

        # read the knight, followed by his preferences
        for i, line in enumerate(f):
            if i == 0:
                pass

            person_data = line.split()

            name = person_data[0]
            preferences = person_data[1:]

            person = Person(name)
            person.preferences = preferences

            if i < num_matches:
                K.append(person)
            else:
                L.append(person)
        f.close()

    return K, L


def print_matches(matches):
    for match in matches:
        sys.stdout.write(match[0] + " " + match[1])


E = set()  # the final matches will be printed


def marriage(M, W):
    while any(not m.engaged_to and m.next_proposal < len(W) for m in M):
        for m in M:
            if m.next_proposal >= len(W):
                continue
            w = W[m.next_proposal]  # woman on m's list to whom he hasn't proposed
            m.next_proposal += 1
            if not w.engaged_to:
                Person.engage(m, w)
                E.add((m.name, w.name))
            elif w.rank_of(m) < w.rank_of(w.engaged_to):
                E.remove((w.engaged_to.name, w.name))
                E.add((m.name, w.name))
                w.engaged_to.engaged_to = None
                Person.engage(m, w)

    print_matches(E)  # print final matches


def main():
    script, file = argv
    K, L = read_people(file)
    marriage(K, L)


main()  # RUN!
