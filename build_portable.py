#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de build multi-plateforme pour NiTriTe V17
Fonctionne sur Windows, Linux et macOS
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def print_header(text):
    """Afficher un header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def clean_build():
    """Nettoyer les anciens builds"""
    print("🧹 Nettoyage des anciens builds...")

    dirs_to_clean = ['dist', 'build', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"   Suppression: {dir_name}/")
            shutil.rmtree(dir_name)

    print("✅ Nettoyage terminé\n")

def check_python_version():
    """Vérifier la version de Python"""
    print("🔍 Vérification de Python...")
    py_version = sys.version_info

    if py_version.major != 3 or py_version.minor < 8:
        print(f"❌ ERREUR: Python {py_version.major}.{py_version.minor} détecté")
        print("⚠️  Python 3.8+ requis")
        return False

    print(f"✅ Python {py_version.major}.{py_version.minor}.{py_version.micro}")
    return True

def check_dependencies():
    """Vérifier les dépendances"""
    print("\n📦 Vérification des dépendances...")

    # Mapping package pip → module Python
    required = {
        'customtkinter': 'customtkinter',
        'Pillow': 'PIL',
        'requests': 'requests',
        'psutil': 'psutil',
        'pyinstaller': 'PyInstaller'
    }

    missing = []
    for package, module in required.items():
        try:
            __import__(module)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - MANQUANT")
            missing.append(package)

    if missing:
        print(f"\n⚠️  Dépendances manquantes: {', '.join(missing)}")
        print("📥 Installation automatique...")

        for package in missing:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package])

        print("✅ Installation terminée")

    return True

def check_files():
    """Vérifier que tous les fichiers nécessaires existent"""
    print("\n📁 Vérification des fichiers...")

    required_files = [
        'src/v14_mvp/main_app.py',
        'data/programs.json',
        'NiTriTe_V17_Portable.spec',
    ]

    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - MANQUANT")
            all_exist = False

    # Assets optionnels
    if os.path.exists('assets/logo.ico'):
        print(f"   ✅ assets/logo.ico (icône)")
    else:
        print(f"   ⚠️  assets/logo.ico - optionnel (pas d'icône)")

    return all_exist

def build_executable():
    """Builder l'exécutable avec PyInstaller"""
    print("\n🔨 Build de l'exécutable avec PyInstaller...")
    print("   Cette opération peut prendre plusieurs minutes...\n")

    try:
        # Utiliser python -m PyInstaller pour compatibilité Windows
        result = subprocess.run(
            [sys.executable, '-m', 'PyInstaller', '--noconfirm', '--clean', 'NiTriTe_V17_Portable.spec'],
            check=True,
            capture_output=False,
            text=True
        )

        return True

    except subprocess.CalledProcessError as e:
        print(f"\n❌ ERREUR lors du build:")
        print(f"   Code de sortie: {e.returncode}")
        return False

    except FileNotFoundError:
        print("\n❌ ERREUR: PyInstaller non trouvé")
        print("   Installation: pip install pyinstaller")
        return False

def verify_build():
    """Vérifier que le build a réussi"""
    print("\n🔍 Vérification du build...")

    # Chercher l'exécutable (extension dépend de l'OS)
    exe_name = 'NiTriTe_V17_Portable.exe' if sys.platform == 'win32' else 'NiTriTe_V17_Portable'
    exe_path = Path('dist') / exe_name

    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✅ Exécutable créé: {exe_path}")
        print(f"   Taille: {size_mb:.1f} MB")
        return True
    else:
        print(f"❌ Exécutable non trouvé: {exe_path}")
        return False

def main():
    """Point d'entrée principal"""
    print_header("NiTriTe V17 - Build Portable")

    # 1. Vérifier Python
    if not check_python_version():
        return 1

    # 2. Vérifier dépendances
    if not check_dependencies():
        return 1

    # 3. Vérifier fichiers
    if not check_files():
        print("\n❌ Fichiers manquants - Impossible de continuer")
        return 1

    # 4. Nettoyer
    clean_build()

    # 5. Builder
    print_header("Démarrage du Build")

    if not build_executable():
        print("\n❌ BUILD ÉCHOUÉ")
        return 1

    # 6. Vérifier
    if not verify_build():
        print("\n❌ BUILD ÉCHOUÉ - Exécutable non créé")
        return 1

    # Succès !
    print_header("BUILD RÉUSSI ! 🎉")

    exe_name = 'NiTriTe_V17_Portable.exe' if sys.platform == 'win32' else 'NiTriTe_V17_Portable'
    print(f"✅ Exécutable prêt: dist/{exe_name}")
    print(f"\n📦 Pour distribuer:")
    print(f"   1. Testez l'exécutable: dist/{exe_name}")
    print(f"   2. Vérifiez toutes les fonctionnalités")
    print(f"   3. Distribuez le fichier dist/{exe_name}")
    print("\n" + "="*60 + "\n")

    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Build annulé par l'utilisateur (Ctrl+C)")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERREUR FATALE: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
