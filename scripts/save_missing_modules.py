#!/usr/bin/env python3
"""B"H - Speichert die fehlenden Ez Chajim Module"""

import os

# Hier die Module aus dem Artefakt einfügen
# Kopiere den Inhalt von MODULES = {...} aus dem Artefakt

def save_modules(base_path="/Users/jorgbruder/ez-chajim"):
    """Speichert alle Module in die richtige Struktur"""
    
    # Module aus dem Artefakt hier einfügen...
    
    for filepath, content in MODULES.items():
        full_path = os.path.join(base_path, filepath)
        
        # Erstelle Verzeichnis wenn es nicht existiert
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Speichere die Datei
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Gespeichert: {filepath}")

if __name__ == "__main__":
    save_modules()
    print("\nKi Ilu Azilut! = Q!")
