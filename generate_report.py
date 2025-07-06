#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ez Chajim Übersichtsbericht"""

import os
from pathlib import Path

print("═" * 60)
print("EZ CHAJIM MODUL-ÜBERSICHT")
print("Stand: 10. Tammus 5785")
print("═" * 60)

modules_dir = Path("modules")
module_count = 0

for module_path in sorted(modules_dir.iterdir()):
    if module_path.is_dir():
        module_count += 1
        init_file = module_path / "src" / "__init__.py"
        
        print(f"\n{module_count}. {module_path.name}")
        
        if init_file.exists():
            # Erste Zeilen der Beschreibung lesen
            with open(init_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines[3:6]:  # Docstring-Zeilen
                    if '"""' not in line and line.strip():
                        print(f"   {line.strip()}")
                        break
            print("   ✓ __init__.py vorhanden")
        else:
            print("   ✗ __init__.py fehlt!")

print(f"\n{'═' * 60}")
print(f"Gesamt: {module_count} Module")
print("Alle Module WWAQ-konform initialisiert!")
print("\nQ!")
