"""
Part 1: Filling Out The CKY Chart By Hand

Sentence: "British left waffles on Falklands"
Grammar is a CNF CFG. Each cell tracks non-terminals WITH backpointers,
and duplicates (same NT, different derivations) are listed separately.
"""

from tabulate import tabulate


BINARY_RULES = [
    ("S",  "NP", "VP"),
    ("NP", "JJ", "NP"),
    ("VP", "VP", "NP"),
    ("VP", "VP", "PP"),
    ("PP", "P",  "NP"),
]

LEXICAL_RULES = {
    "British":   ["NP", "JJ"],
    "left":      ["NP", "VP"],
    "waffles":   ["NP", "VP"],
    "on":        ["P"],
    "Falklands": ["NP"],
}

WORDS = ["British", "left", "waffles", "on", "Falklands"]


def cky_with_backpointers(words, lexical_rules, binary_rules):
    """
    CKY that keeps duplicate non-terminals with different backpointers.
    table[i][j] = list of (NT, backpointer_description)
    """
    n = len(words)
    table = [[[] for _ in range(n + 1)] for _ in range(n + 1)]

    for j in range(1, n + 1):
        word = words[j - 1]
        for nt in lexical_rules.get(word, []):
            table[j - 1][j].append((nt, f"{nt} -> {word}"))

        for i in range(j - 2, -1, -1):
            for k in range(i + 1, j):
                for (a, b, c) in binary_rules:
                    for (b_nt, _) in table[i][k]:
                        if b_nt == b:
                            for (c_nt, _) in table[k][j]:
                                if c_nt == c:
                                    bp = f"{a} -> {b}[{i},{k}] + {c}[{k},{j}]"
                                    table[i][j].append((a, bp))
    return table


def print_chart(table, words):
    n = len(words)

    print("=" * 70)
    print("CKY Chart — Cell Contents with Backpointers")
    print(f"Sentence: \"{' '.join(words)}\"")
    print("=" * 70)

    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length
            entries = table[i][j]
            span = " ".join(words[i:j])
            print(f"\nCell [{i},{j}]  \"{span}\":")
            if entries:
                for (nt, bp) in entries:
                    print(f"    {bp}")
            else:
                print("    (empty)")

    print("\n" + "=" * 70)
    print("Summary Table (non-terminals per cell)")
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
                entries = table[i][cell_j]
                if entries:
                    nts = [nt for (nt, _) in entries]
                    row.append(", ".join(nts))
                else:
                    row.append("-")
        rows.append(row)

    print(tabulate(rows, headers=headers, tablefmt="grid", stralign="center"))


if __name__ == "__main__":
    chart = cky_with_backpointers(WORDS, LEXICAL_RULES, BINARY_RULES)
    print_chart(chart, WORDS)
