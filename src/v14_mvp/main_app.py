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


def safe_print(*args, **kwargs):
    """Print sécurisé qui fonctionne même en mode GUI (console=False)"""
    if sys.stdout is not None:
        try:
            print(*args, **kwargs)
        except:
            pass  # Ignore les erreurs de print en mode GUI


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
        safe_print("🔄 Chargement des données...")
        self.programs_data = self._load_programs()
        self.tools_data = self._load_tools()
        self.config_data = {}
        self.current_page_widget = None

        safe_print(f"✅ {len(self.programs_data)} catégories chargées")
        safe_print(f"✅ {sum(len(apps) for apps in self.programs_data.values())} applications")
        
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
                safe_print(f"⚠️ Fichier non trouvé: {programs_path}")
                return {}
        except Exception as e:
            safe_print(f"❌ Erreur chargement programmes: {e}")
            import traceback
            if sys.stdout is not None:
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
                safe_print("⚠️ Module tools_data_complete introuvable")
                return {}
        except Exception as e:
            safe_print(f"⚠️ Erreur chargement tools: {e}")
            import traceback
            if sys.stdout is not None:
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
        # Configurer encodage UTF-8 pour Windows (seulement si console disponible)
        if sys.platform == 'win32' and sys.stdout is not None:
            import io
            if hasattr(sys.stdout, 'buffer') and sys.stdout.buffer is not None:
                sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            if hasattr(sys.stderr, 'buffer') and sys.stderr.buffer is not None:
                sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

        # Vérifier Python 3.8-3.12
        py_version = sys.version_info
        if py_version.major != 3 or py_version.minor < 8 or py_version.minor > 12:
            # En mode GUI, on ne peut pas afficher ces messages
            # L'application ne se lancera simplement pas
            return

        safe_print(f"[OK] Python {py_version.major}.{py_version.minor}.{py_version.micro}")
        safe_print("[>>] Lancement NiTriTe V17 Beta...")
        safe_print(f"[..] Répertoire: {os.getcwd()}")
        safe_print()

        # Lancer app
        safe_print("[..] Création de l'instance NiTriTeV17...")
        app = NiTriTeV17()
        safe_print("[OK] Instance créée")
        safe_print("[>>] Démarrage mainloop...")
        app.mainloop()
        safe_print("[OK] Application fermée normalement")

    except KeyboardInterrupt:
        safe_print("\n[!] Interruption utilisateur (Ctrl+C)")

    except Exception as e:
        # En mode GUI, afficher une messagebox au lieu de print
        if sys.stdout is None:
            # Mode GUI - afficher une fenêtre d'erreur
            try:
                import tkinter.messagebox as messagebox
                error_msg = f"ERREUR CRITIQUE\n\n{type(e).__name__}: {e}\n\nL'application ne peut pas démarrer."
                messagebox.showerror("NiTriTe V17 - Erreur", error_msg)
            except:
                pass  # Si même ça échoue, on ne peut rien faire
        else:
            # Mode console
            safe_print(f"\n{'='*60}")
            safe_print(f"[X] ERREUR CRITIQUE")
            safe_print(f"{'='*60}")
            safe_print(f"Type: {type(e).__name__}")
            safe_print(f"Message: {e}")
            safe_print(f"\n[i] Traceback complet:")
            safe_print(f"{'-'*60}")
            import traceback
            traceback.print_exc()
            safe_print(f"{'-'*60}")
            safe_print(f"\n[?] Conseils:")
            safe_print(f"  - Vérifiez que tous les fichiers sont présents dans src/v14_mvp/")
            safe_print(f"  - Vérifiez data/programs.json existe")
            safe_print(f"  - Essayez de réinstaller: pip install --upgrade customtkinter")
            safe_print(f"\n{'='*60}")
            if sys.stdin is not None:
                input("\nAppuyez sur Entrée pour quitter...")


if __name__ == "__main__":
    main()
    # Ne demander input que si stdin existe (mode console)
    if sys.stdin is not None:
        input("\nAppuyez sur Entrée pour fermer la fenêtre...")