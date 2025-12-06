#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Application Principale - NiTriTe V17 Beta
Point d'entrée principal avec architecture moderne
"""


import sys
import os
# Ajoute le dossier src/ au sys.path si nécessaire (PyInstaller)
if getattr(sys, 'frozen', False):
    # Exécution dans l'exécutable PyInstaller
    base_path = sys._MEIPASS
    src_path = os.path.join(base_path, 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
else:
    # Exécution normale (dev)
    src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if src_path not in sys.path:
        sys.path.insert(0, src_path)


import customtkinter as ctk
import tkinter as tk
import json
import os
import sys
from pathlib import Path

# --- Correction import dynamique du package v14_mvp ---
try:
    from v14_mvp import design_system
except ModuleNotFoundError:
    # Ajoute src/ au sys.path si le package n'est pas trouvable
    current_dir = os.path.abspath(os.path.dirname(__file__))
    src_dir = os.path.abspath(os.path.join(current_dir, '..'))
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.abspath(os.path.join(base_path, relative_path))

from v14_mvp.design_system import DesignTokens, ModernColors
from v14_mvp.navigation import ModernNavigation
from v14_mvp.pages_simple import SimplePlaceholderPage
from v14_mvp.pages_optimized import OptimizedApplicationsPage, OptimizedToolsPage
from v14_mvp.pages_settings import SettingsPage
from v14_mvp.pages_full import UpdatesPage, BackupPage, DiagnosticPage, OptimizationsPage
from v14_mvp.page_master_install import MasterInstallPage
from v14_mvp.page_portables import PortableAppsPage
from v14_mvp.page_terminal import TerminalPage
from v14_mvp.splash_loader import SplashScreen


class NiTriTeV17(ctk.CTk):
    """Application principale NiTriTe V17"""

    def __init__(self):
        super().__init__()

        # Configuration base
        self.title("NiTriTe V17.0 Beta - Maintenance Informatique Professionnelle")
        self.geometry("1400x800")
        self.minsize(1200, 700)
        
        # Maximiser la fenêtre au démarrage
        try:
            self.state('zoomed')  # Windows
        except:
            pass  # Ignorer si erreur
        
        # Thème
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Charger données directement (sans splash temporairement)
        print("🔄 Chargement des données...")
        self.programs_data = self._load_programs()
        self.tools_data = self._load_tools()
        self.config_data = {}
        self.current_page_widget = None
        
        print(f"✅ {len(self.programs_data)} catégories chargées")
        print(f"✅ {sum(len(apps) for apps in self.programs_data.values())} applications")
        
        # Créer UI
        self._create_main_layout()
        
        # Charger page par défaut
        self._show_page("applications")
    
    def _load_programs(self):
        """Charger données programmes (compatible PyInstaller et bureau)"""
        try:
            # Cherche toujours à la racine du projet (data/programs.json)
            programs_path = resource_path(os.path.join('data', 'programs.json'))
            if not os.path.exists(programs_path):
                # Fallback chemin absolu depuis cwd
                programs_path = os.path.abspath(os.path.join(os.getcwd(), 'data', 'programs.json'))
            if os.path.exists(programs_path):
                with open(programs_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                print(f"⚠️ Fichier non trouvé: {programs_path}")
                return {}
        except Exception as e:
            print(f"❌ Erreur chargement programmes: {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def _load_tools(self):
        """Charger données outils (compatible PyInstaller et bureau)"""
        try:
            import importlib.util
            # Cherche toujours src/tools_data_complete.py à la racine du projet
            module_path = resource_path(os.path.join('src', 'tools_data_complete.py'))
            if not os.path.exists(module_path):
                # Fallback chemin absolu depuis cwd
                module_path = os.path.abspath(os.path.join(os.getcwd(), 'src', 'tools_data_complete.py'))
            if not os.path.exists(module_path):
                # Essai chemin alternatif (PyInstaller peut extraire à la racine)
                module_path = resource_path('tools_data_complete.py')
            spec = importlib.util.spec_from_file_location(
                "tools_data_complete",
                module_path
            )
            if spec and spec.loader:
                tools_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(tools_module)
                return tools_module.get_all_tools()
            else:
                print("⚠️ Module tools_data_complete introuvable")
                return {}
        except Exception as e:
            print(f"⚠️ Erreur chargement tools: {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def _create_main_layout(self):
        """Créer layout principal"""
        # Container principal
        main_container = ctk.CTkFrame(self, fg_color=DesignTokens.BG_PRIMARY)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Navigation
        self.navigation = ModernNavigation(
            main_container,
            on_page_change=self._show_page
        )
        self.navigation.pack(side=tk.LEFT, fill=tk.Y)
        
        # Container contenu
        self.content_container = ctk.CTkFrame(
            main_container,
            fg_color=DesignTokens.BG_PRIMARY
        )
        self.content_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def _show_page(self, page_id):
        """Afficher une page"""
        # Nettoyer page actuelle
        if self.current_page_widget:
            self.current_page_widget.pack_forget()
            self.current_page_widget.destroy()
        
        # Créer nouvelle page
        if page_id == "applications":
            self.current_page_widget = OptimizedApplicationsPage(
                self.content_container,
                self.programs_data
            )
        
        elif page_id == "tools":
            self.current_page_widget = OptimizedToolsPage(
                self.content_container,
                self.tools_data
            )
        
        elif page_id == "master_install":
            self.current_page_widget = MasterInstallPage(
                self.content_container,
                self.programs_data
            )
        
        elif page_id == "portables":
            self.current_page_widget = PortableAppsPage(
                self.content_container
            )
        
        elif page_id == "terminal":
            self.current_page_widget = TerminalPage(
                self.content_container
            )
        
        elif page_id == "updates":
            self.current_page_widget = UpdatesPage(
                self.content_container
            )
        
        elif page_id == "backup":
            self.current_page_widget = BackupPage(
                self.content_container
            )
        
        elif page_id == "optimizations":
            self.current_page_widget = OptimizationsPage(
                self.content_container
            )
        
        elif page_id == "diagnostic":
            self.current_page_widget = DiagnosticPage(
                self.content_container
            )
        
        elif page_id == "settings":
            self.current_page_widget = SettingsPage(
                self.content_container
            )
        
        # Afficher nouvelle page
        if self.current_page_widget:
            self.current_page_widget.pack(fill=tk.BOTH, expand=True)


def main():
    """Point d'entrée"""
    try:
        # Configurer encodage UTF-8 pour Windows
        if sys.platform == 'win32':
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
        
        # Vérifier Python 3.8-3.12
        py_version = sys.version_info
        if py_version.major != 3 or py_version.minor < 8 or py_version.minor > 12:
            print(f"[X] ERREUR: Python {py_version.major}.{py_version.minor} détecté")
            print("[!] CustomTkinter requiert Python 3.8-3.12")
            print("[>] Téléchargez Python 3.12: https://www.python.org/downloads/")
            input("\nAppuyez sur Entrée pour quitter...")
            return
        
        print(f"[OK] Python {py_version.major}.{py_version.minor}.{py_version.micro}")
        print("[>>] Lancement NiTriTe V17 Beta...")
        print(f"[..] Répertoire: {os.getcwd()}")
        print()

        # Lancer app
        print("[..] Création de l'instance NiTriTeV17...")
        app = NiTriTeV17()
        print("[OK] Instance créée")
        print("[>>] Démarrage mainloop...")
        app.mainloop()
        print("[OK] Application fermée normalement")
    
    except KeyboardInterrupt:
        print("\n[!] Interruption utilisateur (Ctrl+C)")
    
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"[X] ERREUR CRITIQUE")
        print(f"{'='*60}")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {e}")
        print(f"\n[i] Traceback complet:")
        print(f"{'-'*60}")
        import traceback
        traceback.print_exc()
        print(f"{'-'*60}")
        print(f"\n[?] Conseils:")
        print(f"  - Vérifiez que tous les fichiers sont présents dans src/v14_mvp/")
        print(f"  - Vérifiez data/programs.json existe")
        print(f"  - Essayez de réinstaller: pip install --upgrade customtkinter")
        print(f"\n{'='*60}")
        input("\nAppuyez sur Entrée pour quitter...")


if __name__ == "__main__":
    main()
    input("\nAppuyez sur Entrée pour fermer la fenêtre...")