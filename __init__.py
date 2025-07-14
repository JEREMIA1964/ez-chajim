#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ez Chajim WWAK - Haupt-Init-Modul
================================
WWAK-konforme Initialisierung des Ez Chajim Systems

Stand: 5. Tammus 5785
Autor: JEREMIA1964
Lizenz: WWAK-konform (siehe LICENSE)

Dieses Modul initialisiert das Ez Chajim System mit:
- HNS10 Spiralsystem (mit Null-Linien-Tabu)
- WWAK-Validierung (K→Q, Zer-Elimination)
- Drei-Kalender-Integration
- Manuskript-Verarbeitung mit Gematria
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import logging
from typing import Dict, List, Optional, Tuple

# WWAK-konforme Version
__version__ = "5785.5.5"  # Jahr.Monat.Tag im hebräischen Kalender
__author__ = "JEREMIA1964"
__wwak_status__ = "KONFORME_AUSGABE"

# Füge lib-Verzeichnis zum Python-Pfad hinzu
LIB_PATH = Path(__file__).parent / 'lib'
if LIB_PATH.exists():
    sys.path.insert(0, str(LIB_PATH))

# Logging-Konfiguration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S MESZ'
)

logger = logging.getLogger('ez_chajim_wwak')

# WWAK-Konstanten
WWAK_MAPPINGS = {
    'K': 'Q',  # Kabbala → Qabbala
    'k': 'q',  # kawana → qawana
    'zer': '',  # Zer-Elimination
    'ZER': '',  # ZER-Elimination
}

# HNS10 Null-Tabu Konfiguration
HNS10_CONFIG = {
    'null_tabu': True,  # Grad 0 ist verboten
    'min_grad': 1,      # Minimum erlaubter Grad
    'max_grad': 360,    # Maximum Grad
    'spiralzeit_format': '{jahr}.{monat}.{tag}.{stunde}'
}

# Kalender-Konfiguration
CALENDAR_CONFIG = {
    'primary': 'hebrew',     # Primärer Kalender
    'secondary': ['solar', 'islamic'],  # Sekundäre Kalender
    'show_all': True        # Zeige alle Kalender in Ausgaben
}

# Projekt-Verzeichnisse
PROJECT_DIRS = {
    'manuscripts': Path('manuscripts'),
    'yaml_schemas': Path('yaml-schemas'),
    'output': Path('output'),
    'temp': Path('.temp'),
    'logs': Path('logs')
}

class EzChajimWWAK:
    """Haupt-Klasse für Ez Chajim WWAK System"""
    
    def __init__(self, base_path: Optional[Path] = None):
        """
        Initialisiere Ez Chajim WWAK System
        
        Args:
            base_path: Basis-Pfad für das Projekt (Standard: aktuelles Verzeichnis)
        """
        self.base_path = base_path or Path.cwd()
        self.components = {}
        self._initialized = False
        
        logger.info(f"Initialisiere Ez Chajim WWAK in: {self.base_path}")
        
        # Erstelle Projekt-Verzeichnisse
        self._create_project_dirs()
        
        # Lade Komponenten
        self._load_components()
        
        # WWAK-Validierung aktivieren
        self._enable_wwak_validation()
        
        self._initialized = True
        logger.info("Ez Chajim WWAK erfolgreich initialisiert! Q!")
    
    def _create_project_dirs(self):
        """Erstelle notwendige Projekt-Verzeichnisse"""
        for name, path in PROJECT_DIRS.items():
            full_path = self.base_path / path
            if not full_path.exists():
                full_path.mkdir(parents=True, exist_ok=True)
                logger.debug(f"Verzeichnis erstellt: {full_path}")
    
    def _load_components(self):
        """Lade alle System-Komponenten"""
        try:
            # HNS10 Spiralsystem
            from hns10_spiral_system import HNS10SpiralSystem
            self.components['hns10'] = HNS10SpiralSystem(
                null_tabu=HNS10_CONFIG['null_tabu']
            )
            logger.info("✓ HNS10 Spiralsystem geladen")
            
            # Manuskript-Prozessor
            from manuscript_processor import ManuscriptProcessor
            self.components['manuscript'] = ManuscriptProcessor()
            logger.info("✓ Manuskript-Prozessor geladen")
            
            # YAML-Formatter
            from yaml_ez_chajim_formatter import YAMLEzChajimFormatter
            self.components['formatter'] = YAMLEzChajimFormatter()
            logger.info("✓ YAML-Formatter geladen")
            
        except ImportError as e:
            logger.error(f"Fehler beim Laden der Komponenten: {e}")
            logger.warning("Stelle sicher, dass alle Bibliotheksdateien im lib/ Verzeichnis sind!")
            raise
    
    def _enable_wwak_validation(self):
        """Aktiviere WWAK-Validierung für alle Komponenten"""
        logger.info("Aktiviere WWAK-Validierung...")
        
        # Setze WWAK-Modus in allen Komponenten
        for name, component in self.components.items():
            if hasattr(component, 'set_wwak_mode'):
                component.set_wwak_mode(True)
                logger.debug(f"WWAK-Modus aktiviert für: {name}")
    
    def validate_text(self, text: str) -> Tuple[bool, List[str]]:
        """
        Validiere Text auf WWAK-Konformität
        
        Args:
            text: Zu validierender Text
            
        Returns:
            Tuple aus (ist_valide, liste_von_fehlern)
        """
        errors = []
        
        # Prüfe verbotene Schreibweisen
        forbidden_patterns = [
            ('Kabbala', 'Qabbala'),
            ('kabbala', 'qabbala'),
            ('Kawana', 'Qawana'),
            ('kawana', 'qawana'),
            ('zerstör', 'berst'),
            ('zerbrech', 'berst'),
            ('zerfetz', 'reiß'),
        ]
        
        for forbidden, correct in forbidden_patterns:
            if forbidden in text:
                errors.append(f"Verboten: '{forbidden}' → Verwende: '{correct}'")
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    def transform_to_wwak(self, text: str) -> str:
        """
        Transformiere Text in WWAK-konforme Form
        
        Args:
            text: Zu transformierender Text
            
        Returns:
            WWAK-konformer Text
        """
        result = text
        
        # Anwende WWAK-Mappings
        for old, new in WWAK_MAPPINGS.items():
            result = result.replace(old, new)
        
        # Spezielle Transformationen
        replacements = [
            ('Kabbala', 'Qabbala'),
            ('kabbala', 'qabbala'),
            ('Kawana', 'Qawana'),
            ('kawana', 'qawana'),
            ('zerstören', 'auflösen'),
            ('zerbrechen', 'bersten'),
            ('zerfetzen', 'reißen'),
        ]
        
        for old, new in replacements:
            result = result.replace(old, new)
        
        return result
    
    def get_spiral_time(self) -> str:
        """
        Hole aktuelle Zeit im Spiralzeit-Format
        
        Returns:
            Spiralzeit-String
        """
        if 'hns10' in self.components:
            return self.components['hns10'].get_current_spiral_time()
        return datetime.now().strftime('%Y.%m.%d.%H')
    
    def process_manuscript(self, manuscript_path: Path) -> Dict:
        """
        Verarbeite ein Ez Chajim Manuskript
        
        Args:
            manuscript_path: Pfad zum Manuskript
            
        Returns:
            Verarbeitete Manuskript-Daten
        """
        if 'manuscript' not in self.components:
            raise RuntimeError("Manuskript-Prozessor nicht geladen!")
        
        logger.info(f"Verarbeite Manuskript: {manuscript_path}")
        
        # Lese Manuskript
        with open(manuscript_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # WWAK-Transformation
        content = self.transform_to_wwak(content)
        
        # Verarbeite mit Manuskript-Prozessor
        result = self.components['manuscript'].process(content)
        
        # Füge Metadaten hinzu
        result['metadata'] = {
            'spiral_time': self.get_spiral_time(),
            'wwak_validated': True,
            'source_file': str(manuscript_path)
        }
        
        return result
    
    def format_to_yaml(self, data: Dict) -> str:
        """
        Formatiere Daten als WWAK-konformes YAML
        
        Args:
            data: Zu formatierende Daten
            
        Returns:
            YAML-String
        """
        if 'formatter' not in self.components:
            raise RuntimeError("YAML-Formatter nicht geladen!")
        
        return self.components['formatter'].format(data)
    
    @property
    def is_initialized(self) -> bool:
        """Prüfe ob System initialisiert ist"""
        return self._initialized
    
    def health_check(self) -> Dict[str, bool]:
        """
        Führe Gesundheitsprüfung des Systems durch
        
        Returns:
            Dictionary mit Komponentenstatus
        """
        status = {
            'system': self._initialized,
            'directories': all(
                (self.base_path / path).exists() 
                for path in PROJECT_DIRS.values()
            )
        }
        
        # Prüfe Komponenten
        for name in ['hns10', 'manuscript', 'formatter']:
            status[f'component_{name}'] = name in self.components
        
        return status
    
    def __repr__(self) -> str:
        """String-Repräsentation"""
        return (
            f"EzChajimWWAK(version={__version__}, "
            f"base_path={self.base_path}, "
            f"components={list(self.components.keys())})"
        )

# Singleton-Instanz
_instance = None

def get_ez_chajim_instance(base_path: Optional[Path] = None) -> EzChajimWWAK:
    """
    Hole Ez Chajim WWAK Singleton-Instanz
    
    Args:
        base_path: Basis-Pfad für das Projekt
        
    Returns:
        EzChajimWWAK Instanz
    """
    global _instance
    if _instance is None:
        _instance = EzChajimWWAK(base_path)
    return _instance

# Convenience-Funktionen für direkten Import
def validate_wwak(text: str) -> Tuple[bool, List[str]]:
    """Validiere Text auf WWAK-Konformität"""
    instance = get_ez_chajim_instance()
    return instance.validate_text(text)

def transform_wwak(text: str) -> str:
    """Transformiere Text in WWAK-konforme Form"""
    instance = get_ez_chajim_instance()
    return instance.transform_to_wwak(text)

def get_spiral_time() -> str:
    """Hole aktuelle Spiralzeit"""
    instance = get_ez_chajim_instance()
    return instance.get_spiral_time()

# Export-Liste
__all__ = [
    'EzChajimWWAK',
    'get_ez_chajim_instance',
    'validate_wwak',
    'transform_wwak',
    'get_spiral_time',
    '__version__',
    '__author__',
    '__wwak_status__'
]

# Initialisierungs-Nachricht
if __name__ != '__main__':
    logger.info(f"Ez Chajim WWAK Modul geladen - Version {__version__}")
    logger.info("Verwende get_ez_chajim_instance() für Zugriff")
    logger.info("Q!")
