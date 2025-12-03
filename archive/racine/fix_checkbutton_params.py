#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de correction des tk.Checkbutton avec des paramètres CustomTkinter
Convertit fg_color= en bg= pour les widgets Tkinter standard
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
]

def fix_file(filepath):
    """Corrige les tk.Checkbutton dans un fichier"""
    
    if not os.path.exists(filepath):
        print(f"[ERROR] Fichier introuvable: {filepath}")
        return 0
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    fixes_count = 0
    
    # Trouver tous les tk.Checkbutton
    pattern = r'(tk\.Checkbutton\s*\([^)]*?\))'
    matches = list(re.finditer(pattern, content, re.DOTALL))
    
    print(f"  Trouve {len(matches)} tk.Checkbutton")
    
    # Pour chaque Checkbutton, vérifier s'il contient fg_color=
    for match in reversed(matches):
        checkbutton_code = match.group(1)
        
        # Vérifier si fg_color= est présent
        if 'fg_color=' in checkbutton_code:
            # Remplacer fg_color= par bg=
            new_code = checkbutton_code.replace('fg_color=', 'bg=')
            
            # Remplacer dans le contenu
            content = content[:match.start()] + new_code + content[match.end():]
            fixes_count += 1
            
            print(f"    Fix: Remplace fg_color= par bg= dans Checkbutton")
        
        # Vérifier si text_color= est présent (non supporté par tk.Checkbutton)
        if 'text_color=' in checkbutton_code:
            # Remplacer text_color= par fg=
            new_code = checkbutton_code.replace('text_color=', 'fg=')
            content = content[:match.start()] + new_code + content[match.end():]
            fixes_count += 1
            print(f"    Fix: Remplace text_color= par fg= dans Checkbutton")
    
    # Aussi corriger les paramètres activeforeground/activebackground dans les CTk widgets
    # (ils ne sont pas supportés par CustomTkinter)
    content = re.sub(r',\s*activeforeground\s*=\s*[^,\)]+', '', content)
    content = re.sub(r',\s*activebackground\s*=\s*[^,\)]+', '', content)
    
    if content != original_content:
        # Créer un backup
        backup_path = filepath + '.backup_checkbutton'
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
    print("CORRECTION DES TK.CHECKBUTTON")
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