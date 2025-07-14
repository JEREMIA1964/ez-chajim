#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WWAK-Validator für Ez Chajim"""

import re
import sys
from pathlib import Path

class WWAKValidator:
    def __init__(self):
        self.verstöße = []
        
    def prüfe_datei(self, dateiname: str):
        """Prüft eine Datei auf WWAK-Konformität"""
        try:
            datei = Path(dateiname)
            if not datei.exists():
                print(f"Datei nicht gefunden: {dateiname}")
                return
                
            inhalt = datei.read_text(encoding='utf-8')
            
            # K→Q Prüfung
            if re.search(r'\b[Kk]elim\b', inhalt):
                self.verstöße.append(f"{dateiname}: 'Kelim' → 'Qelim'")
            if re.search(r'\b[Kk]abbal', inhalt):
                self.verstöße.append(f"{dateiname}: 'Kabbal' → 'Qabbal'")
            if re.search(r'\b[Kk]awana', inhalt):
                self.verstöße.append(f"{dateiname}: 'Kawana' → 'Qawana'")
                
            # Zer-Prüfung (außer Klipa-Kontext)
            zer_matches = re.findall(r'\b(zer[a-zäöüß]+)\b', inhalt, re.IGNORECASE)
            for match in zer_matches:
                umgebung = inhalt[max(0, inhalt.find(match)-50):inhalt.find(match)+50]
                if not any(x in umgebung for x in ['Klipa', 'Ego', 'klipa', 'ego']):
                    self.verstöße.append(f"{dateiname}: Zer-Wort '{match}' ohne Klipa-Kontext")
                    
        except Exception as e:
            print(f"Fehler bei {dateiname}: {e}")
    
    def zeige_bericht(self):
        if not self.verstöße:
            print("✅ Alle geprüften Dateien sind WWAK-konform!")
        else:
            print(f"❌ {len(self.verstöße)} WWAK-Verstöße gefunden:")
            for v in self.verstöße:
                print(f"  • {v}")
        print("\nQ!")

if __name__ == "__main__":
    validator = WWAKValidator()
    if len(sys.argv) > 1:
        for datei in sys.argv[1:]:
            validator.prüfe_datei(datei)
    else:
        print("Verwendung: python3 wwak_validator.py <datei1> <datei2> ...")
    validator.zeige_bericht()
