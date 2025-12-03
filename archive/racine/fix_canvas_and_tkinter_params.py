#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de correction des widgets Tkinter standard (Canvas, etc.)
et des paramètres non supportés par CustomTkinter
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
]

def fix_file(filepath):
    """Corrige un fichier"""
    
    if not os.path.exists(filepath):
        print(f"[ERROR] Fichier introuvable: {filepath}")
        return 0
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    fixes_count = 0
    
    # 1. Corriger tk.Canvas avec fg_color= -> bg=
    # Pattern: tk.Canvas(..., fg_color=COLOR, ...)
    pattern_canvas_fg = r'(tk\.Canvas\([^)]*?)fg_color\s*=\s*'
    matches = list(re.finditer(pattern_canvas_fg, content))
    for match in reversed(matches):
        start = match.end() - len('fg_color=')
        end = match.end()
        content = content[:start] + 'bg=' + content[end:]
        fixes_count += 1
    
    # 2. Corriger splash.configure(fg_color=...) -> splash.configure(bg=...)
    # Pour les widgets Tkinter Toplevel/Tk
    pattern_configure = r'(\.configure\([^)]*?)fg_color\s*=\s*'
    matches = list(re.finditer(pattern_configure, content))
    for match in reversed(matches):
        # Vérifier si c'est un widget Tkinter (pas CTk)
        line_start = content.rfind('\n', 0, match.start())
        line = content[line_start:match.start()]
        if 'self.splash' in line or 'tk.Toplevel' in line or 'tk.Tk' in line:
            start = match.end() - len('fg_color=')
            end = match.end()
            content = content[:start] + 'bg=' + content[end:]
            fixes_count += 1
    
    # 3. Supprimer les paramètres non supportés par CTkButton
    # activebackground, relief, padx, pady
    unsupported_params = ['activebackground', 'relief', 'padx', 'pady']
    
    for param in unsupported_params:
        # Pattern: param=value, (avec ou sans virgule)
        pattern = rf',\s*{param}\s*=\s*[^,\)]+(?=[,\)])'
        content = re.sub(pattern, '', content)
        if pattern in content:
            fixes_count += 1
    
    # 4. Corriger splash_screen.py: self.splash doit être un tk.Toplevel, pas CTk
    if 'splash_screen.py' in filepath:
        # Chercher "self.splash = ctk.CTk()" et remplacer par tk.Toplevel
        content = re.sub(
            r'self\.splash\s*=\s*ctk\.CTk\(\)',
            'self.splash = tk.Toplevel()',
            content
        )
        # Ajouter import tk si nécessaire
        if 'import tkinter as tk' not in content:
            content = 'import tkinter as tk\n' + content
            fixes_count += 1
    
    if content != original_content:
        # Créer un backup
        backup_path = filepath + '.backup_canvas'
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
    print("CORRECTION DES WIDGETS TKINTER ET PARAMETRES NON SUPPORTES")
    print("="*70)
    print()
    
    total_fixes = 0
    
    for filepath in FILES_TO_FIX:
        fixes = fix_file(filepath)
        total_fixes += fixes
    
    print()
    print("="*70)
    print(f"[OK] CORRECTION TERMINEE - {total_fixes} corrections au total")
    print("="*70)

if __name__ == '__main__':
    main()