CKY Parsing

## Setup

```bash
pip install -r requirements.txt
```

## Running

Each part is a standalone script:

```bash
# Part 1: CKY chart by hand (with backpointers and duplicates)
python part1_hand_chart.py

# Part 2: Basic CKY algorithm (sets, no duplicates)
python part2_cky.py

# Part 3: Weighted CKY / Viterbi (most probable parse tree)
python part3_weighted_cky.py

# Part 4: Sum over all parse trees (sentence probability)
python part4_sum_cky.py
```

## File Descriptions

| File | Description |
|------|-------------|
| `part1_hand_chart.py` | CKY with backpointers on "British left waffles on Falklands". Lists duplicate non-terminals with different derivations. |
| `part2_cky.py` | Standard CKY using sets (no duplicates) on the same sentence. |
| `part3_weighted_cky.py` | Viterbi CKY on a PCFG, parsing "astronomers saw stars with ears". Outputs the most probable parse tree and its probability. |
| `part4_sum_cky.py` | Inside algorithm (sum CKY) on the same PCFG/sentence. Outputs the total sentence probability marginalized over all parse trees. |
