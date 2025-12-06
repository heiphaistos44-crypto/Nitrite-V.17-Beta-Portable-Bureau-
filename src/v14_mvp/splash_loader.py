#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Splash Screen avec Chargement - NiTriTe V17
Charge toutes les données avant d'afficher l'interface
"""

import customtkinter as ctk
import tkinter as tk
import os
import sys
from pathlib import Path
import json
import threading
import time
from v14_mvp.design_system import DesignTokens

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.abspath(os.path.join(base_path, relative_path))

class SplashScreen(ctk.CTkToplevel):
    """Splash screen avec barre de progression"""
    
    def __init__(self, parent, on_complete):
        super().__init__(parent)
        
        self.on_complete = on_complete
        self.data_loaded = {}
        
        # Configuration fenêtre
        self.title("NiTriTe V17")
        self.geometry("600x400")
        self.resizable(False, False)
        
        # Centrer
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.winfo_screenheight() // 2) - (400 // 2)
        self.geometry(f"600x400+{x}+{y}")
        
        # Retirer bordures
        self.overrideredirect(True)
        
        # UI
        self._create_ui()
        
        # Démarrer chargement
        self.after(100, self._start_loading)
    
    def _create_ui(self):
        """Créer interface"""
        # Container principal
        main = ctk.CTkFrame(
            self,
            fg_color=DesignTokens.BG_PRIMARY,
            corner_radius=DesignTokens.RADIUS_LG,
            border_width=2,
            border_color=DesignTokens.ACCENT_PRIMARY
        )
        main.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Logo/Titre
        title = ctk.CTkLabel(
            main,
            text="🚀 NiTriTe V17",
            font=(DesignTokens.FONT_FAMILY, 48, "bold"),
            text_color=DesignTokens.ACCENT_PRIMARY
        )
        title.pack(pady=(60, 10))
        
        subtitle = ctk.CTkLabel(
            main,
            text="Maintenance Informatique Professionnelle",
            font=(DesignTokens.FONT_FAMILY, 16),
            text_color=DesignTokens.TEXT_SECONDARY
        )
        subtitle.pack(pady=(0, 40))
        
        # Barre de progression
        self.progress = ctk.CTkProgressBar(
            main,
            width=400,
            height=20,
            corner_radius=10,
            fg_color=DesignTokens.BG_SECONDARY,
            progress_color=DesignTokens.ACCENT_PRIMARY
        )
        self.progress.pack(pady=20)
        self.progress.set(0)
        
        # Label statut
        self.status_label = ctk.CTkLabel(
            main,
            text="Initialisation...",
            font=(DesignTokens.FONT_FAMILY, 14),
            text_color=DesignTokens.TEXT_TERTIARY
        )
        self.status_label.pack(pady=10)
        
        # Stats
        self.stats_label = ctk.CTkLabel(
            main,
            text="",
            font=(DesignTokens.FONT_FAMILY, 12),
            text_color=DesignTokens.TEXT_TERTIARY
        )
        self.stats_label.pack(pady=5)
        
        # Version
        version = ctk.CTkLabel(
            main,
            text="Version 17.0 Beta",
            font=(DesignTokens.FONT_FAMILY, 10),
            text_color=DesignTokens.TEXT_TERTIARY
        )
        version.pack(side=tk.BOTTOM, pady=20)
    
    def _start_loading(self):
        """Démarrer chargement en thread"""
        thread = threading.Thread(target=self._load_data, daemon=True)
        thread.start()
    
    def _load_data(self):
        """Charger toutes les données"""
        try:
            # Étape 1: Programmes
            self._update_status("Chargement des applications...", 0.2)
            time.sleep(0.3)
            
            programs_path = resource_path(os.path.join('data', 'programs.json'))
            if os.path.exists(programs_path):
                with open(programs_path, 'r', encoding='utf-8') as f:
                    self.data_loaded['programs'] = json.load(f)
                    
                    # Compter apps
                    total_apps = sum(len(apps) for apps in self.data_loaded['programs'].values())
                    self._update_stats(f"✅ {total_apps} applications chargées")
            else:
                self.data_loaded['programs'] = {}
                self._update_stats("⚠️ Fichier programmes introuvable")
            
            # Étape 2: Outils
            self._update_status("Chargement des outils système...", 0.5)
            time.sleep(0.3)
            
            try:
                import importlib.util
                module_path = resource_path(os.path.join('src', 'tools_data_complete.py'))
                spec = importlib.util.spec_from_file_location(
                    "tools_data_complete",
                    module_path
                )
                if spec and spec.loader:
                    tools_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(tools_module)
                    self.data_loaded['tools'] = tools_module.get_all_tools()
                    
                    # Compter outils
                    total_tools = sum(len(tools) for tools in self.data_loaded['tools'].values())
                    self._update_stats(f"✅ {total_tools} outils chargés")
                else:
                    self.data_loaded['tools'] = {}
            except Exception as e:
                print(f"⚠️ Erreur chargement outils: {e}")
                self.data_loaded['tools'] = {}
            
            # Étape 3: Configuration
            self._update_status("Chargement de la configuration...", 0.7)
            time.sleep(0.2)
            
            config_path = Path("data/config.json")
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.data_loaded['config'] = json.load(f)
            else:
                self.data_loaded['config'] = {}
            
            # Étape 4: Finalisation
            self._update_status("Préparation de l'interface...", 0.9)
            time.sleep(0.3)
            
            # Complet
            self._update_status("✅ Chargement terminé!", 1.0)
            time.sleep(0.5)
            
            # Callback dans le thread principal
            self.after(100, self._complete)
            
        except Exception as e:
            print(f"❌ Erreur chargement: {e}")
            import traceback
            traceback.print_exc()
            self.after(100, self._complete)
    
    def _update_status(self, text, progress):
        """Mettre à jour statut"""
        def update():
            self.status_label.configure(text=text)
            self.progress.set(progress)
        
        self.after(0, update)
    
    def _update_stats(self, text):
        """Mettre à jour stats"""
        def update():
            current = self.stats_label.cget("text")
            if current:
                self.stats_label.configure(text=f"{current}\n{text}")
            else:
                self.stats_label.configure(text=text)
        
        self.after(0, update)
    
    def _complete(self):
        """Chargement terminé"""
        self.withdraw()
        self.on_complete(self.data_loaded)
        self.destroy()