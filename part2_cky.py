"""
Part 2: CKY Algorithm (Programming)

Sentence: "British left waffles on Falklands"
Uses sets for each cell — no duplicate non-terminals.
Prints the parse table using the tabulate package.
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


def cky_parse(words, lexical_rules, binary_rules):
    """
    Standard CKY algorithm.
    table[i][j] = set of non-terminals that can derive words[i:j].
    """
    n = len(words)
    table = [[set() for _ in range(n + 1)] for _ in range(n + 1)]

    for j in range(1, n + 1):
        word = words[j - 1]
        for nt in lexical_rules.get(word, []):
            table[j - 1][j].add(nt)

        for i in range(j - 2, -1, -1):
            for k in range(i + 1, j):
                for (a, b, c) in binary_rules:
                    if b in table[i][k] and c in table[k][j]:
                        table[i][j].add(a)
    return table


def print_parse_table(table, words):
    n = len(words)

    print("=" * 70)
    print("Part 2: CKY Parse Table (sets, no duplicates)")
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
                entries = table[i][cell_j]
                if entries:
                    row.append(", ".join(sorted(entries)))
                else:
                    row.append("-")
        rows.append(row)

    print(tabulate(rows, headers=headers, tablefmt="grid", stralign="center"))

    if "S" in table[0][n]:
        print(f"\nSentence is VALID — 'S' found in cell [0,{n}].")
    else:
        print(f"\nSentence is INVALID — 'S' not found in cell [0,{n}].")


if __name__ == "__main__":
    chart = cky_parse(WORDS, LEXICAL_RULES, BINARY_RULES)
    print_parse_table(chart, WORDS)
