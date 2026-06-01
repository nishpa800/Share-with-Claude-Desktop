#!/usr/bin/env python3
"""Phase-1 parity recon scanner. Run: python3 scan.py [dir] 2>&1 | cat
Counts dependency-relevant tokens in every .txt Pine file in a directory.
The Desktop folder is TCC-sandboxed (ls/Read fail) but python open() works."""
import os, re, glob, sys

d = sys.argv[1] if len(sys.argv) > 1 else "/Users/anishpatel/Desktop/Indicator studies/"
if not d.endswith("/"):
    d += "/"
targets = sorted(glob.glob(d + "*.txt"))

pats = {
    'request.': r'request\.', 'syminfo.': r'syminfo\.', 'timeframe.': r'timeframe\.',
    'TV.': r'\bTV\.', 'import': r'^\s*import ', 'ta.': r'\bta\.', 'math.': r'\bmath\.',
    'barstate.': r'barstate\.', 'vwap': r'vwap',
    'div/earn/split': r'(dividends|earnings|splits)\.', 'security': r'security',
    'draw.new': r'(label|line|box|table)\.new', 'plotshape': r'plotshape',
    'plotchar': r'plotchar', 'bgcolor': r'bgcolor', 'alertcondition': r'alertcondition',
    'alert(': r'alert\(',
}

if not targets:
    print("NO .txt files in", d)

for t in targets:
    txt = open(t, encoding='utf-8', errors='replace').read()
    print("=" * 70)
    print(os.path.basename(t), "  lines:", txt.count("\n") + 1)
    for name, p in pats.items():
        c = len(re.findall(p, txt, re.M))
        if c:
            print(f"   {name:16s} {c}")
    # surface any import lines verbatim — these are the real TV-dependency risk
    for line in txt.splitlines():
        if re.match(r'\s*import ', line):
            print("   IMPORT >>", line.strip())
