#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de conversion automatique tk → ctk
Convertit tous les widgets Tkinter standard en CustomTkinter
"""

import os
import re
from pathlib import Path

# Configuration UTF-8 pour Windows
import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def convert_widget_calls(content):
    """Convertir les appels de widgets tk en ctk"""
    conversions = {
        # Frames
        r'tk\.Frame\(': 'ctk.CTkFrame(',
        r'ttk\.Frame\(': 'ctk.CTkFrame(',
        
        # Labels
        r'tk\.Label\(': 'ctk.CTkLabel(',
        r'ttk\.Label\(': 'ctk.CTkLabel(',
        
        # Buttons
        r'tk\.Button\(': 'ctk.CTkButton(',
        r'ttk\.Button\(': 'ctk.CTkButton(',
        
        # Entry
        r'tk\.Entry\(': 'ctk.CTkEntry(',
        r'ttk\.Entry\(': 'ctk.CTkEntry(',
        
        # Text (pas de CTkText, garder scrolledtext pour zones de log)
        # r'tk\.Text\(': 'ctk.CTkTextbox(',
    }
    
    for pattern, replacement in conversions.items():
        content = re.sub(pattern, replacement, content)
    
    return content

def convert_widget_config(content):
    """Convertir les paramètres de configuration"""
    # bg → fg_color
    content = re.sub(r'\bbg\s*=\s*', 'fg_color=', content)
    
    # fg → text_color (pour labels/buttons)
    content = re.sub(r'\bfg\s*=\s*', 'text_color=', content)
    
    # Convertir les classes héritées
    content = re.sub(r'class\s+(\w+)\(tk\.Frame\):', r'class \1(ctk.CTkFrame):', content)
    content = re.sub(r'class\s+(\w+)\(ttk\.Frame\):', r'class \1(ctk.CTkFrame):', content)
    
    return content

def backup_file(file_path):
    """Créer une sauvegarde du fichier"""
    backup_path = file_path.parent / f"{file_path.stem}_backup{file_path.suffix}"
    if not backup_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[BACKUP] Sauvegarde creee: {backup_path.name}")
        return True
    return False

def convert_file(file_path):
    """Convertir un fichier Python"""
    try:
        print(f"\n[TRAITEMENT] {file_path.name}")
        
        # Lire le contenu
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Compter les widgets avant
        tk_frame_before = len(re.findall(r'tk\.Frame\(', content))
        tk_label_before = len(re.findall(r'tk\.Label\(', content))
        tk_button_before = len(re.findall(r'tk\.Button\(', content))
        
        # Créer backup
        backup_file(file_path)
        
        # Convertir les widgets
        content = convert_widget_calls(content)
        
        # Convertir les paramètres (ATTENTION: peut casser certaines choses)
        # content = convert_widget_config(content)
        
        # Compter après
        tk_frame_after = len(re.findall(r'tk\.Frame\(', content))
        tk_label_after = len(re.findall(r'tk\.Label\(', content))
        tk_button_after = len(re.findall(r'tk\.Button\(', content))
        
        # Afficher stats
        if original_content != content:
            print(f"  [CONVERSIONS]")
            if tk_frame_before != tk_frame_after:
                print(f"    tk.Frame: {tk_frame_before} → {tk_frame_after} ({tk_frame_before - tk_frame_after} convertis)")
            if tk_label_before != tk_label_after:
                print(f"    tk.Label: {tk_label_before} → {tk_label_after} ({tk_label_before - tk_label_after} convertis)")
            if tk_button_before != tk_button_after:
                print(f"    tk.Button: {tk_button_before} → {tk_button_after} ({tk_button_before - tk_button_after} convertis)")
            
            # Écrire le fichier converti
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  [OK] Fichier converti avec succes")
            return True
        else:
            print(f"  [SKIP] Aucune conversion necessaire")
            return False
            
    except Exception as e:
        print(f"  [ERREUR] {e}")
        return False

def main():
    """Fonction principale"""
    print("="*80)
    print("CONVERSION AUTOMATIQUE TK → CTK")
    print("="*80)
    
    # Fichiers à convertir (ordre de priorité)
    files_to_convert = [
        "src/gui_modern_v13.py",
        "src/advanced_pages.py",
        "src/monitoring_dashboard.py",
        "src/network_tools_gui.py",
        "src/script_automation_gui.py",
        "src/splash_screen.py",
    ]
    
    converted_count = 0
    error_count = 0
    
    for file_path_str in files_to_convert:
        file_path = Path(file_path_str)
        if file_path.exists():
            if convert_file(file_path):
                converted_count += 1
        else:
            print(f"\n[ERREUR] Fichier introuvable: {file_path_str}")
            error_count += 1
    
    print("\n" + "="*80)
    print("RESUME")
    print("="*80)
    print(f"Fichiers convertis: {converted_count}")
    print(f"Erreurs: {error_count}")
    print(f"\nATTENTION: Les fichiers originaux sont sauvegardes avec '_backup'")
    print(f"Si probleme, renommez les fichiers _backup pour restaurer.")
    print("="*80)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERREUR FATALE] {e}")
        import traceback
        traceback.print_exc()