"""Replay exact priority laws for both full-support parity witnesses."""

from collections import defaultdict
from fractions import Fraction as F
from itertools import product


ADJACENCY = {
    3: {"S": ("S", "R", "D"), "R": ("R", "D"), "D": ("D",)},
    4: {"S": ("S", "D1", "D2"), "R": ("R", "D1"), "D1": ("D1",), "D2": ("D2",)},
}
WEIGHTED_S = {3: (F(2, 3), F(1, 6), F(1, 6)), 4: (F(1, 2), F(1, 4), F(1, 4))}
PRIORITY = {"S": 2, "R": 1}


def step(state, letter, states, uniform):
    if letter == "#":
        return [(target, PRIORITY.get(state, 0), F(1, 2)) for target in ("S", "R")]
    row = ADJACENCY[states][state]
    weights = (
        WEIGHTED_S[states] if state == "S" and not uniform else (F(1, len(row)),) * len(row)
    )
    return [(target, 0, weight) for target, weight in zip(row, weights)]


def block_law(length, states, uniform):
    if uniform:
        two = F(1, 2) * F(1, 3) ** length
        one = F(1, 2) ** (length + 1)
        if states == 3:
            one = F(3, 2) * F(1, 2) ** length - F(1, 3) ** length
    else:
        survival = F(2, 3) if states == 3 else F(1, 2)
        one = two = F(1, 2) * survival**length
    return (1 - one - two, one, two)


def propagate_single_blocks(states, uniform):
    live = {"S": F(1, 2), "R": F(1, 2)}
    for length in range(151):
        expected = block_law(length, states, uniform)
        closed = defaultdict(F)
        advanced = defaultdict(F)
        for source, mass in live.items():
            for target, priority, weight in step(source, "#", states, uniform):
                closed[priority, target] += mass * weight
            for target, _, weight in step(source, "a", states, uniform):
                advanced[target] += mass * weight
        assert all(closed[priority, target] == expected[priority] / 2
                   for priority, target in product(range(3), ("S", "R")))
        assert sum(expected) == 1
        live = advanced


def enumerate_two_blocks(states, uniform, first, second):
    start = "D" if states == 3 else "D1"
    law = {(start, ()): F(1)}
    word = "#" + "a" * first + "#" + "a" * second + "#"
    for letter in word:
        following = defaultdict(F)
        for (source, labels), mass in law.items():
            for target, priority, weight in step(source, letter, states, uniform):
                appended = labels + (priority,) if letter == "#" else labels
                following[target, appended] += mass * weight
        law = following
    totals = defaultdict(F)
    for (_, labels), mass in law.items():
        totals[labels[1:]] += mass
    return totals


for states, uniform in product(ADJACENCY, (False, True)):
    propagate_single_blocks(states, uniform)
    for i, j in product(range(9), repeat=2):
        empirical = enumerate_two_blocks(states, uniform, i, j)
        first = block_law(i, states, uniform)
        second = block_law(j, states, uniform)
        assert all(empirical[a, b] == first[a] * second[b]
                   for a, b in product(range(3), repeat=2))

for states in ADJACENCY:
    one = two = F(0)
    for stop in range(1, 65):
        law = block_law(stop, states, True)
        one += 2**stop * law[1]
        two += 2**stop * law[2]
        geom = 1 - F(2, 3) ** stop
        expected_one = F(stop, 2) if states == 4 else F(3 * stop, 2) - 2 * geom
        assert one == expected_one and two == geom

print("604 exact block laws and reset factorizations across both witnesses.")
print("324 two-block laws and 2916 priority-pair probabilities checked, including adjacent separators.")
print("128 grouped-word partial sums on the separating word checked.")
