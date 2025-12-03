#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de correction des paramètres CustomTkinter
Convertit bg= en fg_color= et fg= en text_color=
"""

import os
import re
from pathlib import Path

# Configuration UTF-8
import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def fix_ctk_parameters(content):
    """Corriger les paramètres pour CustomTkinter"""
    
    # Patterns pour CTk widgets uniquement
    ctk_widgets = r'(ctk\.CTk(?:Frame|Label|Button|Entry|Textbox))\('
    
    # Trouver tous les widgets CTk
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        original_line = line
        
        # Si la ligne contient un widget CTk
        if re.search(ctk_widgets, line):
            # Remplacer bg= par fg_color= (seulement pour CTk widgets)
            if 'bg=' in line and 'fg_color=' not in line:
                line = re.sub(r'\bbg\s*=\s*', 'fg_color=', line)
            
            # Remplacer fg= par text_color= (seulement pour CTk widgets)
            if 'fg=' in line and 'text_color=' not in line:
                line = re.sub(r'\bfg\s*=\s*', 'text_color=', line)
        
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def fix_super_init_calls(content):
    """Corriger les appels super().__init__ avec paramètres tk"""
    lines = content.split('\n')
    fixed_lines = []
    
    in_super_call = False
    for i, line in enumerate(lines):
        # Détecter début super().__init__
        if 'super().__init__(' in line and 'bg=' in line:
            line = line.replace('bg=', 'fg_color=')
        
        if 'super().__init__(' in line and 'fg=' in line:
            line = line.replace('fg=', 'text_color=')
            
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def fix_class_inheritance(content):
    """Corriger les héritages de classes"""
    # Remplacer les héritages tk.Frame par ctk.CTkFrame
    content = re.sub(
        r'class\s+(\w+)\(tk\.Frame\):',
        r'class \1(ctk.CTkFrame):',
        content
    )
    
    return content

def process_file(file_path):
    """Traiter un fichier"""
    try:
        print(f"\n[TRAITEMENT] {file_path.name}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Compter avant
        bg_count_before = content.count('bg=')
        fg_count_before = content.count('fg=')
        
        # Appliquer les corrections
        content = fix_ctk_parameters(content)
        content = fix_super_init_calls(content)
        content = fix_class_inheritance(content)
        
        # Compter après
        bg_count_after = content.count('bg=')
        fg_count_after = content.count('fg=')
        
        if original_content != content:
            print(f"  [CORRECTIONS]")
            if bg_count_before != bg_count_after:
                print(f"    bg= → fg_color=: {bg_count_before - bg_count_after} conversions")
            if fg_count_before != fg_count_after:
                print(f"    fg= → text_color=: {fg_count_before - fg_count_after} conversions")
            
            # Sauvegarder
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  [OK] Fichier corrige")
            return True
        else:
            print(f"  [SKIP] Aucune correction necessaire")
            return False
            
    except Exception as e:
        print(f"  [ERREUR] {e}")
        return False

def main():
    """Fonction principale"""
    print("="*80)
    print("CORRECTION DES PARAMETRES CUSTOMTKINTER")
    print("="*80)
    
    files = [
        "src/gui_modern_v13.py",
        "src/advanced_pages.py",
        "src/monitoring_dashboard.py",
        "src/network_tools_gui.py",
        "src/script_automation_gui.py",
        "src/splash_screen.py",
    ]
    
    fixed_count = 0
    
    for file_path_str in files:
        file_path = Path(file_path_str)
        if file_path.exists():
            if process_file(file_path):
                fixed_count += 1
        else:
            print(f"\n[ERREUR] Fichier introuvable: {file_path_str}")
    
    print("\n" + "="*80)
    print("RESUME")
    print("="*80)
    print(f"Fichiers corriges: {fixed_count}")
    print("\nNOTE: Testez l'application avec: python nitrite_v13_modern.py")
    print("="*80)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERREUR FATALE] {e}")
        import traceback
        traceback.print_exc()