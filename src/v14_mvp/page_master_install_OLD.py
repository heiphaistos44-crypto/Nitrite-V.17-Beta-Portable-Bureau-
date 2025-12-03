#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Page Master Install - NiTriTe V14
Installation de packs d'applications prédéfinis avec édition personnalisée
"""

import customtkinter as ctk
import tkinter as tk
import json
from pathlib import Path
from typing import Dict, List
from v14_mvp.design_system import DesignTokens
from v14_mvp.components import ModernCard, ModernButton
from v14_mvp.installer import installer


class MasterInstallPage(ctk.CTkFrame):
    """Page Master Install avec packs prédéfinis et édition personnalisée"""
    
    def __init__(self, parent, programs_data: Dict):
        super().__init__(parent, fg_color=DesignTokens.BG_PRIMARY)
        
        self.programs_data = programs_data
        self.selected_packs = set()
        
        # Chemin pour sauvegarder packs personnalisés
        self.custom_packs_file = Path.home() / "Documents" / "NiTriTe_CustomPacks.json"
        
        # Définir packs par défaut
        self.default_packs = self._get_default_packs()
        
        # Charger packs personnalisés ou utiliser par défaut
        self.packs = self._load_custom_packs()
        
        self._create_header()
        self._create_content()
    
    def _get_default_packs(self):
        """Obtenir configuration par défaut des packs"""
        return {
            "🎮 Gaming": {
                "description": "Pack complet pour les gamers",
                "apps": [
                    "Steam", "Epic Games", "Discord", "OBS Studio",
                    "GeForce Experience", "GOG Galaxy", "Ubisoft Connect",
                    "EA App", "Battle.net", "Razer Cortex",
                    "MSI Afterburner", "NVIDIA GeForce NOW", "AMD Radeon Software",
                    "TeamSpeak"
                ],
                "color": DesignTokens.SUCCESS
            },
            "💼 Bureau": {
                "description": "Outils essentiels pour le travail",
                "apps": [
                    "Microsoft Office", "Adobe Reader", "7-Zip", "Notepad++",
                    "TeamViewer", "AnyDesk", "Zoom", "Microsoft Teams",
                    "Slack", "LibreOffice", "PDFCreator", "WinRAR",
                    "FreeCommander", "Everything"
                ],
                "color": DesignTokens.INFO
            },
            "💻 Développeur": {
                "description": "Environnement de développement complet",
                "apps": [
                    "Visual Studio Code", "Git", "Python", "Node.js",
                    "Docker", "Postman", "Visual Studio Community", "IntelliJ IDEA",
                    "PyCharm Community", "GitHub Desktop", "FileZilla", "Putty",
                    "WinSCP", "Composer", "PHP", "MySQL Workbench"
                ],
                "color": DesignTokens.ACCENT_PRIMARY
            },
            "🎨 Créatif": {
                "description": "Suite complète pour créatifs",
                "apps": [
                    "GIMP", "Inkscape", "Blender", "Audacity",
                    "OBS Studio", "DaVinci Resolve", "Krita", "Paint.NET",
                    "Shotcut", "HandBrake", "ImageMagick", "XnView"
                ],
                "color": "#9C27B0"
            },
            "🌐 Navigateurs": {
                "description": "Tous les navigateurs web",
                "apps": [
                    "Google Chrome", "Mozilla Firefox", "Microsoft Edge",
                    "Brave", "Opera", "Vivaldi", "Tor Browser",
                    "Waterfox", "LibreWolf", "Chromium"
                ],
                "color": "#FF6F00"
            },
            "🎵 Multimédia": {
                "description": "Lecture et gestion multimédia",
                "apps": [
                    "VLC Media Player", "Spotify", "iTunes", "MusicBee",
                    "Foobar2000", "AIMP", "K-Lite Codec Pack", "MediaInfo",
                    "MPC-HC", "PotPlayer", "Winamp", "Audacity"
                ],
                "color": "#E91E63"
            }
        }
    
    def _load_custom_packs(self):
        """Charger packs personnalisés ou utiliser par défaut"""
        try:
            if self.custom_packs_file.exists():
                with open(self.custom_packs_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ Erreur chargement packs personnalisés: {e}")
        
        return self.default_packs.copy()
    
    def _save_custom_packs(self):
        """Sauvegarder packs personnalisés"""
        try:
            self.custom_packs_file.parent.mkdir(exist_ok=True)
            with open(self.custom_packs_file, 'w', encoding='utf-8') as f:
                json.dump(self.packs, f, indent=2, ensure_ascii=False)
            print(f"✅ Packs personnalisés sauvegardés: {self.custom_packs_file}")
        except Exception as e:
            print(f"❌ Erreur sauvegarde packs: {e}")
    
    def _reset_to_default(self):
        """Restaurer packs par défaut"""
        self.packs = self.default_packs.copy()
        self._save_custom_packs()
        
        # Recréer l'interface
        for widget in self.winfo_children():
            widget.destroy()
        self._create_header()
        self._create_content()
        
        print("✅ Packs restaurés aux valeurs par défaut")
    
    def _create_header(self):
        """Header"""
        header = ModernCard(self)
        header.pack(fill=tk.X, padx=20, pady=10)
        
        container = ctk.CTkFrame(header, fg_color="transparent")
        container.pack(fill=tk.X, padx=20, pady=15)
        
        left_side = ctk.CTkFrame(container, fg_color="transparent")
        left_side.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        title = ctk.CTkLabel(
            left_side,
            text="🚀 Master Install",
            font=(DesignTokens.FONT_FAMILY, 24, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY
        )
        title.pack(side=tk.LEFT)
        
        subtitle = ctk.CTkLabel(
            left_side,
            text="Installation rapide de packs d'applications",
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_MD),
            text_color=DesignTokens.TEXT_SECONDARY
        )
        subtitle.pack(side=tk.LEFT, padx=20)
        
        # Boutons à droite
        right_side = ctk.CTkFrame(container, fg_color="transparent")
        right_side.pack(side=tk.RIGHT)
        
        ModernButton(
            right_side,
            text="🔄 Restaurer Défaut",
            variant="text",
            size="sm",
            command=self._reset_to_default
        ).pack(side=tk.LEFT, padx=5)
        
        ModernButton(
            right_side,
            text="🚀 Installer Sélection",
            variant="filled",
            command=self._install_selected_packs
        ).pack(side=tk.LEFT, padx=5)
    
    def _create_content(self):
        """Contenu"""
        scroll = ctk.CTkScrollableFrame(self, fg_color=DesignTokens.BG_PRIMARY)
        scroll.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Pack OrdiPlus en premier
        ordiplus_card = ModernCard(scroll)
        ordiplus_card.pack(fill=tk.X, pady=10)
        
        self._create_ordiplus_pack(ordiplus_card)
        
        # Boutons activation Windows
        activation_card = ModernCard(scroll)
        activation_card.pack(fill=tk.X, pady=10)
        
        self._create_activation_buttons(activation_card)
        
        # Afficher packs en grille 2 colonnes
        row_frame = None
        for idx, (pack_name, pack_data) in enumerate(self.packs.items()):
            if idx % 2 == 0:
                row_frame = ctk.CTkFrame(scroll, fg_color="transparent")
                row_frame.pack(fill=tk.X, pady=5)
            
            self._create_pack_card(row_frame, pack_name, pack_data)
    
    def _create_ordiplus_pack(self, parent):
        """Pack OrdiPlus spécial"""
        # Header
        header = ctk.CTkFrame(
            parent,
            fg_color=DesignTokens.ACCENT_PRIMARY,
            corner_radius=DesignTokens.RADIUS_MD
        )
        header.pack(fill=tk.X, padx=15, pady=15)
        
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill=tk.X, padx=15, pady=12)
        
        title = ctk.CTkLabel(
            header_content,
            text="⭐ Pack OrdiPlus",
            font=(DesignTokens.FONT_FAMILY, 20, "bold"),
            text_color="#FFFFFF"
        )
        title.pack(anchor="w")
        
        desc = ctk.CTkLabel(
            header_content,
            text="Pack complet optimisé OrdiPlus - Applications essentielles",
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_MD),
            text_color="#FFFFFF"
        )
        desc.pack(anchor="w", pady=(5, 0))
        
        # Liste apps
        apps_frame = ctk.CTkFrame(parent, fg_color=DesignTokens.BG_ELEVATED)
        apps_frame.pack(fill=tk.X, padx=15, pady=10)
        
        apps = [
            "RustDesk (Portable)",
            "Office 2007",
            "Adobe Acrobat Reader",
            "VLC Media Player",
            "Malwarebytes",
            "Spybot Search & Destroy",
            "Wise Disk Cleaner",
            "AdwCleaner (Portable)",
            "Mozilla Firefox",
            "Google Chrome"
        ]
        
        count_label = ctk.CTkLabel(
            apps_frame,
            text=f"📦 {len(apps)} applications incluses",
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM, "bold"),
            text_color=DesignTokens.TEXT_SECONDARY
        )
        count_label.pack(anchor="w", padx=10, pady=10)
        
        # Grille 2 colonnes pour apps
        grid = ctk.CTkFrame(apps_frame, fg_color=DesignTokens.BG_ELEVATED)
        grid.pack(fill=tk.X, padx=10, pady=10)
        
        for idx, app in enumerate(apps):
            row = idx // 2
            col = idx % 2
            
            app_label = ctk.CTkLabel(
                grid,
                text=f"  • {app}",
                font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM),
                text_color=DesignTokens.TEXT_TERTIARY,
                anchor="w"
            )
            app_label.grid(row=row, column=col, sticky="w", padx=10, pady=2)
        
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        
        # Bouton install
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        ModernButton(
            btn_frame,
            text="🚀 Installer Pack OrdiPlus",
            variant="filled",
            command=lambda: self._install_ordiplus_pack(apps)
        ).pack(side=tk.RIGHT)
    
    def _create_activation_buttons(self, parent):
        """Boutons d'activation Windows/Office"""
        # Header
        title = ctk.CTkLabel(
            parent,
            text="🔑 Activation Windows & Office",
            font=(DesignTokens.FONT_FAMILY, 18, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY
        )
        title.pack(fill=tk.X, padx=20, pady=15)
        
        desc = ctk.CTkLabel(
            parent,
            text="Scripts d'activation automatique (nécessite droits administrateur)",
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM),
            text_color=DesignTokens.TEXT_SECONDARY
        )
        desc.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Boutons
        buttons_frame = ctk.CTkFrame(parent, fg_color="transparent")
        buttons_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        ModernButton(
            buttons_frame,
            text="🪟 Activer Windows",
            variant="filled",
            command=self._activate_windows
        ).pack(side=tk.LEFT, padx=5)
        
        ModernButton(
            buttons_frame,
            text="📄 Activer Office",
            variant="outlined",
            command=self._activate_office
        ).pack(side=tk.LEFT, padx=5)
        
        ModernButton(
            buttons_frame,
            text="🔑 Activer Windows + Office",
            variant="filled",
            command=self._activate_both
        ).pack(side=tk.LEFT, padx=5)
        
        # Warning
        warning = ctk.CTkLabel(
            parent,
            text="⚠️ Ces scripts utilisent https://get.activated.win - Lancez PowerShell en Administrateur",
            font=(DesignTokens.FONT_FAMILY, 10),
            text_color=DesignTokens.WARNING
        )
        warning.pack(padx=20, pady=(0, 15))
    
    def _activate_windows(self):
        """Activer Windows"""
        import subprocess
        try:
            cmd = 'powershell -Command "Start-Process powershell -Verb RunAs -ArgumentList \'-Command\', \'irm https://get.activated.win | iex\'"'
            subprocess.Popen(cmd, shell=True)
            print("🪟 Lancement activation Windows...")
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    def _activate_office(self):
        """Activer Office"""
        import subprocess
        try:
            cmd = 'powershell -Command "Start-Process powershell -Verb RunAs -ArgumentList \'-Command\', \'irm https://get.activated.win | iex\'"'
            subprocess.Popen(cmd, shell=True)
            print("📄 Lancement activation Office...")
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    def _activate_both(self):
        """Activer Windows et Office"""
        import subprocess
        try:
            cmd = 'powershell -Command "Start-Process powershell -Verb RunAs -ArgumentList \'-Command\', \'irm https://get.activated.win | iex\'"'
            subprocess.Popen(cmd, shell=True)
            print("🔑 Lancement activation Windows + Office...")
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    def _install_ordiplus_pack(self, apps):
        """Installer pack OrdiPlus"""
        print(f"⭐ Installation Pack OrdiPlus:")
        for app in apps:
            print(f"  • {app}")
    
    def _create_pack_card(self, parent, pack_name, pack_data):
        """Créer carte de pack avec bouton édition"""
        card = ModernCard(parent)
        card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Header
        header = ctk.CTkFrame(
            card,
            fg_color=pack_data['color'],
            corner_radius=DesignTokens.RADIUS_MD
        )
        header.pack(fill=tk.X, padx=15, pady=15)
        
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill=tk.X, padx=15, pady=12)
        
        # Titre et bouton édition
        title_row = ctk.CTkFrame(header_content, fg_color="transparent")
        title_row.pack(fill=tk.X)
        
        title = ctk.CTkLabel(
            title_row,
            text=pack_name,
            font=(DesignTokens.FONT_FAMILY, 18, "bold"),
            text_color="#FFFFFF"
        )
        title.pack(side=tk.LEFT)
        
        # Bouton éditer
        edit_btn = ctk.CTkButton(
            title_row,
            text="✏️",
            width=30,
            height=30,
            corner_radius=6,
            fg_color="rgba(255,255,255,0.2)",
            hover_color="rgba(255,255,255,0.3)",
            command=lambda: self._edit_pack(pack_name, pack_data),
            font=(DesignTokens.FONT_FAMILY, 14)
        )
        edit_btn.pack(side=tk.RIGHT)
        
        desc = ctk.CTkLabel(
            header_content,
            text=pack_data['description'],
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM),
            text_color="#FFFFFF",
            wraplength=250
        )
        desc.pack(anchor="w", pady=(5, 0))
        
        # Apps list
        apps_frame = ctk.CTkFrame(card, fg_color=DesignTokens.BG_ELEVATED, corner_radius=8)
        apps_frame.pack(fill=tk.X, padx=15, pady=10)
        
        count_label = ctk.CTkLabel(
            apps_frame,
            text=f"📦 {len(pack_data['apps'])} applications incluses",
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM, "bold"),
            text_color=DesignTokens.TEXT_SECONDARY
        )
        count_label.pack(anchor="w", padx=10, pady=10)
        
        # Liste apps (max 5 affichées)
        for app in pack_data['apps'][:5]:
            app_label = ctk.CTkLabel(
                apps_frame,
                text=f"  • {app}",
                font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM),
                text_color=DesignTokens.TEXT_TERTIARY,
                anchor="w"
            )
            app_label.pack(anchor="w", padx=10, pady=1)
        
        if len(pack_data['apps']) > 5:
            more = ctk.CTkLabel(
                apps_frame,
                text=f"  ... et {len(pack_data['apps']) - 5} autres",
                font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM),
                text_color=DesignTokens.TEXT_TERTIARY,
                anchor="w"
            )
            more.pack(anchor="w", pady=1)
        
        # Checkbox et bouton
        actions = ctk.CTkFrame(card, fg_color="transparent")
        actions.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        var = tk.BooleanVar()
        checkbox = ctk.CTkCheckBox(
            actions,
            text="Sélectionner ce pack",
            variable=var,
            command=lambda: self._toggle_pack(pack_name, var.get()),
            fg_color=DesignTokens.ACCENT_PRIMARY,
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM)
        )
        checkbox.pack(side=tk.LEFT)
        
        ModernButton(
            actions,
            text="🚀 Installer",
            variant="outlined",
            size="sm",
            command=lambda: self._install_pack(pack_name, pack_data)
        ).pack(side=tk.RIGHT)
    
    def _edit_pack(self, pack_name, pack_data):
        """Ouvrir fenêtre d'édition de pack"""
        # Créer fenêtre modale
        edit_window = ctk.CTkToplevel(self)
        edit_window.title(f"Éditer - {pack_name}")
        edit_window.geometry("800x600")
        edit_window.resizable(True, True)
        
        # Centrer fenêtre
        edit_window.update_idletasks()
        x = (edit_window.winfo_screenwidth() // 2) - (800 // 2)
        y = (edit_window.winfo_screenheight() // 2) - (600 // 2)
        edit_window.geometry(f"800x600+{x}+{y}")
        
        # Header
        header = ctk.CTkFrame(edit_window, fg_color=pack_data['color'])
        header.pack(fill=tk.X, padx=20, pady=20)
        
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill=tk.X, padx=20, pady=15)
        
        title = ctk.CTkLabel(
            header_content,
            text=f"✏️ Éditer {pack_name}",
            font=(DesignTokens.FONT_FAMILY, 20, "bold"),
            text_color="#FFFFFF"
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            header_content,
            text="Ajoutez ou retirez des applications du pack",
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_MD),
            text_color="#FFFFFF"
        )
        subtitle.pack(anchor="w", pady=(5, 0))
        
        # Zone de contenu
        content = ctk.CTkFrame(edit_window, fg_color="transparent")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Colonne gauche: Apps actuelles du pack
        left_panel = ctk.CTkFrame(content, fg_color=DesignTokens.BG_ELEVATED, corner_radius=DesignTokens.RADIUS_MD)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        left_title = ctk.CTkLabel(
            left_panel,
            text=f"📦 Applications dans le pack ({len(pack_data['apps'])})",
            font=(DesignTokens.FONT_FAMILY, 16, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY
        )
        left_title.pack(padx=15, pady=15)
        
        # Liste scrollable des apps dans le pack
        left_scroll = ctk.CTkScrollableFrame(left_panel, fg_color="transparent")
        left_scroll.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Variable pour stocker les apps sélectionnées
        pack_apps = pack_data['apps'].copy()
        
        def refresh_lists():
            """Rafraîchir les deux listes"""
            # Clear left list
            for widget in left_scroll.winfo_children():
                widget.destroy()
            
            # Recreate left list
            for app in pack_apps:
                app_frame = ctk.CTkFrame(left_scroll, fg_color=DesignTokens.BG_SECONDARY, corner_radius=6)
                app_frame.pack(fill=tk.X, pady=2, padx=5)
                
                app_label = ctk.CTkLabel(
                    app_frame,
                    text=app,
                    font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM),
                    text_color=DesignTokens.TEXT_PRIMARY,
                    anchor="w"
                )
                app_label.pack(side=tk.LEFT, padx=10, pady=8, fill=tk.X, expand=True)
                
                remove_btn = ctk.CTkButton(
                    app_frame,
                    text="➖",
                    width=30,
                    height=30,
                    corner_radius=6,
                    fg_color=DesignTokens.ERROR,
                    hover_color="#D32F2F",
                    command=lambda a=app: remove_app(a),
                    font=(DesignTokens.FONT_FAMILY, 16)
                )
                remove_btn.pack(side=tk.RIGHT, padx=5)
            
            # Update count
            left_title.configure(text=f"📦 Applications dans le pack ({len(pack_apps)})")
        
        def remove_app(app):
            """Retirer une app du pack"""
            if app in pack_apps:
                pack_apps.remove(app)
                refresh_lists()
        
        def add_app(app):
            """Ajouter une app au pack"""
            if app not in pack_apps:
                pack_apps.append(app)
                refresh_lists()
        
        # Colonne droite: Toutes les apps disponibles
        right_panel = ctk.CTkFrame(content, fg_color=DesignTokens.BG_ELEVATED, corner_radius=DesignTokens.RADIUS_MD)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        right_title = ctk.CTkLabel(
            right_panel,
            text="📚 Applications disponibles",
            font=(DesignTokens.FONT_FAMILY, 16, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY
        )
        right_title.pack(padx=15, pady=15)
        
        # Barre de recherche
        search_var = tk.StringVar()
        search_var.trace('w', lambda *args: filter_available_apps())
        
        search_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        search_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Rechercher une application...",
            textvariable=search_var,
            height=35,
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM)
        )
        search_entry.pack(fill=tk.X)
        
        # Liste scrollable des apps disponibles
        right_scroll = ctk.CTkScrollableFrame(right_panel, fg_color="transparent")
        right_scroll.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Collecter toutes les apps disponibles depuis programs_data
        all_available_apps = set()
        for category, apps in self.programs_data.items():
            all_available_apps.update(apps.keys())
        
        all_available_apps = sorted(all_available_apps)
        
        def filter_available_apps():
            """Filtrer apps disponibles selon recherche"""
            # Clear
            for widget in right_scroll.winfo_children():
                widget.destroy()
            
            search_term = search_var.get().lower()
            
            for app in all_available_apps:
                if search_term and search_term not in app.lower():
                    continue
                
                # Ne pas afficher si déjà dans le pack
                if app in pack_apps:
                    continue
                
                app_frame = ctk.CTkFrame(right_scroll, fg_color=DesignTokens.BG_SECONDARY, corner_radius=6)
                app_frame.pack(fill=tk.X, pady=2, padx=5)
                
                app_label = ctk.CTkLabel(
                    app_frame,
                    text=app,
                    font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM),
                    text_color=DesignTokens.TEXT_PRIMARY,
                    anchor="w"
                )
                app_label.pack(side=tk.LEFT, padx=10, pady=8, fill=tk.X, expand=True)
                
                add_btn = ctk.CTkButton(
                    app_frame,
                    text="➕",
                    width=30,
                    height=30,
                    corner_radius=6,
                    fg_color=DesignTokens.SUCCESS,
                    hover_color="#388E3C",
                    command=lambda a=app: add_app(a),
                    font=(DesignTokens.FONT_FAMILY, 16)
                )
                add_btn.pack(side=tk.RIGHT, padx=5)
        
        # Boutons actions en bas
        actions = ctk.CTkFrame(edit_window, fg_color="transparent")
        actions.pack(fill=tk.X, padx=20, pady=(10, 20))
        
        ModernButton(
            actions,
            text="❌ Annuler",
            variant="text",
            command=edit_window.destroy
        ).pack(side=tk.LEFT)
        
        def save_changes():
            """Sauvegarder les modifications"""
            self.packs[pack_name]['apps'] = pack_apps.copy()
            self._save_custom_packs()
            
            # Recréer l'interface
            for widget in self.winfo_children():
                widget.destroy()
            self._create_header()
            self._create_content()
            
            edit_window.destroy()
            print(f"✅ Pack {pack_name} modifié avec succès!")
        
        ModernButton(
            actions,
            text="💾 Sauvegarder",
            variant="filled",
            command=save_changes
        ).pack(side=tk.RIGHT)
        
        # Initialiser les listes
        refresh_lists()
        filter_available_apps()
    
    def _toggle_pack(self, pack_name, selected):
        """Toggle sélection pack"""
        if selected:
            self.selected_packs.add(pack_name)
        else:
            self.selected_packs.discard(pack_name)
    
    def _install_pack(self, pack_name, pack_data):
        """Installer un pack"""
        print(f"🚀 Installation du pack: {pack_name}")
        print(f"   Applications: {', '.join(pack_data['apps'])}")
    
    def _install_selected_packs(self):
        """Installer les packs sélectionnés"""
        if not self.selected_packs:
            return
        
        print(f"🚀 Installation de {len(self.selected_packs)} packs:")
        for pack in self.selected_packs:
            print(f"  • {pack}")