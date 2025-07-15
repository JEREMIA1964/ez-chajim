#!/usr/bin/env python3
import sys

# Einfache Umschrift
m = {
    'א':'', 'ב':'b', 'ג':'g', 'ד':'d', 'ה':'h', 'ו':'w',
    'ז':'s', 'ח':'ch', 'ט':'t', 'י':'j', 'כ':'k', 'ך':'ch',
    'ל':'l', 'מ':'m', 'ם':'m', 'נ':'n', 'ן':'n', 'ס':'s',
    'ע':'', 'פ':'p', 'ף':'f', 'צ':'z', 'ץ':'z', 'ק':'k',
    'ר':'r', 'ש':'sch', 'ת':'t'
}

# Text von Datei oder stdin
if len(sys.argv) > 1:
    with open(sys.argv[1], 'r') as f:
        text = f.read()
else:
    print("Text eingeben (Ctrl+D zum Beenden):")
    text = sys.stdin.read()

# Umschrift
result = ''.join(m.get(c, c) for c in text)
print(result)
print("Q!")
