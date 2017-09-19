
from sys import stdout as out
from sys import stderr as error
from sys import argv

class Person:
    def __init__(self, name):
        self.name = name  # initialized invariant
        self.preferences = []  # initialized invariant
        self.next_proposal = 0  # initialized invariant
        self.engaged_to = None  # initialized invariant

    def rank_of(self, person):
        return self.preferences.index(person.name)

    def disengage(self):
        self.engaged_to = None

    def engage(m, w):
        w.engaged_to = m
        m.engaged_to = w


def read_people(input_file):
    if not input_file:
        exit(1)

    K = []  # initialized invariant
    L = []  # initialized invariant

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


def print_matches(K):
    for k in K:
        out.write(k.name + " " + k.engaged_to.name + "\n")


def marriage(M, W):
    # while there exists a knight not engaged and who hasn't preposed to
    # every lady
    while any(not m.engaged_to and m.next_proposal < len(W) for m in M):
        for m in M:
            if m.engaged_to or m.next_proposal >= len(W):
                continue

            # knight selects his next highest ranked lady to propose to
            w_name = m.preferences[m.next_proposal]  # initialized invariant
            w = next(w_ for w_ in W if w_.name == w_name) # initialized invariant
            m.next_proposal += 1  # maintenance invariant

            # if the given w name does not exist in W, exit
            if not w:
                error.write("A lady with the name " + w_name + " could not be found.")
                exit(1)

            # if the lady is not engaged, k and l become engaged
            # otherwise, if the lady prefers k to her current engagement,
            # k and l become engaged and k' is free
            if not w.engaged_to:
                Person.engage(m, w)
            elif w.rank_of(m) < w.rank_of(w.engaged_to):
                w.engaged_to.disengage()
                Person.engage(m, w)

    print_matches(M)  # print final matches, termination invariant


def main():
    script, file = argv
    K, L = read_people(file)
    marriage(K, L)


main()  # RUN!
