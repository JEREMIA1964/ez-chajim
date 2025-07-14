#!/bin/bash
# B"H - Q→K Migration Script
# 5785/04/18 (18. Tammus 5785), MESZ 05:07
# Beschluss: JBR.-Wolff!Q!

echo "B\"H - Q→K MIGRATION"
echo "===================="
echo "Datum: 18. Tammus 5785, MESZ 05:07"
echo ""

# Ez Chajim Root
EZ_ROOT="/Users/jorgbruder/ez-chajim"

# Backup erstellen
echo "1. ERSTELLE BACKUP..."
BACKUP_DIR="$EZ_ROOT/backup_vor_k_migration_5785_04_18"
mkdir -p "$BACKUP_DIR"
cp -r "$EZ_ROOT/modules" "$BACKUP_DIR/"
echo "✅ Backup erstellt in: $BACKUP_DIR"
echo ""

# Q→K Transformationen durchführen
echo "2. FÜHRE MIGRATION DURCH..."
echo "---------------------------"

# Alle Python-Dateien
find "$EZ_ROOT/modules" -name "*.py" -not -path "*/venv/*" -exec sed -i '' 's/Qabbala/Kabbala/g' {} \;
find "$EZ_ROOT/modules" -name "*.py" -not -path "*/venv/*" -exec sed -i '' 's/qabbala/kabbala/g' {} \;
find "$EZ_ROOT/modules" -name "*.py" -not -path "*/venv/*" -exec sed -i '' 's/Qawana/Kawana/g' {} \;
find "$EZ_ROOT/modules" -name "*.py" -not -path "*/venv/*" -exec sed -i '' 's/qawana/kawana/g' {} \;
find "$EZ_ROOT/modules" -name "*.py" -not -path "*/venv/*" -exec sed -i '' 's/Qli/Kli/g' {} \;
find "$EZ_ROOT/modules" -name "*.py" -not -path "*/venv/*" -exec sed -i '' 's/qli/kli/g' {} \;
find "$EZ_ROOT/modules" -name "*.py" -not -path "*/venv/*" -exec sed -i '' 's/Qlim/Klim/g' {} \;
find "$EZ_ROOT/modules" -name "*.py" -not -path "*/venv/*" -exec sed -i '' 's/qlim/klim/g' {} \;
find "$EZ_ROOT/modules" -name "*.py" -not -path "*/venv/*" -exec sed -i '' 's/Qlipa/Klipa/g' {} \;
find "$EZ_ROOT/modules" -name "*.py" -not -path "*/venv/*" -exec sed -i '' 's/qlipa/klipa/g' {} \;
find "$EZ_ROOT/modules" -name "*.py" -not -path "*/venv/*" -exec sed -i '' 's/Qlipot/Klipot/g' {} \;
find "$EZ_ROOT/modules" -name "*.py" -not -path "*/venv/*" -exec sed -i '' 's/qlipot/klipot/g' {} \;

echo "✅ Q→K Migration durchgeführt!"
echo ""

# WWAQ→WWAK
echo "3. WWAQ→WWAK MIGRATION..."
echo "-------------------------"

find "$EZ_ROOT" -type f \( -name "*.py" -o -name "*.md" -o -name "*.txt" \) -not -path "*/venv/*" -exec sed -i '' 's/WWAQ/WWAK/g' {} \;
find "$EZ_ROOT" -type f \( -name "*.py" -o -name "*.md" -o -name "*.txt" \) -not -path "*/venv/*" -exec sed -i '' 's/wwaq/wwak/g' {} \;

echo "✅ WWAQ→WWAK Migration durchgeführt!"
echo ""
echo "Ki Ilu Azilut! Q!"
