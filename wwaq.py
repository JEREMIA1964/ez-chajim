#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ez Chajim WWAQ Smart Launcher
============================
Intelligenter Launcher für das Ez Chajim System

Stand: 5. Tammus 5785
Autor: JEREMIA1964

Verwendung:
    ./wwaq.py check              # System-Gesundheitsprüfung
    ./wwaq.py validate <datei>   # WWAQ-Validierung
    ./wwaq.py process <datei>    # Manuskript verarbeiten
    ./wwaq.py init               # Projekt initialisieren
    ./wwaq.py spiral             # Aktuelle Spiralzeit
"""

import sys
import os
from pathlib import Path
import click
import json
import yaml
from datetime import datetime
from typing import Optional, Dict, List

# Füge das Projekt-Verzeichnis zum Python-Pfad hinzu
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Importiere Ez Chajim Komponenten
try:
    from __init__ import (
        get_ez_chajim_instance,
        validate_wwaq,
        transform_wwaq,
        get_spiral_time,
        __version__
    )
    MODULES_LOADED = True
except ImportError as e:
    print(f"⚠️  Warnung: Konnte Ez Chajim Module nicht laden: {e}")
    print("   Stelle sicher, dass __init__.py im gleichen Verzeichnis ist!")
    MODULES_LOADED = False

# ANSI Farben für Terminal-Ausgabe
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header():
    """Zeige Ez Chajim Header"""
    header = f"""
{Colors.CYAN}╔═══════════════════════════════════════════════════════════════╗
║                   {Colors.BOLD}Ez Chajim WWAQ System{Colors.ENDC}{Colors.CYAN}                        ║
║                      Version: {__version__ if MODULES_LOADED else 'N/A'}                          ║
║                  {Colors.YELLOW}עץ חיים - Baum des Lebens{Colors.CYAN}                    ║
╚═══════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
    print(header)

def print_status(message: str, status: str = "info"):
    """Formatierte Status-Ausgabe"""
    icons = {
        "info": f"{Colors.BLUE}ℹ{Colors.ENDC}",
        "success": f"{Colors.GREEN}✓{Colors.ENDC}",
        "warning": f"{Colors.YELLOW}⚠{Colors.ENDC}",
        "error": f"{Colors.RED}✗{Colors.ENDC}",
        "working": f"{Colors.CYAN}⚡{Colors.ENDC}"
    }
    icon = icons.get(status, "•")
    print(f"{icon} {message}")

@click.group()
@click.version_option(version=__version__ if MODULES_LOADED else "N/A")
def cli():
    """Ez Chajim WWAQ Smart Launcher"""
    pass

@cli.command()
def check():
    """Führe System-Gesundheitsprüfung durch"""
    print_header()
    print_status("Führe System-Gesundheitsprüfung durch...", "working")
    
    if not MODULES_LOADED:
        print_status("Module nicht geladen - nur Basis-Prüfung möglich", "warning")
        
        # Basis-Verzeichnisprüfung
        required_files = ['__init__.py', 'lib/hns10_spiral_system.py', 
                         'lib/manuscript_processor.py', 'lib/yaml_ez_chajim_formatter.py']
        
        for file in required_files:
            path = PROJECT_ROOT / file
            if path.exists():
                print_status(f"Datei gefunden: {file}", "success")
            else:
                print_status(f"Datei fehlt: {file}", "error")
        
        return
    
    # Vollständige Gesundheitsprüfung
    try:
        instance = get_ez_chajim_instance()
        health = instance.health_check()
        
        print(f"\n{Colors.BOLD}Systemstatus:{Colors.ENDC}")
        for component, status in health.items():
            if status:
                print_status(f"{component}: OK", "success")
            else:
                print_status(f"{component}: FEHLER", "error")
        
        # Zusätzliche Prüfungen
        print(f"\n{Colors.BOLD}Umgebung:{Colors.ENDC}")
        print_status(f"Python-Version: {sys.version.split()[0]}", "info")
        print_status(f"Arbeitsverzeichnis: {Path.cwd()}", "info")
        print_status(f"Spiralzeit: {get_spiral_time()}", "info")
        
        print(f"\n{Colors.GREEN}System-Prüfung abgeschlossen! Q!{Colors.ENDC}")
        
    except Exception as e:
        print_status(f"Fehler bei Gesundheitsprüfung: {e}", "error")
        sys.exit(1)

@cli.command()
@click.argument('file', type=click.Path(exists=True))
def validate(file):
    """Validiere Datei auf WWAQ-Konformität"""
    print_header()
    print_status(f"Validiere Datei: {file}", "working")
    
    if not MODULES_LOADED:
        print_status("Module nicht geladen - Validierung nicht möglich", "error")
        sys.exit(1)
    
    try:
        # Lese Datei
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Validiere
        is_valid, errors = validate_wwaq(content)
        
        if is_valid:
            print_status("Datei ist WWAQ-konform!", "success")
        else:
            print_status(f"Datei enthält {len(errors)} WWAQ-Verstöße:", "error")
            for error in errors:
                print(f"  {Colors.RED}•{Colors.ENDC} {error}")
        
        # Zeige Statistiken
        print(f"\n{Colors.BOLD}Statistiken:{Colors.ENDC}")
        print_status(f"Zeichen: {len(content)}", "info")
        print_status(f"Zeilen: {content.count(chr(10)) + 1}", "info")
        print_status(f"Wörter: {len(content.split())}", "info")
        
    except Exception as e:
        print_status(f"Fehler bei Validierung: {e}", "error")
        sys.exit(1)

@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--output', '-o', help='Ausgabedatei (Standard: stdout)')
@click.option('--format', '-f', type=click.Choice(['yaml', 'json']), 
              default='yaml', help='Ausgabeformat')
def process(file, output, format):
    """Verarbeite Ez Chajim Manuskript"""
    print_header()
    print_status(f"Verarbeite Manuskript: {file}", "working")
    
    if not MODULES_LOADED:
        print_status("Module nicht geladen - Verarbeitung nicht möglich", "error")
        sys.exit(1)
    
    try:
        instance = get_ez_chajim_instance()
        
        # Verarbeite Manuskript
        result = instance.process_manuscript(Path(file))
        
        # Formatiere Ausgabe
        if format == 'yaml':
            output_content = instance.format_to_yaml(result)
        else:
            output_content = json.dumps(result, indent=2, ensure_ascii=False)
        
        # Schreibe Ausgabe
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(output_content)
            print_status(f"Ausgabe geschrieben nach: {output}", "success")
        else:
            print(f"\n{Colors.BOLD}Verarbeitetes Manuskript:{Colors.ENDC}")
            print(output_content)
        
        print_status("Verarbeitung abgeschlossen! Q!", "success")
        
    except Exception as e:
        print_status(f"Fehler bei Verarbeitung: {e}", "error")
        sys.exit(1)

@cli.command()
def init():
    """Initialisiere neues Ez Chajim Projekt"""
    print_header()
    print_status("Initialisiere neues Ez Chajim Projekt...", "working")
    
    # Erstelle Verzeichnisstruktur
    directories = [
        'lib',
        'src',
        'manuscripts',
        'yaml-schemas',
        'output',
        'logs',
        '.temp'
    ]
    
    for dir_name in directories:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            dir_path.mkdir(parents=True)
            print_status(f"Erstellt: {dir_name}/", "success")
        else:
            print_status(f"Existiert bereits: {dir_name}/", "info")
    
    # Erstelle Beispiel-Konfiguration
    config = {
        'project': 'Ez Chajim WWAQ',
        'version': __version__ if MODULES_LOADED else '5785.5.5',
        'wwaq': {
            'validation': True,
            'transformations': {
                'K': 'Q',
                'zer': ''
            }
        },
        'hns10': {
            'null_tabu': True,
            'min_grad': 1,
            'max_grad': 360
        },
        'calendars': ['hebrew', 'solar', 'islamic']
    }
    
    config_path = Path('ez-chajim-config.yaml')
    if not config_path.exists():
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
        print_status("Konfiguration erstellt: ez-chajim-config.yaml", "success")
    
    # Erstelle README
    readme_content = f"""# Ez Chajim WWAQ Projekt

Stand: {datetime.now().strftime('%d.%m.%Y')}

## Struktur

- `lib/` - Kernbibliotheken (HNS10, Manuskript-Prozessor, YAML-Formatter)
- `src/` - Zusätzlicher Quellcode
- `manuscripts/` - Original Ez Chajim Manuskripte
- `yaml-schemas/` - YAML Schema-Definitionen
- `output/` - Generierte Ausgaben
- `logs/` - System-Logs

## Verwendung

```bash
# System-Check
./wwaq.py check

# Datei validieren
./wwaq.py validate manuscript.txt

# Manuskript verarbeiten
./wwaq.py process manuscript.txt -o output.yaml
```

## WWAQ-Konformität

Dieses Projekt folgt den WWAQ-Richtlinien:
- K→Q Transformation (Qabbala statt Kabbala)
- Zer-Elimination
- DIN 31636 Transliteration

Q!
"""
    
    readme_path = Path('README.md')
    if not readme_path.exists():
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print_status("README.md erstellt", "success")
    
    print(f"\n{Colors.GREEN}Projekt initialisiert! Q!{Colors.ENDC}")
    print_status("Nächste Schritte:", "info")
    print("  1. Kopiere die Bibliotheksdateien nach lib/")
    print("  2. Führe './wwaq.py check' aus")
    print("  3. Beginne mit der Manuskript-Verarbeitung")

@cli.command()
def spiral():
    """Zeige aktuelle Spiralzeit"""
    print_header()
    
    if not MODULES_LOADED:
        # Fallback ohne Module
        now = datetime.now()
        print_status(f"Systemzeit: {now.strftime('%Y.%m.%d.%H')}", "info")
    else:
        try:
            spiral_time = get_spiral_time()
            print_status(f"Spiralzeit: {spiral_time}", "info")
            
            # Zusätzliche Zeitinformationen
            instance = get_ez_chajim_instance()
            if 'hns10' in instance.components:
                hns10 = instance.components['hns10']
                
                # Zeige alle drei Kalender
                print(f"\n{Colors.BOLD}Kalender-Synchronisation:{Colors.ENDC}")
                
                # Diese Methoden müssten in hns10_spiral_system.py implementiert sein
                # Hier als Beispiel
                print_status("Hebräisch: 5. Tammus 5785", "info")
                print_status("Solar: 10. Juli 2025", "info")
                print_status("Islamisch: 13. Muharram 1447", "info")
                
        except Exception as e:
            print_status(f"Fehler beim Abrufen der Spiralzeit: {e}", "error")

@cli.command()
@click.argument('text')
def transform(text):
    """Transformiere Text in WWAQ-konforme Form"""
    if not MODULES_LOADED:
        print_status("Module nicht geladen - Transformation nicht möglich", "error")
        sys.exit(1)
    
    try:
        result = transform_wwaq(text)
        print(f"{Colors.BOLD}Original:{Colors.ENDC} {text}")
        print(f"{Colors.BOLD}WWAQ:{Colors.ENDC} {result}")
        
        if text != result:
            print_status("Text wurde transformiert", "success")
        else:
            print_status("Text war bereits WWAQ-konform", "info")
            
    except Exception as e:
        print_status(f"Fehler bei Transformation: {e}", "error")

# Hauptprogramm
if __name__ == '__main__':
    try:
        cli()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Abgebrochen durch Benutzer{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print_status(f"Unerwarteter Fehler: {e}", "error")
        sys.exit(1)
