from networkx import neighbors


def game_theoretic_centrality(g, i):
    s = 1 / (g.degree(i) + 1)

    for j in neighbors(g, i):
        s = s + 1 / (g.degree(j) + 1)

    return s

