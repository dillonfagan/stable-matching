
from sys import stdout as out
from sys import stderr as error
from sys import argv

class Person:
    def __init__(self, name):
        self.name = name
        self.preferences = []
        self.next_proposal = 0
        self.engaged_to = None

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


def print_matches(M):
    for m in M:
        if not m.engaged_to:
            error.write(m.name + " is not engaged. \n")
        else:
            out.write(m.name + " " + m.engaged_to.name + "\n")


def marriage(M, W):
    while any(not m.engaged_to and m.next_proposal < len(W) for m in M):
        for m in M:
            if m.engaged_to or m.next_proposal >= len(W):
                continue

            # knight selects his next highest ranked lady to propose to
            w_name = m.preferences[m.next_proposal]
            w = next(w_ for w_ in W if w_.name == w_name)
            m.next_proposal += 1

            if not w:
                error.write("A lady with the name " + w_name + " could not be found.")
                exit(1)

            if not w.engaged_to:
                Person.engage(m, w)
            elif w.rank_of(m) < w.rank_of(w.engaged_to):
                w.engaged_to.disengage()
                Person.engage(m, w)

    print_matches(M)  # print final matches


def main():
    script, file = argv
    K, L = read_people(file)
    marriage(K, L)


main()  # RUN!
