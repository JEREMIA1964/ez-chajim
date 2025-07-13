#!/usr/bin/env python3
"""
SUPER EINFACHES PROGRAMM ZUM KORRIGIEREN VON DAGESH-FEHLERN
===========================================================

BENUTZUNG:
1. Speichern Sie diese Datei als "dagesh_fix.py"
2. Legen Sie sie in den Ordner wo Ihre Dateien sind
3. Öffnen Sie ein Terminal/Kommandozeile
4. Tippen Sie: python dagesh_fix.py
5. FERTIG!
"""

import os

def korrigiere_dagesh_fehler(text):
    """
    Diese Funktion korrigiert alle Dagesh-Fehler
    """
    # ALLE Korrekturen die wir brauchen
    korrekturen = {
        # Dagesh-Verdopplungen
        'Massach': 'Massach',
        'massach': 'massach',
        'MASSACH': 'MASSACH',
        
        'Chessed': 'Chessed', 
        'chessed': 'chessed',
        'CHESSED': 'CHESSED',
        
        'Jessod': 'Jessod',
        'jessod': 'jessod', 
        'JESSOD': 'JESSOD',
        
        'Tiqqun': 'Tiqqun',
        'tiqqun': 'tiqqun',
        'TIQQUN': 'TIQQUN',
        'Tiqqun': 'Tiqqun',  # Falsche Dopplung
        'tiqqun': 'tiqqun',
        
        # WWAQ K→Q
        'Qabbala': 'Qabbala',
        'qabbala': 'qabbala',
        'QABBALA': 'QABBALA',
        'Qabbala': 'Qabbala',
        'qabbala': 'qabbala',
        
        'Qawana': 'Qawana',
        'qawana': 'qawana',
        'QAWANA': 'QAWANA',
        'Qawanot': 'Qawanot',
        'qawanot': 'qawanot',
        
        'Qelim': 'Qelim',
        'qelim': 'qelim',
        'QELIM': 'QELIM',
        
        'Qli': 'Qli',
        'qli': 'qli',
        'QLI': 'QLI',
        
        'Qlipot': 'Qlipot',
        'qlipot': 'qlipot',
        'QLIPOT': 'QLIPOT',
        'Qlipa': 'Qlipa',
        'qlipa': 'qlipa',
        
        # Zer-Elimination
        'wandeln': 'wandeln',
        'gewandelt': 'gewandelt',
        'Wandlung': 'Wandlung',
        'wandelnd': 'wandelnd',
        
        'bersten': 'bersten',
        'berstet': 'berstet',
        'geborsten': 'geborsten',
        'Bersten': 'Bersten'
    }
    
    # Ersetze alle falschen Schreibweisen
    for falsch, richtig in korrekturen.items():
        text = text.replace(falsch, richtig)
    
    return text


def korrigiere_datei(dateiname):
    """
    Korrigiert eine einzelne Datei
    """
    try:
        # Datei lesen
        print(f"📖 Lese Datei: {dateiname}")
        with open(dateiname, 'r', encoding='utf-8') as f:
            inhalt = f.read()
        
        # Korrigieren
        korrigiert = korrigiere_dagesh_fehler(inhalt)
        
        # Wenn etwas geändert wurde
        if inhalt != korrigiert:
            # Backup erstellen
            backup_name = dateiname + '.backup'
            with open(backup_name, 'w', encoding='utf-8') as f:
                f.write(inhalt)
            print(f"💾 Backup erstellt: {backup_name}")
            
            # Korrigierte Version speichern
            with open(dateiname, 'w', encoding='utf-8') as f:
                f.write(korrigiert)
            print(f"✅ Korrigiert: {dateiname}")
            return True
        else:
            print(f"👍 Bereits korrekt: {dateiname}")
            return False
            
    except Exception as e:
        print(f"❌ Fehler bei {dateiname}: {e}")
        return False


def hauptprogramm():
    """
    Das Hauptprogramm
    """
    print("=" * 60)
    print("DAGESH & WWAQ KORREKTUR-PROGRAMM")
    print("=" * 60)
    print()
    
    # Frage welche Dateien korrigiert werden sollen
    print("Was möchten Sie korrigieren?")
    print("1 = Alle .md Dateien (Markdown)")
    print("2 = Alle .py Dateien (Python)")
    print("3 = Alle .txt Dateien")
    print("4 = ALLES (.md, .py, .txt)")
    print("5 = Eine bestimmte Datei")
    
    auswahl = input("\nIhre Wahl (1-5): ").strip()
    
    dateien_zu_korrigieren = []
    
    if auswahl == '1':
        # Alle .md Dateien finden
        for datei in os.listdir('.'):
            if datei.endswith('.md'):
                dateien_zu_korrigieren.append(datei)
                
    elif auswahl == '2':
        # Alle .py Dateien finden
        for datei in os.listdir('.'):
            if datei.endswith('.py'):
                dateien_zu_korrigieren.append(datei)
                
    elif auswahl == '3':
        # Alle .txt Dateien finden
        for datei in os.listdir('.'):
            if datei.endswith('.txt'):
                dateien_zu_korrigieren.append(datei)
                
    elif auswahl == '4':
        # ALLE Dateien
        for datei in os.listdir('.'):
            if datei.endswith(('.md', '.py', '.txt')):
                dateien_zu_korrigieren.append(datei)
                
    elif auswahl == '5':
        # Bestimmte Datei
        dateiname = input("Dateiname eingeben: ").strip()
        if os.path.exists(dateiname):
            dateien_zu_korrigieren.append(dateiname)
        else:
            print(f"❌ Datei '{dateiname}' nicht gefunden!")
            return
    else:
        print("❌ Ungültige Auswahl!")
        return
    
    # Zeige was gefunden wurde
    print(f"\n📁 Gefundene Dateien: {len(dateien_zu_korrigieren)}")
    
    if not dateien_zu_korrigieren:
        print("❌ Keine Dateien gefunden!")
        return
    
    # Frage ob fortfahren
    print("\nDiese Dateien werden korrigiert:")
    for datei in dateien_zu_korrigieren[:10]:  # Erste 10 zeigen
        print(f"  - {datei}")
    if len(dateien_zu_korrigieren) > 10:
        print(f"  ... und {len(dateien_zu_korrigieren) - 10} weitere")
    
    antwort = input("\nFortfahren? (j/n): ").strip().lower()
    
    if antwort != 'j':
        print("Abgebrochen!")
        return
    
    # Korrigiere alle Dateien
    print("\n🔧 Starte Korrektur...\n")
    
    korrigiert_count = 0
    for datei in dateien_zu_korrigieren:
        if korrigiere_datei(datei):
            korrigiert_count += 1
    
    # Zusammenfassung
    print("\n" + "=" * 60)
    print("FERTIG!")
    print(f"✅ {korrigiert_count} Dateien wurden korrigiert")
    print(f"👍 {len(dateien_zu_korrigieren) - korrigiert_count} Dateien waren bereits korrekt")
    print("\n💡 Tipp: Backups wurden mit .backup Endung erstellt")
    print("=" * 60)


# BEISPIEL-TEST
def zeige_beispiele():
    """
    Zeigt Beispiele was korrigiert wird
    """
    print("\n📚 BEISPIELE was korrigiert wird:")
    print("-" * 40)
    
    beispiele = [
        ("Massach", "Massach"),
        ("Die Qabbala", "Die Qabbala"),
        ("Chessed und Jessod", "Chessed und Jessod"),
        ("Nezach und Hod", "Nezach und Hod"),  # Bleibt gleich!
        ("tiqqun olam", "tiqqun olam"),
        ("Die Qelim bersten", "Die Qelim bersten")
    ]
    
    for vorher, nachher in beispiele:
        korrigiert = korrigiere_dagesh_fehler(vorher)
        print(f"'{vorher}' → '{korrigiert}'")
        
    print("-" * 40)


# WENN DAS PROGRAMM DIREKT GESTARTET WIRD
if __name__ == "__main__":
    # Zeige erst Beispiele
    zeige_beispiele()
    
    # Dann Hauptprogramm
    print("\nDrücken Sie ENTER um fortzufahren...")
    input()
    
    hauptprogramm()
    
    print("\nQ!")
    
    # Warte auf ENTER bevor das Fenster schließt
    input("\nDrücken Sie ENTER zum Beenden...")