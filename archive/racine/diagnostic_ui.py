#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnostic UI pour NiTriTe V13
Détecte tous les problèmes d'affichage et de compatibilité CustomTkinter
"""

import sys
import os
import io
import logging
from datetime import datetime
from pathlib import Path

# Configuration UTF-8 pour Windows (OBLIGATOIRE)
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Ajouter src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Configuration logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
log_file = log_dir / f"diagnostic_ui_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def check_imports():
    """Vérifier toutes les dépendances"""
    logger.info("="*80)
    logger.info("DIAGNOSTIC - VÉRIFICATION DES IMPORTS")
    logger.info("="*80)
    
    imports_to_check = [
        ("tkinter", "tk"),
        ("tkinter.ttk", "ttk"),
        ("customtkinter", "ctk"),
        ("PIL", "Pillow"),
        ("requests", None),
        ("psutil", None),
    ]
    
    missing = []
    for module_name, package_name in imports_to_check:
        try:
            __import__(module_name)
            logger.info(f"✓ {module_name} - OK")
        except ImportError as e:
            pkg = package_name or module_name
            logger.error(f"✗ {module_name} - MANQUANT (pip install {pkg})")
            missing.append(pkg)
    
    return missing

def check_customtkinter():
    """Vérifier la version et configuration de CustomTkinter"""
    logger.info("\n" + "="*80)
    logger.info("DIAGNOSTIC - CUSTOMTKINTER")
    logger.info("="*80)
    
    try:
        import customtkinter as ctk
        logger.info(f"✓ CustomTkinter version: {ctk.__version__}")
        
        # Tester création fenêtre
        test_window = ctk.CTk()
        test_window.withdraw()  # Cacher la fenêtre
        logger.info("✓ Création fenêtre CTk - OK")
        
        # Tester widgets de base
        test_frame = ctk.CTkFrame(test_window)
        logger.info("✓ CTkFrame - OK")
        
        test_label = ctk.CTkLabel(test_window, text="Test")
        logger.info("✓ CTkLabel - OK")
        
        test_button = ctk.CTkButton(test_window, text="Test")
        logger.info("✓ CTkButton - OK")
        
        test_window.destroy()
        return True
        
    except Exception as e:
        logger.error(f"✗ Erreur CustomTkinter: {e}", exc_info=True)
        return False

def check_mixed_widgets():
    """Détecter les widgets mixtes tk/ctk dans le code"""
    logger.info("\n" + "="*80)
    logger.info("DIAGNOSTIC - WIDGETS MIXTES (TK vs CTK)")
    logger.info("="*80)
    
    problematic_files = []
    src_dir = Path("src")
    
    # Patterns problématiques
    tk_patterns = [
        "tk.Frame(",
        "tk.Label(",
        "tk.Button(",
        "tk.Entry(",
        "tk.Text(",
        "ttk.Frame(",
        "ttk.Label(",
        "ttk.Button(",
    ]
    
    for py_file in src_dir.glob("*.py"):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            issues = []
            for pattern in tk_patterns:
                if pattern in content:
                    count = content.count(pattern)
                    issues.append(f"{pattern}: {count}x")
            
            if issues:
                logger.warning(f"⚠️  {py_file.name}:")
                for issue in issues:
                    logger.warning(f"   - {issue}")
                problematic_files.append(py_file.name)
                
        except Exception as e:
            logger.error(f"Erreur lecture {py_file}: {e}")
    
    if problematic_files:
        logger.warning(f"\n⚠️  {len(problematic_files)} fichiers avec widgets mixtes détectés")
    else:
        logger.info("✓ Aucun widget mixte détecté")
    
    return problematic_files

def check_colors_usage():
    """Vérifier l'utilisation des couleurs"""
    logger.info("\n" + "="*80)
    logger.info("DIAGNOSTIC - CONFIGURATION COULEURS")
    logger.info("="*80)
    
    try:
        from modern_colors import ModernColors
        logger.info("✓ Module modern_colors importé")
        
        # Vérifier les couleurs principales
        colors_to_check = [
            "BG_DARK", "BG_MEDIUM", "BG_LIGHT", "BG_CARD",
            "ORANGE_PRIMARY", "TEXT_PRIMARY", "TEXT_SECONDARY"
        ]
        
        for color_name in colors_to_check:
            if hasattr(ModernColors, color_name):
                color_value = getattr(ModernColors, color_name)
                logger.info(f"  {color_name}: {color_value}")
            else:
                logger.error(f"✗ Couleur manquante: {color_name}")
                
    except Exception as e:
        logger.error(f"✗ Erreur import modern_colors: {e}", exc_info=True)

def analyze_gui_file():
    """Analyser le fichier GUI principal"""
    logger.info("\n" + "="*80)
    logger.info("DIAGNOSTIC - ANALYSE GUI_MODERN_V13.PY")
    logger.info("="*80)
    
    gui_file = Path("src/gui_modern_v13.py")
    if not gui_file.exists():
        logger.error(f"✗ Fichier non trouvé: {gui_file}")
        return
    
    try:
        with open(gui_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Compter les imports
        ctk_imports = content.count("import customtkinter")
        tk_imports = content.count("import tkinter")
        
        logger.info(f"Imports CustomTkinter: {ctk_imports}")
        logger.info(f"Imports Tkinter: {tk_imports}")
        
        # Compter les widgets
        ctk_widgets = content.count("ctk.CTk")
        tk_widgets = content.count("tk.Frame") + content.count("tk.Label") + content.count("tk.Button")
        
        logger.info(f"Widgets CustomTkinter: {ctk_widgets}")
        logger.info(f"Widgets Tkinter standard: {tk_widgets}")
        
        if tk_widgets > ctk_widgets * 0.5:
            logger.warning("⚠️  PROBLÈME: Trop de widgets Tkinter standard vs CustomTkinter")
            logger.warning("   Cela peut causer des problèmes d'affichage!")
        
    except Exception as e:
        logger.error(f"✗ Erreur analyse GUI: {e}", exc_info=True)

def test_simple_window():
    """Tester une fenêtre simple pour isoler le problème"""
    logger.info("\n" + "="*80)
    logger.info("TEST - FENÊTRE SIMPLE CUSTOMTKINTER")
    logger.info("="*80)
    
    try:
        import customtkinter as ctk
        
        # Test 1: Fenêtre basique
        logger.info("Test 1: Création fenêtre basique...")
        root = ctk.CTk()
        root.title("Test NiTriTe")
        root.geometry("400x300")
        
        # Test 2: Frame avec couleur
        logger.info("Test 2: Frame avec couleur...")
        frame = ctk.CTkFrame(root, fg_color="#1a1a1a")
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Test 3: Label
        logger.info("Test 3: Label avec texte...")
        label = ctk.CTkLabel(
            frame,
            text="Test d'affichage",
            font=("Segoe UI", 16),
            text_color="#ffffff"
        )
        label.pack(pady=20)
        
        # Test 4: Button
        logger.info("Test 4: Bouton...")
        button = ctk.CTkButton(
            frame,
            text="Test Button",
            fg_color="#FF6B35",
            hover_color="#ff8555"
        )
        button.pack(pady=10)
        
        logger.info("✓ Tous les widgets créés avec succès")
        logger.info("Fermeture automatique dans 2 secondes...")
        
        root.after(2000, root.destroy)
        root.mainloop()
        
        logger.info("✓ Test fenêtre simple - SUCCÈS")
        return True
        
    except Exception as e:
        logger.error(f"✗ Test fenêtre simple - ÉCHEC: {e}", exc_info=True)
        return False

def main():
    """Fonction principale du diagnostic"""
    print("\n" + "="*80)
    print("[DIAGNOSTIC] UI NITRITE V13")
    print("="*80 + "\n")
    
    logger.info("Démarrage du diagnostic...")
    logger.info(f"Fichier log: {log_file}")
    
    # 1. Vérifier les imports
    missing = check_imports()
    
    # 2. Vérifier CustomTkinter
    ctk_ok = check_customtkinter()
    
    # 3. Vérifier widgets mixtes
    mixed_widgets = check_mixed_widgets()
    
    # 4. Vérifier couleurs
    check_colors_usage()
    
    # 5. Analyser GUI
    analyze_gui_file()
    
    # 6. Test simple
    if ctk_ok:
        test_simple_window()
    
    # Résumé
    logger.info("\n" + "="*80)
    logger.info("RÉSUMÉ DU DIAGNOSTIC")
    logger.info("="*80)
    
    if missing:
        logger.error(f"✗ Dépendances manquantes: {', '.join(missing)}")
        logger.error(f"  Installer avec: pip install {' '.join(missing)}")
    else:
        logger.info("✓ Toutes les dépendances sont installées")
    
    if not ctk_ok:
        logger.error("✗ CustomTkinter ne fonctionne pas correctement")
    else:
        logger.info("✓ CustomTkinter fonctionne")
    
    if mixed_widgets:
        logger.warning(f"⚠️  {len(mixed_widgets)} fichiers avec widgets mixtes tk/ctk")
        logger.warning("   RECOMMANDATION: Convertir tous les widgets en CustomTkinter")
    else:
        logger.info("✓ Pas de widgets mixtes détectés")
    
    logger.info(f"\n✓ Diagnostic complet sauvegardé dans: {log_file}")
    print(f"\n✓ Diagnostic terminé! Consultez: {log_file}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"ERREUR FATALE: {e}", exc_info=True)
        print(f"\n[ERREUR] Erreur fatale: {e}")
        try:
            print(f"Voir details dans: {log_file}")
        except:
            print("Voir details dans: logs/diagnostic_ui_*.log")