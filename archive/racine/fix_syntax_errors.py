#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de correction des erreurs de syntaxe causées par la suppression de paramètres
"""

import re
import os
import sys

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

FILES_TO_FIX = [
    'src/gui_modern_v13.py',
    'src/advanced_pages.py',
    'src/splash_screen.py',
    'src/monitoring_dashboard.py',
    'src/network_tools_gui.py',
    'src/script_automation_gui.py',
]

def fix_file(filepath):
    """Corrige les erreurs de syntaxe dans un fichier"""
    
    if not os.path.exists(filepath):
        print(f"[ERROR] Fichier introuvable: {filepath}")
        return 0
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    fixes_count = 0
    
    # Pattern 1: Corriger ", NOMBRE))" -> ", PARAM=NOMBRE)"
    # Ex: .pack(fill=tk.X, 15)) -> .pack(fill=tk.X, pady=15)
    # Ex: .pack(side=tk.LEFT, 10)) -> .pack(side=tk.LEFT, padx=10)
    
    # Cas 1: fill=tk.X, NOMBRE)) -> fill=tk.X, pady=NOMBRE)
    pattern1 = r'(fill=tk\.[XY]),\s*(\d+)\)\)'
    matches = list(re.finditer(pattern1, content))
    for match in reversed(matches):
        old_text = match.group(0)
        fill_val = match.group(1)
        num = match.group(2)
        new_text = f"{fill_val}, pady={num})"
        content = content[:match.start()] + new_text + content[match.end():]
        fixes_count += 1
        print(f"  Fix: {old_text} -> {new_text}")
    
    # Cas 2: side=tk.LEFT/RIGHT, NOMBRE)) -> side=tk.XXX, padx=NOMBRE)
    pattern2 = r'(side=tk\.(LEFT|RIGHT)),\s*(\d+)\)\)'
    matches = list(re.finditer(pattern2, content))
    for match in reversed(matches):
        old_text = match.group(0)
        side_val = match.group(1)
        num = match.group(3)
        new_text = f"{side_val}, padx={num})"
        content = content[:match.start()] + new_text + content[match.end():]
        fixes_count += 1
        print(f"  Fix: {old_text} -> {new_text}")
    
    # Cas 3: side=tk.TOP/BOTTOM, NOMBRE)) -> side=tk.XXX, pady=NOMBRE)
    pattern3 = r'(side=tk\.(TOP|BOTTOM)),\s*(\d+)\)\)'
    matches = list(re.finditer(pattern3, content))
    for match in reversed(matches):
        old_text = match.group(0)
        side_val = match.group(1)
        num = match.group(3)
        new_text = f"{side_val}, pady={num})"
        content = content[:match.start()] + new_text + content[match.end():]
        fixes_count += 1
        print(f"  Fix: {old_text} -> {new_text}")
    
    # Cas 4: .pack/grid/place(..., NOMBRE)) sans autre paramètre visible
    # Plus difficile, on va chercher les patterns génériques
    pattern4 = r'(\.(pack|grid|place)\([^)]*),\s*(\d+)\)\)'
    matches = list(re.finditer(pattern4, content))
    for match in reversed(matches):
        # Vérifier qu'il n'y a pas déjà un paramètre pady= ou padx=
        if 'pady=' not in match.group(0) and 'padx=' not in match.group(0):
            old_text = match.group(0)
            prefix = match.group(1)
            num = match.group(3)
            # Par défaut, utiliser pady si fill=tk.X ou pady sinon
            if 'fill=tk.X' in old_text or 'fill=tk.Y' in old_text:
                new_text = f"{prefix}, pady={num})"
            else:
                new_text = f"{prefix}, padx={num})"
            content = content[:match.start()] + new_text + content[match.end():]
            fixes_count += 1
            print(f"  Fix: {old_text} -> {new_text}")
    
    if content != original_content:
        # Créer un backup
        backup_path = filepath + '.backup_syntax'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original_content)
        
        # Écrire les corrections
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[OK] {filepath}: {fixes_count} corrections appliquees")
        return fixes_count
    else:
        print(f"[INFO] {filepath}: Aucune correction necessaire")
        return 0

def main():
    """Point d'entree principal"""
    print("="*70)
    print("CORRECTION DES ERREURS DE SYNTAXE")
    print("="*70)
    print()
    
    total_fixes = 0
    
    for filepath in FILES_TO_FIX:
        print(f"\nTraitement de {filepath}...")
        fixes = fix_file(filepath)
        total_fixes += fixes
    
    print()
    print("="*70)
    print(f"[OK] CORRECTION TERMINEE - {total_fixes} corrections au total")
    print("="*70)

if __name__ == '__main__':
    main()