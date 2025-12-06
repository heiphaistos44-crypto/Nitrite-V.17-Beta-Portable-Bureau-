#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Page Master Install Simple - NiTriTe V17
Sans édition, juste affichage et installation
"""

import customtkinter as ctk
import tkinter as tk
from typing import Dict
from v14_mvp.design_system import DesignTokens
from v14_mvp.components import ModernCard, ModernButton


class MasterInstallPage(ctk.CTkFrame):
    """Page Master Install simple"""
    
    def __init__(self, parent, programs_data: Dict):
        super().__init__(parent, fg_color=DesignTokens.BG_PRIMARY)
        
        self.programs_data = programs_data
        self.selected_packs = set()
        
        self._create_header()
        self._create_content()
    
    def _create_header(self):
        """Header"""
        header = ModernCard(self)
        header.pack(fill=tk.X, padx=20, pady=10)
        
        container = ctk.CTkFrame(header, fg_color="transparent")
        container.pack(fill=tk.X, padx=20, pady=15)
        
        title = ctk.CTkLabel(
            container,
            text="🚀 Master Install",
            font=(DesignTokens.FONT_FAMILY, 24, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY
        )
        title.pack(side=tk.LEFT)
        
        subtitle = ctk.CTkLabel(
            container,
            text="Installation rapide de packs d'applications",
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_MD),
            text_color=DesignTokens.TEXT_SECONDARY
        )
        subtitle.pack(side=tk.LEFT, padx=20)
        
        ModernButton(
            container,
            text="🚀 Installer Sélection",
            variant="filled",
            command=self._install_selected_packs
        ).pack(side=tk.RIGHT)
    
    def _create_content(self):
        """Contenu"""
        scroll = ctk.CTkScrollableFrame(self, fg_color=DesignTokens.BG_PRIMARY)
        scroll.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Packs prédéfinis
        packs = {
            "🏢 OrdiPlus": {
                "description": "Pack complet OrdiPlus - Maintenance professionnelle",
                "apps": [
                    "Adobe Acrobat Reader DC",
                    "Microsoft Office 2007",
                    "Mozilla Firefox",
                    "VLC Media Player"
                ],
                "cleaning_tools": [
                    "Malwarebytes",
                    "Spybot Search & Destroy",
                    "RustDesk",
                    "Wise Disk Cleaner"
                ],
                "color": "#1E88E5",
                "create_folders": True
            },
            "🎮 Gaming": {
                "description": "Pack complet pour les gamers",
                "apps": ["Steam", "Discord", "OBS Studio", "Epic Games", "Battle.net", "GeForce Experience"],
                "color": DesignTokens.SUCCESS
            },
            "💼 Bureau": {
                "description": "Outils essentiels pour le travail",
                "apps": ["Microsoft Office", "Adobe Reader", "7-Zip", "TeamViewer", "Zoom", "Slack"],
                "color": DesignTokens.INFO
            },
            "💻 Développeur": {
                "description": "Environnement de développement",
                "apps": ["Visual Studio Code", "Git", "Python", "Docker", "Node.js", "Postman"],
                "color": DesignTokens.ACCENT_PRIMARY
            },
            "🌐 Navigateurs": {
                "description": "Navigateurs web populaires",
                "apps": ["Google Chrome", "Mozilla Firefox", "Brave", "Microsoft Edge", "Opera"],
                "color": "#FF6F00"
            },
        }
        
        # Afficher packs en grille
        row_frame = None
        for idx, (pack_name, pack_data) in enumerate(packs.items()):
            if idx % 2 == 0:
                row_frame = ctk.CTkFrame(scroll, fg_color="transparent")
                row_frame.pack(fill=tk.X, pady=5)
            
            self._create_pack_card(row_frame, pack_name, pack_data)
    
    def _create_pack_card(self, parent, pack_name, pack_data):
        """Créer carte de pack"""
        card = ModernCard(parent)
        card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Header coloré
        header = ctk.CTkFrame(
            card,
            fg_color=pack_data['color'],
            corner_radius=DesignTokens.RADIUS_MD
        )
        header.pack(fill=tk.X, padx=15, pady=15)
        
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill=tk.X, padx=15, pady=12)
        
        title = ctk.CTkLabel(
            header_content,
            text=pack_name,
            font=(DesignTokens.FONT_FAMILY, 18, "bold"),
            text_color="#FFFFFF"
        )
        title.pack(anchor="w")
        
        desc = ctk.CTkLabel(
            header_content,
            text=pack_data['description'],
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM),
            text_color="#FFFFFF"
        )
        desc.pack(anchor="w", pady=(5, 0))
        
        # Liste apps avec fond visible
        apps_frame = ctk.CTkFrame(
            card,
            fg_color=DesignTokens.BG_ELEVATED,
            corner_radius=8
        )
        apps_frame.pack(fill=tk.X, padx=15, pady=10)
        
        count_label = ctk.CTkLabel(
            apps_frame,
            text=f"📦 {len(pack_data['apps'])} applications",
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY
        )
        count_label.pack(anchor="w", padx=15, pady=10)
        
        # Afficher apps principales
        for app in pack_data['apps']:
            app_label = ctk.CTkLabel(
                apps_frame,
                text=f"  • {app}",
                font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM),
                text_color=DesignTokens.TEXT_SECONDARY,
                anchor="w"
            )
            app_label.pack(anchor="w", padx=15, pady=2)
        
        # Si pack avec outils de nettoyage, afficher section spéciale
        if 'cleaning_tools' in pack_data:
            separator = ctk.CTkFrame(apps_frame, fg_color=DesignTokens.TEXT_TERTIARY, height=1)
            separator.pack(fill=tk.X, padx=15, pady=10)
            
            folder_label = ctk.CTkLabel(
                apps_frame,
                text="📁 Outils de nettoyage (dossier séparé)",
                font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM, "bold"),
                text_color=DesignTokens.ACCENT_PRIMARY,
                anchor="w"
            )
            folder_label.pack(anchor="w", padx=15, pady=5)
            
            for tool in pack_data['cleaning_tools']:
                tool_label = ctk.CTkLabel(
                    apps_frame,
                    text=f"  🧹 {tool}",
                    font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM),
                    text_color=DesignTokens.TEXT_SECONDARY,
                    anchor="w"
                )
                tool_label.pack(anchor="w", padx=15, pady=2)
        
        # Actions
        actions = ctk.CTkFrame(card, fg_color="transparent")
        actions.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        var = tk.BooleanVar()
        checkbox = ctk.CTkCheckBox(
            actions,
            text="Sélectionner",
            variable=var,
            command=lambda: self._toggle_pack(pack_name, var.get()),
            fg_color=DesignTokens.ACCENT_PRIMARY
        )
        checkbox.pack(side=tk.LEFT)
        
        ModernButton(
            actions,
            text="🚀 Installer",
            variant="outlined",
            size="sm",
            command=lambda: self._install_pack(pack_name, pack_data)
        ).pack(side=tk.RIGHT)
    
    def _toggle_pack(self, pack_name, selected):
        """Toggle sélection"""
        if selected:
            self.selected_packs.add(pack_name)
        else:
            self.selected_packs.discard(pack_name)
    
    def _install_pack(self, pack_name, pack_data):
        """Installer un pack avec organisation en dossiers"""
        print(f"🚀 Installation du pack: {pack_name}")
        print(f"📍 Organisation:")
        
        # Apps principales
        print(f"\n📦 Applications principales:")
        for app in pack_data['apps']:
            print(f"  • Installation de {app}")
            self._install_app_winget(app)
        
        # Outils de nettoyage dans dossier séparé
        if 'cleaning_tools' in pack_data:
            print(f"\n📁 Création du dossier 'Outils de nettoyage'")
            import os
            cleaning_folder = os.path.join(os.environ.get('PROGRAMFILES', 'C:\\Program Files'), 'Outils de nettoyage')
            
            try:
                os.makedirs(cleaning_folder, exist_ok=True)
                print(f"   ✅ Dossier créé: {cleaning_folder}")
            except:
                print(f"   ⚠️ Création du dossier nécessite droits admin")
            
            print(f"\n🧹 Outils de nettoyage:")
            for tool in pack_data['cleaning_tools']:
                print(f"  • Installation de {tool} dans le dossier")
                self._install_app_winget(tool, target_folder=cleaning_folder)
        
        print(f"\n✅ Installation du pack {pack_name} terminée")
    
    def _install_app_winget(self, app_name, target_folder=None):
        """Installer une app via WinGet"""
        import subprocess
        
        # Mapping noms vers IDs WinGet
        winget_ids = {
            "Adobe Acrobat Reader DC": "Adobe.Acrobat.Reader.64-bit",
            "Microsoft Office 2007": "Microsoft.Office",
            "Mozilla Firefox": "Mozilla.Firefox",
            "VLC Media Player": "VideoLAN.VLC",
            "Malwarebytes": "Malwarebytes.Malwarebytes",
            "Spybot Search & Destroy": "Safer-Networking.SpybotAntiBeacon",
            "RustDesk": "RustDesk.RustDesk",
            "Wise Disk Cleaner": "WiseCleaner.WiseDiskCleaner"
        }
        
        winget_id = winget_ids.get(app_name, app_name)
        
        try:
            # Commande WinGet de base
            cmd = ['winget', 'install', '--id', winget_id, '--silent', '--accept-package-agreements', '--accept-source-agreements']
            
            # Si dossier cible spécifié
            if target_folder:
                cmd.extend(['--location', target_folder])
            
            print(f"   ⬇️ Commande: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"   ✅ {app_name} installé")
            else:
                print(f"   ⚠️ Erreur installation {app_name}: {result.stderr[:100]}")
        except subprocess.TimeoutExpired:
            print(f"   ⏱️ Timeout pour {app_name}")
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
    
    def _install_selected_packs(self):
        """Installer packs sélectionnés"""
        if not self.selected_packs:
            print("⚠️ Aucun pack sélectionné")
            return
        
        print(f"\n{'='*60}")
        print(f"🚀 INSTALLATION DE {len(self.selected_packs)} PACK(S)")
        print(f"{'='*60}\n")
        
        # Trouver les données des packs
        packs = {
            "🏢 OrdiPlus": {
                "description": "Pack complet OrdiPlus - Maintenance professionnelle",
                "apps": [
                    "Adobe Acrobat Reader DC",
                    "Microsoft Office 2007",
                    "Mozilla Firefox",
                    "VLC Media Player"
                ],
                "cleaning_tools": [
                    "Malwarebytes",
                    "Spybot Search & Destroy",
                    "RustDesk",
                    "Wise Disk Cleaner"
                ],
                "color": "#1E88E5",
                "create_folders": True
            },
            "🎮 Gaming": {
                "description": "Pack complet pour les gamers",
                "apps": ["Steam", "Discord", "OBS Studio", "Epic Games", "Battle.net", "GeForce Experience"],
                "color": DesignTokens.SUCCESS
            },
            "💼 Bureau": {
                "description": "Outils essentiels pour le travail",
                "apps": ["Microsoft Office", "Adobe Reader", "7-Zip", "TeamViewer", "Zoom", "Slack"],
                "color": DesignTokens.INFO
            },
            "💻 Développeur": {
                "description": "Environnement de développement",
                "apps": ["Visual Studio Code", "Git", "Python", "Docker", "Node.js", "Postman"],
                "color": DesignTokens.ACCENT_PRIMARY
            },
            "🌐 Navigateurs": {
                "description": "Navigateurs web populaires",
                "apps": ["Google Chrome", "Mozilla Firefox", "Brave", "Microsoft Edge", "Opera"],
                "color": "#FF6F00"
            },
        }
        
        for pack_name in self.selected_packs:
            if pack_name in packs:
                self._install_pack(pack_name, packs[pack_name])
                print()  # Ligne vide entre les packs
        
        print(f"{'='*60}")
        print(f"✅ INSTALLATION TERMINÉE")
        print(f"{'='*60}")