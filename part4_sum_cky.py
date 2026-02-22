"""
Part 4: Sum Over All Parse Trees

Sentence: "astronomers saw stars with ears"
Same PCFG as Part 3. Instead of keeping the max (Viterbi),
we sum probabilities over all derivations to compute the
total probability of the sentence (marginalizing over trees).
"""

from tabulate import tabulate


BINARY_RULES = [
    ("S",  "NP", "VP", 1.0),
    ("PP", "P",  "NP", 1.0),
    ("VP", "V",  "NP", 0.7),
    ("VP", "VP", "PP", 0.3),
    ("NP", "NP", "PP", 0.4),
]

LEXICAL_RULES = {
    "astronomers": [("NP", 0.4)],
    "saw":         [("V", 1.0), ("NP", 0.04)],
    "stars":       [("NP", 0.18)],
    "with":        [("P", 1.0)],
    "ears":        [("NP", 0.18)],
    "telescopes":  [("NP", 0.1)],
}

WORDS = ["astronomers", "saw", "stars", "with", "ears"]


def sum_cky(words, lexical_rules, binary_rules):
    """
    Inside-algorithm variant of CKY.
    Each cell stores {NT: total_probability} summed over all derivations.
    """
    n = len(words)
    table = [[{} for _ in range(n + 1)] for _ in range(n + 1)]

    for j in range(1, n + 1):
        word = words[j - 1]
        for (nt, prob) in lexical_rules.get(word, []):
            table[j - 1][j][nt] = table[j - 1][j].get(nt, 0.0) + prob

        for i in range(j - 2, -1, -1):
            for k in range(i + 1, j):
                for (a, b, c, rule_prob) in binary_rules:
                    if b in table[i][k] and c in table[k][j]:
                        b_prob = table[i][k][b]
                        c_prob = table[k][j][c]
                        contribution = rule_prob * b_prob * c_prob
                        table[i][j][a] = table[i][j].get(a, 0.0) + contribution
    return table


def print_results(table, words):
    n = len(words)

    print("=" * 70)
    print("Part 4: Sum Over All Parse Trees (Inside Algorithm)")
    print(f"Sentence: \"{' '.join(words)}\"")
    print("=" * 70)

    headers = [""] + [f"{w}\n[*,{j+1}]" for j, w in enumerate(words)]
    rows = []
    for i in range(n):
        row = [f"[{i},*]"]
        for j in range(n):
            cell_j = j + 1
            if cell_j <= i:
                row.append("")
            else:
                cell = table[i][cell_j]
                if cell:
                    parts = []
                    for nt in sorted(cell):
                        prob = cell[nt]
                        parts.append(f"{nt}: {prob:.10f}")
                    row.append("\n".join(parts))
                else:
                    row.append("-")
        rows.append(row)

    print(tabulate(rows, headers=headers, tablefmt="grid", stralign="center"))

    if "S" in table[0][n]:
        total_prob = table[0][n]["S"]
        print(f"\nTotal probability of the sentence")
        print(f"  (summed over all parse trees): {total_prob:.10f}")
    else:
        print(f"\nNo valid parse — 'S' not in cell [0,{n}].")


if __name__ == "__main__":
    chart = sum_cky(WORDS, LEXICAL_RULES, BINARY_RULES)
    print_results(chart, WORDS)
