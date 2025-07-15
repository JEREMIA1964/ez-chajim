O
#!/usr/bin/env python3
"""B"H - Validiere alle Module
5785/04/18 (18. Tammus 5785)
"""

import sys
import os
from pathlib import Path

# Füge modules zum Path hinzu
sys.path.insert(0, str(Path(__file__).parent / 'modules'))

try:
    from core.de_schreibweise_basis import validator
    
    print("B\"H - Validiere alle Module")
    print("="*60)
    
    modules_dir = Path(__file__).parent / 'modules'
    
    for py_file in modules_dir.rglob('*.py'):
        if 'venv' not in str(py_file) and '__pycache__' not in str(py_file):
            print(f"\nValidiere: {py_file.name}")
            validator.validate_module(str(py_file))
    
    print("\nKi Ilu Azilut! Q!")
    
except ImportError as e:
    print(f"Import-Fehler: {e}")
    print("Stelle sicher, dass de_schreibweise_basis.py existiert!")
