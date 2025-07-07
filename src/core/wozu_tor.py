#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Das WOZU-TOR - Kernmodul
========================

WOZU ist nicht eine Frage – sondern das TOR.

Stand: 11. Tammus 5785, MESZ 18:15
"""

from typing import Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class WozuAusrichtung(Enum):
    """Die heiligen WOZU-Ausrichtungen"""
    EIN_SOF_OFFENBARUNG = "Offenbarung des Lichts EIN SOF"
    NAHAT_RUACH = "Freude für den Schöpfer"
    SCHECHINA_ERHEBUNG = "Erhebung der Schechina"
    SEELEN_ANBINDUNG = "Anbindung aller Seelen"


@dataclass
class WozuAnalyse:
    """Ergebnis einer WOZU-Analyse"""
    text: str
    ist_wozu_zentriert: bool
    ausrichtung: Optional[WozuAusrichtung]
    transformation: Optional[str]
    azilut_score: float = 0.0


class WozuTor:
    """Das TOR zwischen Trennung und Einheit"""
    
    def __init__(self):
        self.durchgänge = 0
        print("WOZU-TOR initialisiert. Q!")
    
    def prüfe_durchgang(self, text: str) -> WozuAnalyse:
        """Prüft ob Text das TOR durchqueren kann"""
        
        # WOZU dieser Code?
        # Um zu erkennen, ob die Absicht rein ist
        
        text_lower = text.lower()
        
        # Einfache erste Prüfung
        ist_wozu = "wozu" in text_lower or "למען" in text
        
        # Bestimme Ausrichtung
        ausrichtung = None
        if "licht" in text_lower or "אור" in text:
            ausrichtung = WozuAusrichtung.EIN_SOF_OFFENBARUNG
        elif "freude" in text_lower or "נחת" in text:
            ausrichtung = WozuAusrichtung.NAHAT_RUACH
            
        # Berechne Score
        score = 1.0 if ist_wozu else 0.3
        if ausrichtung:
            score = min(score + 0.3, 1.0)
        
        # Transformation wenn nötig
        transformation = None
        if not ist_wozu:
            transformation = f"WOZU sage ich: '{text}'? - Zur Offenbarung des Lichts!"
        
        return WozuAnalyse(
            text=text,
            ist_wozu_zentriert=ist_wozu,
            ausrichtung=ausrichtung,
            transformation=transformation,
            azilut_score=score
        )
    
    def durchquere_tor(self, text: str) -> str:
        """Führt Text durch das TOR"""
        
        analyse = self.prüfe_durchgang(text)
        
        if analyse.ist_wozu_zentriert:
            self.durchgänge += 1
            return f"✅ TOR DURCHQUERT! {text}"
        else:
            return f"🔄 TRANSFORMATION NÖTIG: {analyse.transformation}"


# Teste sofort!
if __name__ == "__main__":
    print("=== WOZU-TOR TEST ===")
    print(f"Stand: 11. Tammus 5785")
    print()
    
    tor = WozuTor()
    
    # Test-Sätze
    tests = [
        "Ich will Erfolg",
        "WOZU arbeite ich? Um Licht zu offenbaren!",
        "Was ist das?",
        "WOZU sind wir hier? Zur Freude des Schöpfers!"
    ]
    
    for test in tests:
        print(f"Text: {test}")
        print(f"→ {tor.durchquere_tor(test)}")
        print()
    
    print(f"Gesamt-Durchgänge: {tor.durchgänge}")
    print("\nQ!")
