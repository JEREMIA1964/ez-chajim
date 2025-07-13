# Ez Chajim Transliteration Integration Guide
**Stand: 12. Tammus 5785**

## Phase 1: Basis-Integration (Minimal-Setup)

### 1.1 TransliterationService einrichten

```bash
# Verzeichnisstruktur erstellen
mkdir -p ez-chajim/modules/transliteration
mkdir -p ez-chajim/config

# Service-Datei kopieren
cp transliteration_service.py ez-chajim/modules/transliteration/

# __init__.py erstellen für Import
echo "from .transliteration_service import *" > ez-chajim/modules/transliteration/__init__.py
```

### 1.2 Minimale Konfiguration

```yaml
# ez-chajim/config/transliteration.yaml
transliteration_config:
  version: "5785.12.12"
  
  # Kritische Dagesh-Korrekturen
  pflicht_korrekturen:
    Massach: Massach
    Chessed: Chessed
    Jessod: Jessod
    Tiqqun: Tiqqun
    
  # WWAQ K→Q
  k_zu_q:
    Qabbala: Qabbala
    Qawana: Qawana
    Qelim: Qelim
```

### 1.3 Test der Installation

```python
# test_transliteration.py
from modules.transliteration import korrigiere_text, validiere

# Test-Fälle
test_texte = [
    "Die Qabbala von Massach",
    "Chessed und Jessod",
    "Nezach bleibt Nezach"
]

for text in test_texte:
    korrigiert = korrigiere_text(text)
    valid, fehler = validiere(text)
    
    print(f"Original:   {text}")
    print(f"Korrigiert: {korrigiert}")
    print(f"Valid:      {valid}")
    if fehler:
        print(f"Fehler:     {fehler}")
    print("-" * 40)
```

## Phase 2: Module einzeln aktualisieren

### 2.1 PardesProcessor anpassen

```python
# In src/pardes/core/pardes_system.py

# Am Anfang hinzufügen:
try:
    from modules.transliteration import korrigiere_text
    TRANSLITERATION_AKTIV = True
except ImportError:
    TRANSLITERATION_AKTIV = False
    def korrigiere_text(text):
        return text  # Fallback

# In der process() Methode:
def process(self, text: str, context: Optional[Dict] = None):
    # NEU: Text korrigieren
    if TRANSLITERATION_AKTIV:
        text = korrigiere_text(text)
    
    # Rest der Methode...
```

### 2.2 IntelliChunker anpassen

```python
# In src/intelli_chunk.py

# Wrapper-Funktion für alle Text-Eingänge
def _prepare_text(self, text: str) -> str:
    """Bereitet Text vor: WWAQ + Dagesh-Korrekturen"""
    try:
        from modules.transliteration import korrigiere_text
        return korrigiere_text(text)
    except ImportError:
        # Minimal-Korrekturen wenn Service fehlt
        replacements = {
            'Massach': 'Massach',
            'Chessed': 'Chessed',
            'Qabbala': 'Qabbala'
        }
        for alt, neu in replacements.items():
            text = text.replace(alt, neu)
        return text

# In chunk_text() verwenden:
def chunk_text(self, text: str) -> List[Chunk]:
    text = self._prepare_text(text)  # NEU!
    # Rest der Methode...
```

## Phase 3: Git-Integration

### 3.1 Pre-Commit Hook einrichten

```bash
# .git/hooks/pre-commit
#!/bin/bash

# Prüfe ob TransliterationService verfügbar
if [ -f "modules/transliteration/transliteration_service.py" ]; then
    echo "🔍 Prüfe Schreibweisen..."
    
    # Python-Check
    python3 -c "
from modules.transliteration import validiere
import sys

fehler_gefunden = False

# Prüfe geänderte .md und .py Dateien
import subprocess
result = subprocess.run(['git', 'diff', '--cached', '--name-only'], 
                       capture_output=True, text=True)

for datei in result.stdout.strip().split('\n'):
    if datei.endswith(('.md', '.py')):
        try:
            with open(datei, 'r') as f:
                inhalt = f.read()
            valid, fehler = validiere(inhalt)
            if not valid:
                print(f'❌ {datei}: {fehler[0]}')
                fehler_gefunden = True
        except:
            pass

if fehler_gefunden:
    print('⚠️  Bitte korrigiere die Schreibweisen!')
    sys.exit(1)
"
fi
```

### 3.2 Makefile anpassen

```makefile
# In Makefile hinzufügen

.PHONY: check-transliteration fix-transliteration

check-transliteration:
	@if [ -f "modules/transliteration/transliteration_service.py" ]; then \
		python -m modules.transliteration --check; \
	else \
		echo "⚠️  TransliterationService nicht installiert"; \
	fi

fix-transliteration:
	@if [ -f "modules/transliteration/transliteration_service.py" ]; then \
		find . -name "*.md" -o -name "*.py" | xargs python -m modules.transliteration --fix; \
		echo "✅ Schreibweisen korrigiert"; \
	fi

# In test-Target einbinden
test: check-transliteration
	pytest tests/
```

## Phase 4: Schrittweise Aktivierung

### 4.1 Modul-für-Modul Vorgehen

```yaml
# activation_plan.yaml
aktivierungs_reihenfolge:
  1_woche:
    - PardesProcessor  # Zentral, viel Text
    - IntelliChunker   # Kritisch für Chunks
    
  2_woche:
    - RabashProcessor  # Viele hebräische Begriffe
    - WozuValidator    # Prüft sowieso Text
    
  3_woche:
    - ManuscriptProcessor
    - YamlFormatter
    - Alle anderen Module
```

### 4.2 Test-Suite erweitern

```python
# tests/test_transliteration_integration.py
import pytest
from modules.transliteration import korrigiere_text

class TestTransliterationIntegration:
    
    def test_dagesh_korrekturen(self):
        """Testet kritische Dagesh-Fälle"""
        assert korrigiere_text("Massach") == "Massach"
        assert korrigiere_text("Chessed") == "Chessed"
        assert korrigiere_text("Nezach") == "Nezach"  # Keine Änderung!
    
    def test_wwaq_transformation(self):
        """Testet K→Q Regeln"""
        assert korrigiere_text("Qabbala") == "Qabbala"
        assert korrigiere_text("Die Qawana") == "Die Qawana"
    
    def test_module_integration(self):
        """Testet ob Module korrekt integriert"""
        from src.pardes.core.pardes_system import PardesProcessor
        
        processor = PardesProcessor()
        # Sollte intern korrigieren
        result = processor.process("Chessed von Massach")
        
        # Prüfe ob korrigiert wurde
        assert "Chessed" in str(result)
        assert "Massach" in str(result)
```

## Phase 5: Monitoring & Wartung

### 5.1 Einfaches Monitoring-Script

```python
# scripts/check_all_files.py
#!/usr/bin/env python3
"""Prüft alle Dateien auf Transliterationsfehler"""

import os
from pathlib import Path
from modules.transliteration import validiere

def check_directory(path="."):
    fehler_gesamt = 0
    dateien_mit_fehlern = []
    
    for datei in Path(path).rglob("*.md"):
        with open(datei, 'r', encoding='utf-8') as f:
            inhalt = f.read()
        
        valid, fehler = validiere(inhalt)
        if not valid:
            fehler_gesamt += len(fehler)
            dateien_mit_fehlern.append((datei, fehler))
    
    # Report
    print(f"=== TRANSLITERATIONS-CHECK ===")
    print(f"Gefundene Fehler: {fehler_gesamt}")
    
    if dateien_mit_fehlern:
        print("\nDateien mit Fehlern:")
        for datei, fehler in dateien_mit_fehlern[:5]:  # Erste 5
            print(f"\n{datei}:")
            for f in fehler:
                print(f"  - {f}")
    
    return fehler_gesamt == 0

if __name__ == "__main__":
    import sys
    success = check_directory()
    sys.exit(0 if success else 1)
```

### 5.2 Automatisches Fix-Script

```bash
#!/bin/bash
# scripts/fix_all_transliterations.sh

echo "🔧 Korrigiere alle Transliterationen..."

# Backup erstellen
echo "📦 Erstelle Backup..."
git stash push -m "Backup vor Transliterations-Fix"

# Korrekturen anwenden
find . -type f \( -name "*.md" -o -name "*.py" \) -print0 | \
while IFS= read -r -d '' file; do
    echo "  Korrigiere: $file"
    python -c "
from modules.transliteration import korrigiere_text
with open('$file', 'r') as f:
    content = f.read()
korrigiert = korrigiere_text(content)
if content != korrigiert:
    with open('$file', 'w') as f:
        f.write(korrigiert)
    print('    ✓ Korrigiert')
"
done

echo "✅ Fertig! Prüfe mit 'git diff'"
```

## Wichtige Hinweise

### ⚠️ Nezach bleibt Nezach!
```yaml
KEINE_VERDOPPLUNG:
  - Nezach (נֶצַח) - hat KEINEN Dagesh
  - Hod (הוֹד) - hat KEINEN Dagesh
  
MIT_VERDOPPLUNG:
  - Massach (מַסָּךְ) - Dagesh im ס
  - Chessed (חֶסֶּד) - Dagesh im ס  
  - Jessod (יְסוֹד) - Dagesh im ס
  - Tiqqun (תִּקּוּן) - Dagesh im ק
```

### 🔄 Reihenfolge der Integration
1. **Erst testen** mit einzelnen Dateien
2. **Dann ein Modul** komplett umstellen
3. **Schließlich alle Module** nachziehen

### 📊 Erfolgs-Metriken
- Keine "Massach" mehr in Dokumentation
- Keine "Qabbala" in Code-Kommentaren  
- Git-Commits ohne Transliterationsfehler

Q!
