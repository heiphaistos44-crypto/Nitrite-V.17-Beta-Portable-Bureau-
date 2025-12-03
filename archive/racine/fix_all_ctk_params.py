#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de correction finale de tous les paramètres CustomTkinter
Corrige TOUS les paramètres bg= et fg= restants
"""

import re
import os
import sys
from pathlib import Path

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Fichiers à corriger
FILES_TO_FIX = [
    'src/gui_modern_v13.py',
    'src/advanced_pages.py',
    'src/splash_screen.py',
    'src/monitoring_dashboard.py',
    'src/network_tools_gui.py',
    'src/script_automation_gui.py',
]

def fix_ctk_params_in_file(filepath):
    """Corrige tous les paramètres bg= et fg= dans un fichier"""
    
    if not os.path.exists(filepath):
        print(f"❌ Fichier introuvable: {filepath}")
        return 0
    
    # Lire le contenu
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    fixes_count = 0
    
    # Pattern 1: widget.config(bg=..., fg=...) -> widget.configure(fg_color=..., text_color=...)
    # Remplacer .config( par .configure(
    content = re.sub(
        r'\.config\(',
        r'.configure(',
        content
    )
    
    # Pattern 2: bg=COLOR -> fg_color=COLOR (dans les appels de widgets)
    # Chercher bg= qui n'est pas déjà dans fg_color= ou bg_color=
    pattern_bg = r'\bbg\s*=\s*'
    matches_bg = re.finditer(pattern_bg, content)
    
    # Compter et remplacer de la fin vers le début pour éviter les décalages
    bg_positions = [(m.start(), m.end()) for m in matches_bg]
    for start, end in reversed(bg_positions):
        # Vérifier qu'on n'est pas dans un commentaire
        line_start = content.rfind('\n', 0, start) + 1
        line = content[line_start:start]
        if '#' not in line:
            content = content[:start] + 'fg_color=' + content[end:]
            fixes_count += 1
    
    # Pattern 3: fg=COLOR -> text_color=COLOR
    pattern_fg = r'\bfg\s*=\s*'
    matches_fg = re.finditer(pattern_fg, content)
    
    fg_positions = [(m.start(), m.end()) for m in matches_fg]
    for start, end in reversed(fg_positions):
        line_start = content.rfind('\n', 0, start) + 1
        line = content[line_start:start]
        if '#' not in line:
            content = content[:start] + 'text_color=' + content[end:]
            fixes_count += 1
    
    # Pattern 4: justify=tk.CENTER (certains widgets CTk n'acceptent pas justify)
    # On va le supprimer pour les CTkLabel uniquement
    content = re.sub(
        r',\s*justify\s*=\s*tk\.[A-Z]+\s*(?=\n\s*\))',
        '',
        content
    )
    
    if content != original_content:
        # Créer un backup
        backup_path = filepath + '.backup_final'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original_content)
        
        # Écrire les corrections
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[OK] {filepath}: {fixes_count} corrections appliquees (backup: {backup_path})")
        return fixes_count
    else:
        print(f"[INFO] {filepath}: Aucune correction necessaire")
        return 0

def main():
    """Point d'entree principal"""
    print("="*70)
    print("CORRECTION FINALE DES PARAMETRES CUSTOMTKINTER")
    print("="*70)
    print()
    
    total_fixes = 0
    
    for filepath in FILES_TO_FIX:
        fixes = fix_ctk_params_in_file(filepath)
        total_fixes += fixes
    
    print()
    print("="*70)
    print(f"[OK] CORRECTION TERMINEE - {total_fixes} parametres corriges au total")
    print("="*70)

if __name__ == '__main__':
    main()