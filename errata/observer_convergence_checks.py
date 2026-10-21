#!/usr/bin/env python3
"""Reproduce proposed corrections to Observer Convergence s8 Fix.pdf.

Source revision: 8b33d720168967513920812cd565be4c61a5117b.
All transition matrices use COLUMN probability vectors: p_next = K p.
The checks use exact fractions and Python's standard library.
Optional --plot PATH needs matplotlib and writes a replacement for Figure 4.
Prepared with AI assistance; the calculations have been executed and checked.
"""
import argparse
from fractions import Fraction as F
from pathlib import Path


def matrix(rows):
    return tuple(tuple(F(x) for x in row) for row in rows)


def columns(m):
    return tuple(zip(*m))


def mv(m, v):
    return tuple(sum(a * b for a, b in zip(row, v)) for row in m)


def mm(a, b):
    return tuple(tuple(sum(x * y for x, y in zip(row, col))
                       for col in columns(b)) for row in a)


def power(m, n):
    result = matrix([[int(i == j) for j in range(len(m))]
                     for i in range(len(m))])
    for _ in range(n):
        result = mm(m, result)
    return result


def tv(a, b):
    return sum(abs(x - y) for x, y in zip(a, b)) / 2


def delta(m):
    return max(tv(a, b) for a in columns(m) for b in columns(m))


def check_stochastic(m):
    assert all(x >= 0 for row in m for x in row)
    assert all(sum(col) == 1 for col in columns(m))


def stationary(m):
    """Solve (K-I)p=0 with the last equation replaced by sum(p)=1."""
    n = len(m)
    augmented = [[m[i][j] - int(i == j) for j in range(n)] + [F(0)]
                 for i in range(n)]
    augmented[-1] = [F(1)] * (n + 1)
    for j in range(n):
        pivot = next(i for i in range(j, n) if augmented[i][j])
        augmented[j], augmented[pivot] = augmented[pivot], augmented[j]
        divisor = augmented[j][j]
        augmented[j] = [x / divisor for x in augmented[j]]
        for i in range(n):
            if i != j:
                scale = augmented[i][j]
                augmented[i] = [x - scale * y
                                for x, y in zip(augmented[i], augmented[j])]
    return tuple(row[-1] for row in augmented)


K = matrix([
    ['.80', '.85', '.05', '.05', '.05'],
    ['.05', '.05', '.80', '.05', '.05'],
    ['.05', '.05', '.05', '.05', '.05'],
    ['.05', '.00', '.05', '.05', '.05'],
    ['.05', '.05', '.05', '.80', '.80'],
])


def walkthrough():
    check_stochastic(K)
    p = stationary(K)
    expected = tuple(map(F, ['.48', '.0875', '.05', '.045625', '.336875']))
    reported = tuple(map(F, ['.38', '.12', '.05', '.05', '.40']))
    assert p == expected and mv(K, p) == p and sum(p) == 1
    assert delta(K) == F(4, 5) and delta(mm(K, K)) == F(3, 5)
    residual = tuple(a - b for a, b in zip(mv(K, reported), reported))
    assert residual == tuple(map(F, ['.051', '-.0325', '0', '-.006', '-.0125']))
    assert tv(p, reported) == F(1, 10)
    worst20 = max(tv(col, p) for col in columns(power(K, 20)))
    assert worst20 < F(3, 1000)
    print('Stationary distribution:', tuple(map(float, p)))
    print('Reported-vector residual:', tuple(map(float, residual)))
    print('TV(correct, reported):', float(tv(p, reported)))
    print('delta(K), delta(K^2):', delta(K), delta(mm(K, K)))
    print('Coefficient-only two-step bound at n=20:', float(F(3, 5)**10))
    print('Actual worst-case TV at n=20:', float(worst20))
    print('Mass outside deterministic fixed states A,E:', float(sum(p[1:4])))
    return p


def changing_kernel_examples():
    # The displayed individual-power condition does not control mixed products.
    a = matrix([[0, 1, 0], [0, 0, '1/2'], [1, 0, '1/2']])
    b = matrix([[0, 0, '1/2'], [1, 0, 0], [0, 1, '1/2']])
    for m in (a, b):
        check_stochastic(m)
        assert min(x for row in power(m, 5) for x in row) == F(1, 8)
    ba = mm(b, a)
    u = tuple(map(F, [0, 1, 0]))
    v = tuple(map(F, ['1/3', 0, '2/3']))
    assert mv(ba, u) == u and mv(ba, v) == v and tv(u, v) == 1
    print('Individual fifth-power minima: 1/8, 1/8')
    print('Alternating product BA has disjoint invariant distributions:', u, v)
    # These matrices do NOT share a common primitive support subgraph.
    # Stronger common-support/edge-weight assumptions can exclude this example.

    # Even uniformly positive one-step mixing does not imply a stationary limit.
    p = tuple(map(F, ['3/4', '1/4']))
    q = tuple(map(F, ['1/4', '3/4']))
    first = matrix([[p[0], p[0]], [p[1], p[1]]])
    second = matrix([[q[0], q[0]], [q[1], q[1]]])
    for m in (first, second):
        check_stochastic(m)
        assert delta(m) == 0
    assert mv(first, q) == p and mv(second, p) == q and p != q
    print('Perfectly mixing alternating kernels cycle between:', p, q)


def plot(path, p):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    matplotlib.rcParams['svg.hashsalt'] = 'observer-convergence-corrected'
    matplotlib.rcParams['svg.fonttype'] = 'none'
    fig, ax = plt.subplots(figsize=(7.5, 4.5), layout='constrained')
    steps = list(range(21))
    for i, label in [(0, 'Start at A'), (2, 'Start at C'), (4, 'Start at E')]:
        current = tuple(F(int(j == i)) for j in range(5))
        distances = []
        for _ in steps:
            distances.append(float(tv(current, p)))
            current = mv(K, current)
        ax.plot(steps, distances, marker='.', label=label)
    ax.plot(steps, [float(F(3, 5)**(n//2)) for n in steps],
            linestyle='--', color='gray', label='Two-step coefficient bound')
    ax.set(xlabel='Steps n', ylabel='Total-variation distance to correct stationary p',
           title='System beta: the printed transition matrix', xlim=(0, 20), ylim=(0, 1.02))
    ax.grid(alpha=.2)
    ax.legend()
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(destination, metadata={'Date': None})
    if destination.suffix.lower() == '.svg':
        destination.write_text('\n'.join(line.rstrip() for line in
                                          destination.read_text().splitlines()) + '\n')
    plt.close(fig)
    print('Wrote:', destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plot', metavar='PATH', help='Write a plot (requires matplotlib).')
    args = parser.parse_args()
    p = walkthrough()
    changing_kernel_examples()
    print('All exact-arithmetic checks passed.')
    if args.plot:
        plot(args.plot, p)


if __name__ == '__main__':
    main()
