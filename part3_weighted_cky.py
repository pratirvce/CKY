"""
Part 3: Weighted CKY Algorithm (Viterbi)

Sentence: "astronomers saw stars with ears"
Uses a PCFG in CNF. Finds the most probable parse tree
by keeping the max-probability derivation per non-terminal per cell.
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


def weighted_cky(words, lexical_rules, binary_rules):
    """
    Viterbi CKY: each cell stores {NT: (max_prob, backpointer)}.
    backpointer is either the word (for lexical) or (k, B, C) for binary.
    """
    n = len(words)
    table = [[{} for _ in range(n + 1)] for _ in range(n + 1)]

    for j in range(1, n + 1):
        word = words[j - 1]
        for (nt, prob) in lexical_rules.get(word, []):
            table[j - 1][j][nt] = (prob, word)

        for i in range(j - 2, -1, -1):
            for k in range(i + 1, j):
                for (a, b, c, rule_prob) in binary_rules:
                    if b in table[i][k] and c in table[k][j]:
                        b_prob = table[i][k][b][0]
                        c_prob = table[k][j][c][0]
                        prob = rule_prob * b_prob * c_prob
                        if a not in table[i][j] or prob > table[i][j][a][0]:
                            table[i][j][a] = (prob, (k, b, c))
    return table


def extract_tree(table, words, i, j, nt):
    """Recursively build a bracket-notation parse tree."""
    prob, bp = table[i][j][nt]
    if isinstance(bp, str):
        return f"({nt} {bp})"
    k, b, c = bp
    left = extract_tree(table, words, i, k, b)
    right = extract_tree(table, words, k, j, c)
    return f"({nt} {left} {right})"


def pretty_tree(tree_str, indent=0):
    """Convert bracket notation to a readable indented tree."""
    result = []
    i = 0
    depth = 0
    current = ""

    for ch in tree_str:
        if ch == "(":
            if current.strip():
                result.append(" " * depth + current.strip())
                current = ""
            depth += 1
            current += ch
        elif ch == ")":
            current += ch
            inner = current.strip()
            tokens = inner[1:-1].split(None, 1)
            if len(tokens) == 2 and "(" not in tokens[1]:
                result.append(" " * depth + f"({tokens[0]} {tokens[1]})")
            else:
                if tokens:
                    result.append(" " * depth + f"({tokens[0]}")
                result.append(" " * depth + ")")
            current = ""
            depth -= 1
        else:
            current += ch

    return "\n".join(result)


def print_results(table, words):
    n = len(words)

    print("=" * 70)
    print("Part 3: Weighted CKY (Viterbi) Parse Table")
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
                        prob = cell[nt][0]
                        parts.append(f"{nt}: {prob:.6g}")
                    row.append("\n".join(parts))
                else:
                    row.append("-")
        rows.append(row)

    print(tabulate(rows, headers=headers, tablefmt="grid", stralign="center"))

    if "S" in table[0][n]:
        prob = table[0][n]["S"][0]
        tree = extract_tree(table, words, 0, n, "S")
        print(f"\nMost probable parse tree (probability = {prob:.10f}):\n")
        print(f"  Bracket notation: {tree}")
        print(f"\n  Indented form:")
        for line in pretty_tree(tree).split("\n"):
            print(f"    {line}")
    else:
        print(f"\nNo valid parse found — 'S' not in cell [0,{n}].")


if __name__ == "__main__":
    chart = weighted_cky(WORDS, LEXICAL_RULES, BINARY_RULES)
    print_results(chart, WORDS)
