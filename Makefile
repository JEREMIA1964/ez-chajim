# Ez Chajim WOZU-System Makefile
# WOZU? Um die Entwicklung zu erleichtern!

.PHONY: help install test run clean

help:
	@echo "Ez Chajim WOZU-System"
	@echo "===================="
	@echo "install  - Installiere Abhängigkeiten"
	@echo "test     - Führe Tests aus"
	@echo "run      - Starte WOZU-TOR Test"
	@echo "clean    - Räume auf"
	@echo "Q!"

install:
	pip install -r requirements.txt

test:
	python -m pytest tests/ -v

run:
	python src/core/wozu_tor.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
