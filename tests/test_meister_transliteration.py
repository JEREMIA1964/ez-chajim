#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test-Script für MEISTER FRAGE Tool mit Transliteration"""

import sys
import os
sys.path.insert(0, 'src')

from meister_frage_tool import MeisterFrageTool
from meister_transliteration import MeisterTransliteration

def test_basic():
    print("=== BASIC TEST ===\n")
    
    # Test Transliteration
    trans = MeisterTransliteration()
    text = "Die Kabbala lehrt über Chesed und Jesod."
    korrigiert = trans.korrigiere_deutsche_begriffe(text)
    
    print(f"Original:   {text}")
    print(f"Korrigiert: {korrigiert}")
    print()
    
    # Test MEISTER Tool
    tool = MeisterFrageTool()
    ergebnis = tool.verarbeite_text(text)
    
    if ergebnis['beste_frage']:
        print(f"Beste Frage: {ergebnis['beste_frage'].frage}")
    
    print("\nQ!")

if __name__ == "__main__":
    test_basic()
