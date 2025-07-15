#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ez Chajim Hebrew Processor - Standalone Version
Für direkte Verwendung mit Python3 in nano
Stand: 12. Tammus 5785, Oostende
"""

import re
import sys


class HebrewProcessor:
    """Deutsche akademische Umschrift für hebräische Texte"""
    
    def __init__(self):
        # Konsonanten-Mapping
        self.konsonanten = {
            'א': '',      # Alef - stumm
            'ב': 'b',     # Bet
            'ג': 'g',     # Gimel
            'ד': 'd',     # Dalet
            'ה': 'h',     # He
            'ו': 'w',     # Waw
            'ז': 's',     # Sajin - NICHT "z"!
            'ח': 'ch',    # Chet
            'ט': 't',     # Tet
            'י': 'j',     # Jod
            'כ': 'k',     # Kaf
            'ך': 'ch',    # Kaf sofit
            'ל': 'l',     # Lamed
            'מ': 'm',     # Mem
            'ם': 'm',     # Mem sofit
            'נ': 'n',     # Nun
            'ן': 'n',     # Nun sofit
            'ס': 's',     # Samech
            'ע': '',      # Ajin
            'פ': 'p',     # Pe
            'ף': 'f',     # Pe sofit
            'צ': 'z',     # Zade - NICHT "tz"!
            'ץ': 'z',     # Zade sofit
            'ק': 'k',     # Qof - NIE "q"!
            'ר': 'r',     # Resch
            'ש': 'sch',   # Schin
            'ת': 't'      # Taw
        }
        
        # WWAK-Transformationen
        self.wwak = {
            'qabbala': 'qabbala',
            'qawana': 'qawana',
            'qelim': 'qelim',
            'keli': 'qeli',
            'qli': 'qli',
            'qlipot': 'qlipot',
            'tiqqun': 'tiqqun'
        }
    
    def umschrift(self, text):
        """Macht deutsche Umschrift"""
        result = []
        
        for i, char in enumerate(text):
            if char in self.konsonanten:
                buchstabe = self.konsonanten[char]
                
                # Samech zwischen Vokalen = SS
                if char == 'ס' and self._zwischen_vokalen(text, i):
                    buchstabe = 'ss'
                
                result.append(buchstabe)
            elif char in ' .,;:!?\n':
                result.append(char)
            elif char.isalpha() and ord(char) < 256:
                result.append(char)
        
        # Text zusammenfügen
        umschrift = ''.join(result)
        
        # WWAK anwenden
        for alt, neu in self.wwak.items():
            umschrift = re.sub(f'\\b{alt}\\b', neu, umschrift, flags=re.I)
        
        # Erster Buchstabe groß
        if umschrift:
            umschrift = umschrift[0].upper() + umschrift[1:]
        
        return umschrift + "\nQ!"
    
    def _zwischen_vokalen(self, text, pos):
        """Prüft ob zwischen Vokalen"""
        if pos == 0 or pos >= len(text) - 1:
            return False
        
        # Vereinfachte Prüfung
        vokal_chars = 'אהוי'
        vor = any(c in vokal_chars for c in text[max(0, pos-2):pos])
        nach = any(c in vokal_chars for c in text[pos+1:min(len(text), pos+3)])
        
        return vor and nach


def main():
    """Hauptfunktion"""
    print("Ez Chajim Hebrew Processor")
    print("Stand: 12. Tammus 5785, Oostende")
    print("-" * 40)
    
    processor = HebrewProcessor()
    
    # Direkt-Modus für hebräischen Text
    print("\nHinweis: Geben Sie hebräischen Text direkt ein")
    print("oder wählen Sie eine Option (1-4)")
    print("\nOptionen:")
    print("1. Mehrzeiligen Text eingeben")
    print("2. Datei verarbeiten")
    print("3. Beispiele zeigen")
    print("4. Beenden")
    
    while True:
        eingabe = input("\nEingabe: ").strip()
        
        # Prüfe ob hebräischer Text (enthält hebräische Zeichen)
        if any('\u0590' <= c <= '\u05FF' for c in eingabe):
            print("\nUmschrift:")
            print("-" * 40)
            print(processor.umschrift(eingabe))
            continue
        
        # Sonst als Menü-Wahl behandeln
        if eingabe == '1':
            print("\nHebräischen Text eingeben (Leerzeile zum Beenden):")
            lines = []
            while True:
                line = input()
                if not line:
                    break
                lines.append(line)
            
            if lines:
                text = '\n'.join(lines)
                print("\nUmschrift:")
                print("-" * 40)
                print(processor.umschrift(text))
        
        elif eingabe == '2':
            datei = input("\nDateiname: ").strip()
            try:
                with open(datei, 'r', encoding='utf-8') as f:
                    text = f.read()
                print("\nUmschrift:")
                print("-" * 40)
                print(processor.umschrift(text))
            except FileNotFoundError:
                print("Datei nicht gefunden!")
            except Exception as e:
                print(f"Fehler: {e}")
        
        elif eingabe == '3':
            print("\nBeispiele:")
            print("-" * 40)
            beispiele = [
                ('שלום', 'Schalom'),
                ('חסד', 'Chessed (mit SS!)'),
                ('זהר', 'Sohar (NICHT Zohar!)'),
                ('צדיק', 'Zaddik (NICHT Tzaddik!)'),
                ('קבלה', 'Qabbala (WWAK!)'),
                ('חסרון', 'Chissaron (Doppel-S!)'),
                ('ציצית', 'Zizit (NICHT Tzitzit!)')
            ]
            
            for hebr, erklaerung in beispiele:
                result = processor.umschrift(hebr).replace('\nQ!', '')
                print(f"{hebr} → {result} ({erklaerung})")
        
        elif eingabe == '4':
            print("\nQ!")
            break
        
        else:
            # Nochmal prüfen ob vielleicht doch Text
            if eingabe:
                print("\nUmschrift:")
                print("-" * 40)
                print(processor.umschrift(eingabe))
            else:
                print("Keine Eingabe!")


if __name__ == '__main__':
    main()
