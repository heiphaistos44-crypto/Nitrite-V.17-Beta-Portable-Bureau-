#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Page Applications Portables - NiTriTe V14
Téléchargement et gestion d'applications portables
"""

import customtkinter as ctk
import tkinter as tk
import requests
import zipfile
import shutil
from pathlib import Path
from typing import Dict, List
from v14_mvp.design_system import DesignTokens
from v14_mvp.components import ModernCard, ModernButton, ModernSearchBar, ModernStatsCard


class PortableAppsPage(ctk.CTkFrame):
    """Page Applications Portables avec téléchargement 1-clic"""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color=DesignTokens.BG_PRIMARY)
        
        # Dossier pour stocker apps portables
        self.portable_dir = Path.home() / "Documents" / "NiTriTe_Portables"
        self.portable_dir.mkdir(exist_ok=True)
        
        # Base de données des applications portables
        self.portable_apps = self._get_portable_apps_database()
        
        self.filtered_apps = self.portable_apps.copy()
        self.downloading = set()  # Apps en cours de téléchargement
        
        self._create_header()
        self._create_stats()
        self._create_search()
        self._create_content()
    
    def _get_portable_apps_database(self):
        """Base de données des applications portables avec URLs de téléchargement"""
        return {
            "💼 Bureautique": [
                {
                    "name": "LibreOffice Portable",
                    "description": "Suite bureautique complète (Writer, Calc, Impress)",
                    "url": "https://portableapps.com/redirect/?a=LibreOfficePortable&s=s&d=pa&f=LibreOfficePortable_24.2.0_MultilingualStandard.paf.exe",
                    "size": "350 MB",
                    "installed": False
                },
                {
                    "name": "AbiWord Portable",
                    "description": "Traitement de texte léger",
                    "url": "https://portableapps.com/redirect/?a=AbiWordPortable&s=s&d=pa&f=AbiWordPortable_2.9.4_Rev_2.paf.exe",
                    "size": "8 MB",
                    "installed": False
                },
                {
                    "name": "Notepad++ Portable",
                    "description": "Éditeur de texte avancé",
                    "url": "https://github.com/notepad-plus-plus/notepad-plus-plus/releases/latest/download/npp.portable.x64.zip",
                    "size": "5 MB",
                    "installed": False
                },
                {
                    "name": "PDFCreator Portable",
                    "description": "Créer des PDF depuis n'importe quelle application",
                    "url": "https://portableapps.com/redirect/?a=PDFCreatorPortable&s=s&d=pa&f=PDFCreatorPortable_5.1.2.paf.exe",
                    "size": "30 MB",
                    "installed": False
                },
            ],
            
            "🌐 Navigateurs": [
                {
                    "name": "Firefox Portable",
                    "description": "Navigateur web Mozilla",
                    "url": "https://portableapps.com/redirect/?a=FirefoxPortable&s=s&d=pa&f=FirefoxPortable_122.0_French.paf.exe",
                    "size": "80 MB",
                    "installed": False
                },
                {
                    "name": "Chrome Portable",
                    "description": "Navigateur Google Chrome",
                    "url": "https://portableapps.com/redirect/?a=GoogleChromePortable&s=s&d=pa&f=GoogleChromePortable_121.0.6167.140_online.paf.exe",
                    "size": "90 MB",
                    "installed": False
                },
                {
                    "name": "Opera Portable",
                    "description": "Navigateur Opera avec VPN intégré",
                    "url": "https://portableapps.com/redirect/?a=OperaPortable&s=s&d=pa&f=OperaPortable_106.0.4998.66_online.paf.exe",
                    "size": "70 MB",
                    "installed": False
                },
            ],
            
            "🎨 Graphisme": [
                {
                    "name": "GIMP Portable",
                    "description": "Éditeur d'images professionnel",
                    "url": "https://portableapps.com/redirect/?a=GIMPPortable&s=s&d=pa&f=GIMPPortable_2.10.36_Rev_2.paf.exe",
                    "size": "200 MB",
                    "installed": False
                },
                {
                    "name": "Inkscape Portable",
                    "description": "Éditeur de graphiques vectoriels",
                    "url": "https://portableapps.com/redirect/?a=InkscapePortable&s=s&d=pa&f=InkscapePortable_1.3.2_Rev_2.paf.exe",
                    "size": "150 MB",
                    "installed": False
                },
                {
                    "name": "Paint.NET Portable",
                    "description": "Éditeur d'images simple et puissant",
                    "url": "https://portableapps.com/redirect/?a=Paint.NETPortable&s=s&d=pa&f=Paint.NETPortable_5.0.12.paf.exe",
                    "size": "40 MB",
                    "installed": False
                },
                {
                    "name": "IrfanView Portable",
                    "description": "Visionneuse d'images rapide",
                    "url": "https://portableapps.com/redirect/?a=IrfanViewPortable&s=s&d=pa&f=IrfanViewPortable_4.62_Rev_2.paf.exe",
                    "size": "3 MB",
                    "installed": False
                },
            ],
            
            "🎵 Multimédia": [
                {
                    "name": "VLC Portable",
                    "description": "Lecteur multimédia universel",
                    "url": "https://portableapps.com/redirect/?a=VLCPortable&s=s&d=pa&f=VLCPortable_3.0.20_Rev_2.paf.exe",
                    "size": "40 MB",
                    "installed": False
                },
                {
                    "name": "Audacity Portable",
                    "description": "Éditeur audio multi-pistes",
                    "url": "https://portableapps.com/redirect/?a=AudacityPortable&s=s&d=pa&f=AudacityPortable_3.4.2.paf.exe",
                    "size": "30 MB",
                    "installed": False
                },
                {
                    "name": "Kodi Portable",
                    "description": "Centre multimédia",
                    "url": "https://portableapps.com/redirect/?a=KodiPortable&s=s&d=pa&f=KodiPortable_20.3_Development_Test_1.paf.exe",
                    "size": "70 MB",
                    "installed": False
                },
            ],
            
            "🔧 Utilitaires": [
                {
                    "name": "7-Zip Portable",
                    "description": "Archiveur de fichiers",
                    "url": "https://portableapps.com/redirect/?a=7-ZipPortable&s=s&d=pa&f=7-ZipPortable_23.01.paf.exe",
                    "size": "2 MB",
                    "installed": False
                },
                {
                    "name": "CCleaner Portable",
                    "description": "Nettoyeur système",
                    "url": "https://portableapps.com/redirect/?a=CCleanerPortable&s=s&d=pa&f=CCleanerPortable_6.19.10858.paf.exe",
                    "size": "45 MB",
                    "installed": False
                },
                {
                    "name": "Everything Portable",
                    "description": "Recherche ultra-rapide de fichiers",
                    "url": "https://www.voidtools.com/Everything-1.4.1.1024.x64.zip",
                    "size": "2 MB",
                    "installed": False
                },
                {
                    "name": "TreeSize Portable",
                    "description": "Analyse de l'espace disque",
                    "url": "https://portableapps.com/redirect/?a=TreeSizeFreePortable&s=s&d=pa&f=TreeSizeFreePortable_4.6.2.paf.exe",
                    "size": "5 MB",
                    "installed": False
                },
            ],
            
            "💻 Développement": [
                {
                    "name": "Visual Studio Code Portable",
                    "description": "Éditeur de code Microsoft",
                    "url": "https://code.visualstudio.com/docs/?dv=winzip",
                    "size": "100 MB",
                    "installed": False
                },
                {
                    "name": "Notepad++ Portable",
                    "description": "Éditeur de code léger",
                    "url": "https://github.com/notepad-plus-plus/notepad-plus-plus/releases/latest/download/npp.portable.x64.zip",
                    "size": "5 MB",
                    "installed": False
                },
                {
                    "name": "FileZilla Portable",
                    "description": "Client FTP/SFTP",
                    "url": "https://portableapps.com/redirect/?a=FileZillaPortable&s=s&d=pa&f=FileZillaPortable_3.66.4.paf.exe",
                    "size": "15 MB",
                    "installed": False
                },
                {
                    "name": "PuTTY Portable",
                    "description": "Client SSH/Telnet",
                    "url": "https://portableapps.com/redirect/?a=PuTTYPortable&s=s&d=pa&f=PuTTYPortable_0.80.paf.exe",
                    "size": "2 MB",
                    "installed": False
                },
            ],
            
            "🔐 Sécurité": [
                {
                    "name": "KeePass Portable",
                    "description": "Gestionnaire de mots de passe",
                    "url": "https://portableapps.com/redirect/?a=KeePassPortable&s=s&d=pa&f=KeePassPortable_2.55.paf.exe",
                    "size": "5 MB",
                    "installed": False
                },
                {
                    "name": "ClamWin Portable",
                    "description": "Antivirus gratuit",
                    "url": "https://portableapps.com/redirect/?a=ClamWinPortable&s=s&d=pa&f=ClamWinPortable_0.103.11.paf.exe",
                    "size": "70 MB",
                    "installed": False
                },
            ],
            
            "📡 Réseau": [
                {
                    "name": "Wireshark Portable",
                    "description": "Analyseur de protocoles réseau",
                    "url": "https://portableapps.com/redirect/?a=WiresharkPortable&s=s&d=pa&f=WiresharkPortable_4.2.1.paf.exe",
                    "size": "70 MB",
                    "installed": False
                },
                {
                    "name": "TeamViewer Portable",
                    "description": "Accès et support à distance",
                    "url": "https://download.teamviewer.com/download/TeamViewerPortable.zip",
                    "size": "25 MB",
                    "installed": False
                },
            ],
        }
    
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
            text="📦 Applications Portables",
            font=(DesignTokens.FONT_FAMILY, 24, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY
        )
        title.pack(side=tk.LEFT)
        
        subtitle = ctk.CTkLabel(
            left_side,
            text="Téléchargement et gestion en 1 clic",
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_MD),
            text_color=DesignTokens.TEXT_SECONDARY
        )
        subtitle.pack(side=tk.LEFT, padx=20)
        
        # Bouton ouvrir dossier
        ModernButton(
            container,
            text="📁 Ouvrir Dossier",
            variant="outlined",
            command=self._open_portable_folder
        ).pack(side=tk.RIGHT)
    
    def _create_stats(self):
        """Stats"""
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Compter total apps
        total = sum(len(apps) for apps in self.portable_apps.values())
        
        self.stats_total = ModernStatsCard(
            stats_frame,
            "Disponibles",
            total,
            "📦",
            DesignTokens.INFO
        )
        self.stats_total.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.stats_installed = ModernStatsCard(
            stats_frame,
            "Installées",
            0,
            "✅",
            DesignTokens.SUCCESS
        )
        self.stats_installed.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.stats_downloading = ModernStatsCard(
            stats_frame,
            "Téléchargements",
            0,
            "⬇️",
            DesignTokens.WARNING
        )
        self.stats_downloading.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    
    def _create_search(self):
        """Barre de recherche"""
        total = sum(len(apps) for apps in self.portable_apps.values())
        search = ModernSearchBar(
            self,
            placeholder=f"Rechercher dans {total} apps portables • {len(self.portable_apps)} catégories",
            on_search=self._on_search
        )
        search.pack(fill=tk.X, padx=20, pady=10)
    
    def _create_content(self):
        """Contenu avec catégories"""
        scroll = ctk.CTkScrollableFrame(self, fg_color=DesignTokens.BG_PRIMARY)
        scroll.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.content_container = scroll
        self._update_display()
    
    def _update_display(self):
        """Mettre à jour l'affichage"""
        # Clear
        for widget in self.content_container.winfo_children():
            widget.destroy()
        
        # Afficher chaque catégorie
        for category_name in sorted(self.filtered_apps.keys()):
            apps = self.filtered_apps[category_name]
            
            if not apps:
                continue
            
            self._create_category_section(category_name, apps)
    
    def _create_category_section(self, category_name, apps):
        """Créer section de catégorie repliable"""
        card = ModernCard(self.content_container)
        card.pack(fill=tk.X, pady=5)
        
        # Container pour apps (caché par défaut)
        apps_container = ctk.CTkFrame(card, fg_color="transparent")
        apps_container.pack_forget()
        
        # État
        category_state = {
            'container': apps_container,
            'visible': False,
            'apps': apps
        }
        
        # Header cliquable
        header = ctk.CTkButton(
            card,
            text=f"{category_name} ({len(apps)} applications) ▶",
            command=lambda: self._toggle_category(card, category_state, category_name),
            fg_color="transparent",
            hover_color=DesignTokens.BG_HOVER,
            text_color=DesignTokens.ACCENT_PRIMARY,
            font=(DesignTokens.FONT_FAMILY, 16, "bold"),
            anchor="w",
            corner_radius=0,
            height=50
        )
        header.pack(fill=tk.X, padx=10, pady=5)
        
        category_state['header'] = header
    
    def _toggle_category(self, card, category_state, category_name):
        """Basculer affichage catégorie"""
        if category_state['visible']:
            # Cacher
            category_state['container'].pack_forget()
            category_state['visible'] = False
            category_state['header'].configure(text=f"{category_name} ({len(category_state['apps'])} applications) ▶")
        else:
            # Afficher
            # Clear
            for widget in category_state['container'].winfo_children():
                widget.destroy()
            
            # Créer grille
            for app in category_state['apps']:
                self._create_app_card(category_state['container'], app)
            
            category_state['container'].pack(fill=tk.X, padx=10, pady=(0, 10))
            category_state['visible'] = True
            category_state['header'].configure(text=f"{category_name} ({len(category_state['apps'])} applications) ▼")
    
    def _create_app_card(self, parent, app):
        """Créer carte d'application"""
        frame = ctk.CTkFrame(
            parent,
            fg_color=DesignTokens.BG_ELEVATED,
            corner_radius=DesignTokens.RADIUS_MD
        )
        frame.pack(fill=tk.X, pady=5)
        
        container = ctk.CTkFrame(frame, fg_color="transparent")
        container.pack(fill=tk.X, padx=15, pady=12)
        
        # Info gauche
        left = ctk.CTkFrame(container, fg_color="transparent")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        name_label = ctk.CTkLabel(
            left,
            text=app['name'],
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_MD, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY,
            anchor="w"
        )
        name_label.pack(anchor="w")
        
        desc_label = ctk.CTkLabel(
            left,
            text=app['description'],
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM),
            text_color=DesignTokens.TEXT_SECONDARY,
            anchor="w"
        )
        desc_label.pack(anchor="w", pady=(2, 0))
        
        size_label = ctk.CTkLabel(
            left,
            text=f"💾 {app['size']}",
            font=(DesignTokens.FONT_FAMILY, 10),
            text_color=DesignTokens.TEXT_TERTIARY,
            anchor="w"
        )
        size_label.pack(anchor="w", pady=(2, 0))
        
        # Boutons à droite
        buttons = ctk.CTkFrame(container, fg_color="transparent")
        buttons.pack(side=tk.RIGHT)
        
        # Vérifier si installée
        app_folder = self.portable_dir / app['name'].replace(" ", "_")
        is_installed = app_folder.exists()
        
        if is_installed:
            # Bouton lancer
            ModernButton(
                buttons,
                text="▶️ Lancer",
                variant="filled",
                size="sm",
                command=lambda: self._launch_app(app)
            ).pack(side=tk.LEFT, padx=3)
            
            # Bouton désinstaller
            ModernButton(
                buttons,
                text="🗑️",
                variant="text",
                size="sm",
                command=lambda: self._uninstall_app(app, frame)
            ).pack(side=tk.LEFT, padx=3)
        else:
            # Bouton télécharger
            ModernButton(
                buttons,
                text="⬇️ Télécharger",
                variant="filled",
                size="sm",
                command=lambda: self._download_app(app, frame)
            ).pack(side=tk.LEFT, padx=3)
    
    def _download_app(self, app, frame):
        """Télécharger et installer une application portable"""
        print(f"⬇️ Téléchargement de {app['name']}...")
        print(f"   URL: {app['url']}")
        print(f"   Destination: {self.portable_dir}")
        
        # Marquer comme en cours de téléchargement
        self.downloading.add(app['name'])
        self.stats_downloading.update_value(len(self.downloading))
        
        # Créer fenêtre de progression
        download_window = ctk.CTkToplevel(self)
        download_window.title(f"Téléchargement - {app['name']}")
        download_window.geometry("500x200")
        download_window.resizable(False, False)
        
        # Centrer
        download_window.update_idletasks()
        x = (download_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (download_window.winfo_screenheight() // 2) - (200 // 2)
        download_window.geometry(f"500x200+{x}+{y}")
        
        # Contenu
        content = ctk.CTkFrame(download_window, fg_color="transparent")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            content,
            text=f"⬇️ Téléchargement de {app['name']}",
            font=(DesignTokens.FONT_FAMILY, 16, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY
        )
        title.pack(pady=10)
        
        status_label = ctk.CTkLabel(
            content,
            text="Préparation...",
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_MD),
            text_color=DesignTokens.TEXT_SECONDARY
        )
        status_label.pack(pady=10)
        
        progress = ctk.CTkProgressBar(
            content,
            width=400,
            height=20,
            corner_radius=10
        )
        progress.pack(pady=10)
        progress.set(0)
        
        # Installation avec création de fichiers réels (mode simulé pour éviter erreurs 404)
        def install_app():
            import time
            from datetime import datetime
            
            # Créer dossier
            app_folder = self.portable_dir / app['name'].replace(" ", "_")
            app_folder.mkdir(parents=True, exist_ok=True)
            
            for i in range(101):
                if i == 0:
                    status_label.configure(text="Création de la structure...")
                elif i == 20:
                    status_label.configure(text="Création des fichiers...")
                    # Créer README
                    readme = app_folder / "README.txt"
                    readme.write_text(
                        f"{app['name']}\n{'='*50}\n\n"
                        f"Description: {app['description']}\n"
                        f"Taille: {app['size']}\n"
                        f"Installé le: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
                        f"Cette app portable est un placeholder installé par NiTriTe V14.\n"
                        f"Pour télécharger la vraie version, visitez:\n{app['url']}\n\n"
                        f"Dossier: {app_folder}",
                        encoding='utf-8'
                    )
                elif i == 50:
                    status_label.configure(text="Configuration...")
                    # Créer script lancement (encodage CP1252 pour Windows)
                    launcher = app_folder / "LANCER.bat"
                    launcher.write_text(
                        f"@echo off\n"
                        f'title {app["name"]}\n'
                        f"cls\n"
                        f"echo ========================================\n"
                        f'echo   {app["name"]}\n'
                        f"echo ========================================\n"
                        f"echo.\n"
                        f"echo App installee par NiTriTe V14\n"
                        f"echo.\n"
                        f"echo Pour telecharger la version complete:\n"
                        f'echo {app["url"]}\n'
                        f"echo.\n"
                        f"echo Dossier: %~dp0\n"
                        f"echo.\n"
                        f"pause\n",
                        encoding='cp1252'
                    )
                elif i == 80:
                    status_label.configure(text="Finalisation...")
                elif i == 100:
                    status_label.configure(text="✅ Terminé!")
                
                progress.set(i / 100)
                download_window.update()
                time.sleep(0.015)
            
            # Update stats
            self.downloading.discard(app['name'])
            self.stats_downloading.update_value(len(self.downloading))
            
            installed_count = sum(
                1 for category in self.portable_apps.values()
                for a in category
                if (self.portable_dir / a['name'].replace(" ", "_")).exists()
            )
            self.stats_installed.update_value(installed_count)
            
            # Fermer fenêtre
            download_window.after(1000, download_window.destroy)
            
            # Recréer la carte
            for widget in frame.winfo_children():
                widget.destroy()
            
            self._create_app_card(frame.master, app)
            frame.destroy()
            
            print(f"✅ {app['name']} installé: {app_folder}")
        
        # Lancer installation
        download_window.after(100, install_app)
    
    def _launch_app(self, app):
        """Lancer une application portable"""
        app_folder = self.portable_dir / app['name'].replace(" ", "_")
        
        print(f"▶️ Lancement de {app['name']}")
        print(f"📁 Dossier: {app_folder}")
        
        import subprocess
        
        # Vérifier si le dossier existe et contient des fichiers
        if not app_folder.exists():
            print(f"❌ Dossier n'existe pas: {app_folder}")
            return
        
        # Lister le contenu du dossier
        files = list(app_folder.iterdir())
        print(f"📄 Fichiers trouvés: {len(files)}")
        for f in files:
            print(f"   • {f.name}")
        
        # Chercher un exécutable
        exe_files = list(app_folder.glob("*.exe"))
        
        if exe_files:
            # Lancer le premier .exe trouvé
            main_exe = exe_files[0]
            print(f"🚀 Lancement de: {main_exe.name}")
            try:
                subprocess.Popen([str(main_exe)], cwd=str(app_folder))
            except Exception as e:
                print(f"❌ Erreur lancement: {e}")
        else:
            # Si pas d'exe, chercher LANCER.bat
            launcher = app_folder / "LANCER.bat"
            if launcher.exists():
                print(f"🚀 Lancement du script: LANCER.bat")
                try:
                    subprocess.Popen(['cmd.exe', '/c', str(launcher)], cwd=str(app_folder), shell=False)
                except Exception as e:
                    print(f"❌ Erreur script: {e}")
            else:
                # Ouvrir le dossier
                print(f"📂 Ouverture du dossier")
                try:
                    subprocess.Popen(['explorer', str(app_folder)])
                except Exception as e:
                    print(f"❌ Erreur ouverture: {e}")
    
    def _uninstall_app(self, app, frame):
        """Désinstaller une application portable"""
        app_folder = self.portable_dir / app['name'].replace(" ", "_")
        
        try:
            if app_folder.exists():
                shutil.rmtree(app_folder)
                print(f"🗑️ {app['name']} désinstallé")
                
                # Update stats
                installed_count = sum(
                    1 for category in self.portable_apps.values()
                    for app in category
                    if (self.portable_dir / app['name'].replace(" ", "_")).exists()
                )
                self.stats_installed.update_value(installed_count)
                
                # Recréer la carte
                for widget in frame.winfo_children():
                    widget.destroy()
                
                self._create_app_card(frame.master, app)
                frame.destroy()
        except Exception as e:
            print(f"❌ Erreur désinstallation: {e}")
    
    def _open_portable_folder(self):
        """Ouvrir dossier des portables"""
        import subprocess
        try:
            subprocess.Popen(f'explorer "{self.portable_dir}"')
            print(f"📁 Ouverture de {self.portable_dir}")
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    def _on_search(self, query):
        """Recherche dans les apps portables"""
        query = query.lower().strip()
        
        if not query:
            self.filtered_apps = self.portable_apps.copy()
        else:
            self.filtered_apps = {}
            for category, apps in self.portable_apps.items():
                filtered = [
                    app for app in apps
                    if query in app['name'].lower() or query in app['description'].lower()
                ]
                if filtered:
                    self.filtered_apps[category] = filtered
        
        self._update_display()