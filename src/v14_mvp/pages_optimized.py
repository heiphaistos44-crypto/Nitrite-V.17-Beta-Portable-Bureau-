#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pages Optimisées - NiTriTe V14
Versions optimisées avec chargement progressif
"""

import customtkinter as ctk
import tkinter as tk
from typing import Dict, List
from v14_mvp.design_system import DesignTokens
from v14_mvp.components import ModernCard, ModernSearchBar, ModernStatsCard, ModernButton
from v14_mvp.installer import installer


class OptimizedApplicationsPage(ctk.CTkFrame):
    """Page Applications optimisée avec catégories groupées"""
    
    def __init__(self, parent, programs_data: Dict):
        super().__init__(parent, fg_color=DesignTokens.BG_PRIMARY)
        
        self.programs_data = programs_data
        self.selected_apps = set()
        self.all_apps = []
        self.filtered_categories = {}
        
        # Préparer liste
        self._prepare_apps_list()
        
        # UI
        self._create_header()
        self._create_stats()
        self._create_search()
        self._create_content()
    
    def _prepare_apps_list(self):
        """Préparer liste d'applications groupées par catégorie (TOUTES les apps)"""
        # Préparer liste complète
        for category, apps in self.programs_data.items():
            for app_name, app_data in apps.items():
                app_info = {
                    'name': app_name,
                    'category': category,
                    'description': app_data.get('description', ''),
                    'essential': app_data.get('essential', False)
                }
                self.all_apps.append(app_info)
        
        # Grouper par catégorie pour affichage - SANS LIMITE
        self.filtered_categories = {}
        for category, apps in self.programs_data.items():
            apps_list = [
                {
                    'name': app_name,
                    'category': category,
                    'description': app_data.get('description', ''),
                    'essential': app_data.get('essential', False)
                }
                for app_name, app_data in apps.items()
            ]
            
            # AUCUNE LIMITE - Afficher toutes les apps
            self.filtered_categories[category] = apps_list
    
    def _create_header(self):
        """Header"""
        header = ModernCard(self)
        header.pack(fill=tk.X, padx=20, pady=10)
        
        container = ctk.CTkFrame(header, fg_color="transparent")
        container.pack(fill=tk.X, padx=20, pady=15)
        
        title = ctk.CTkLabel(
            container,
            text="📦 Applications",
            font=(DesignTokens.FONT_FAMILY, 24, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY
        )
        title.pack(side=tk.LEFT)
        
        actions = ctk.CTkFrame(container, fg_color="transparent")
        actions.pack(side=tk.RIGHT)
        
        ModernButton(
            actions,
            text="🚀 Installer Sélection",
            variant="filled",
            size="md",
            command=self._install_selected
        ).pack(side=tk.LEFT, padx=5)
    
    def _create_stats(self):
        """Stats"""
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.stats_total = ModernStatsCard(
            stats_frame,
            "Total",
            len(self.all_apps),
            "📦",
            DesignTokens.ACCENT_PRIMARY
        )
        self.stats_total.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Calculer nombre d'apps affichées
        total_displayed = sum(len(apps) for apps in self.filtered_categories.values())
        
        self.stats_displayed = ModernStatsCard(
            stats_frame,
            "Affichées",
            total_displayed,
            "👁️",
            DesignTokens.INFO
        )
        self.stats_displayed.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.stats_selected = ModernStatsCard(
            stats_frame,
            "Sélection",
            0,
            "✓",
            DesignTokens.SUCCESS
        )
        self.stats_selected.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    
    def _create_search(self):
        """Recherche"""
        search = ModernSearchBar(
            self,
            placeholder=f"Rechercher dans {len(self.all_apps)} apps • {len(self.filtered_categories)} catégories",
            on_search=self._on_search
        )
        search.pack(fill=tk.X, padx=20, pady=10)
    
    def _create_content(self):
        """Contenu avec catégories groupées"""
        # Liste scrollable
        scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=DesignTokens.BG_PRIMARY
        )
        scroll_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Container grille
        self.grid_container = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        self.grid_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Afficher toutes les catégories
        self._update_grid()
    
    def _update_grid(self):
        """Mettre à jour grille avec catégories repliables"""
        # Clear
        for widget in self.grid_container.winfo_children():
            widget.destroy()
        
        # Afficher chaque catégorie avec système repliable
        for category_name in sorted(self.filtered_categories.keys()):
            apps = self.filtered_categories[category_name]
            
            if not apps:
                continue
            
            self._create_category_section(category_name, apps)
    
    def _create_category_section(self, category_name, apps):
        """Créer une section de catégorie repliable"""
        # Card pour la catégorie
        card = ctk.CTkFrame(
            self.grid_container,
            fg_color=DesignTokens.BG_ELEVATED,
            corner_radius=DesignTokens.RADIUS_MD
        )
        card.pack(fill=tk.X, pady=5)
        
        # Container pour apps (caché par défaut)
        apps_container = ctk.CTkFrame(card, fg_color="transparent")
        apps_container.pack_forget()
        
        # État de la catégorie
        category_state = {
            'container': apps_container,
            'visible': False,
            'apps': apps
        }
        
        # Header cliquable
        header = ctk.CTkButton(
            card,
            text=f"📂 {category_name} ({len(apps)} applications) ▶",
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
        
        # Stocker header pour mise à jour texte
        category_state['header'] = header
    
    def _toggle_category(self, card, category_state, category_name):
        """Basculer affichage catégorie"""
        if category_state['visible']:
            # Cacher
            category_state['container'].pack_forget()
            category_state['visible'] = False
            category_state['header'].configure(text=f"📂 {category_name} ({len(category_state['apps'])} applications) ▶")
        else:
            # Afficher
            # Clear container
            for widget in category_state['container'].winfo_children():
                widget.destroy()
            
            # Créer grille 3 colonnes
            grid_frame = ctk.CTkFrame(category_state['container'], fg_color="transparent")
            grid_frame.pack(fill=tk.X, padx=10, pady=10)
            
            row, col = 0, 0
            max_cols = 3
            
            for app in category_state['apps']:
                self._create_app_card_in_grid(grid_frame, app, row, col)
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1
            
            # Configurer colonnes
            for i in range(max_cols):
                grid_frame.columnconfigure(i, weight=1)
            
            category_state['container'].pack(fill=tk.X, padx=5, pady=(0, 10))
            category_state['visible'] = True
            category_state['header'].configure(text=f"📂 {category_name} ({len(category_state['apps'])} applications) ▼")
    
    def _create_app_card_in_grid(self, parent, app, row, col):
        """Créer carte app dans grille"""
        frame = ctk.CTkFrame(
            parent,
            fg_color=DesignTokens.BG_SECONDARY,
            corner_radius=DesignTokens.RADIUS_MD,
            height=70
        )
        frame.grid(row=row, column=col, sticky="ew", padx=5, pady=5)
        
        # Container
        container = ctk.CTkFrame(frame, fg_color="transparent")
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)
        
        # Checkbox
        var = tk.BooleanVar()
        checkbox = ctk.CTkCheckBox(
            container,
            text="",
            variable=var,
            command=lambda: self._toggle_app(app['name'], var.get()),
            fg_color=DesignTokens.ACCENT_PRIMARY,
            corner_radius=4,
            width=20
        )
        checkbox.pack(side=tk.LEFT, padx=(0, 8))
        
        # Info (nom + catégorie)
        info_frame = ctk.CTkFrame(container, fg_color="transparent")
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Nom
        name_label = ctk.CTkLabel(
            info_frame,
            text=app['name'][:30] + ('...' if len(app['name']) > 30 else ''),
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY,
            anchor="w"
        )
        name_label.pack(anchor="w")
        
        # Catégorie
        cat_label = ctk.CTkLabel(
            info_frame,
            text=f"📁 {app['category']}",
            font=(DesignTokens.FONT_FAMILY, 10),
            text_color=DesignTokens.TEXT_TERTIARY,
            anchor="w"
        )
        cat_label.pack(anchor="w")
        
        # Bouton site web
        web_btn = ctk.CTkButton(
            container,
            text="🌐",
            width=28,
            height=28,
            corner_radius=6,
            fg_color=DesignTokens.INFO,
            hover_color=DesignTokens.BG_HOVER,
            command=lambda: self._open_website(app['name']),
            font=(DesignTokens.FONT_FAMILY, 14)
        )
        web_btn.pack(side=tk.RIGHT, padx=3)
        
        # Badge essentiel
        if app['essential']:
            badge = ctk.CTkLabel(
                container,
                text="⭐",
                font=(DesignTokens.FONT_FAMILY, 12),
                text_color=DesignTokens.WARNING
            )
            badge.pack(side=tk.RIGHT, padx=3)
    
    def _create_app_card(self, app, row, col):
        """Créer une carte d'application compacte"""
        frame = ctk.CTkFrame(
            self.grid_container,
            fg_color=DesignTokens.BG_ELEVATED,
            corner_radius=DesignTokens.RADIUS_MD,
            height=60
        )
        frame.grid(row=row, column=col, sticky="ew", padx=5, pady=5)
        
        # Container avec padding
        container = ctk.CTkFrame(frame, fg_color="transparent")
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)
        
        # Ligne du haut: Checkbox + Nom + Badge
        top_row = ctk.CTkFrame(container, fg_color="transparent")
        top_row.pack(fill=tk.X)
        
        # Checkbox
        var = tk.BooleanVar()
        checkbox = ctk.CTkCheckBox(
            top_row,
            text="",
            variable=var,
            command=lambda: self._toggle_app(app['name'], var.get()),
            fg_color=DesignTokens.ACCENT_PRIMARY,
            corner_radius=4,
            width=20
        )
        checkbox.pack(side=tk.LEFT, padx=(0, 8))
        
        # Nom (tronqué si trop long)
        name_label = ctk.CTkLabel(
            top_row,
            text=app['name'][:30] + ('...' if len(app['name']) > 30 else ''),
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY,
            anchor="w"
        )
        name_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Badge essentiel
        if app['essential']:
            badge = ctk.CTkLabel(
                top_row,
                text="⭐",
                font=(DesignTokens.FONT_FAMILY, 12),
                text_color=DesignTokens.WARNING
            )
            badge.pack(side=tk.RIGHT, padx=3)
        
        # Ligne du bas: Catégorie
        cat_label = ctk.CTkLabel(
            container,
            text=f"📁 {app['category']}",
            font=(DesignTokens.FONT_FAMILY, 10),
            text_color=DesignTokens.TEXT_TERTIARY,
            anchor="w"
        )
        cat_label.pack(fill=tk.X, pady=(3, 0))
    
    def _toggle_app(self, app_name, selected):
        """Toggle sélection"""
        if selected:
            self.selected_apps.add(app_name)
        else:
            self.selected_apps.discard(app_name)
        self.stats_selected.update_value(len(self.selected_apps))
    
    def _on_search(self, query):
        """Recherche avec filtrage par catégorie"""
        query = query.lower().strip()
        
        if not query:
            # Restaurer toutes les catégories
            self.filtered_categories = {}
            for category, apps in self.programs_data.items():
                self.filtered_categories[category] = [
                    {
                        'name': app_name,
                        'category': category,
                        'description': app_data.get('description', ''),
                        'essential': app_data.get('essential', False)
                    }
                    for app_name, app_data in apps.items()
                ]
        else:
            # Filtrer dans chaque catégorie
            self.filtered_categories = {}
            for category, apps in self.programs_data.items():
                filtered_apps = [
                    {
                        'name': app_name,
                        'category': category,
                        'description': app_data.get('description', ''),
                        'essential': app_data.get('essential', False)
                    }
                    for app_name, app_data in apps.items()
                    if query in app_name.lower() or query in app_data.get('description', '').lower()
                ]
                if filtered_apps:
                    self.filtered_categories[category] = filtered_apps
        
        # Calculer total
        total_displayed = sum(len(apps) for apps in self.filtered_categories.values())
        self.stats_displayed.update_value(total_displayed)
        self._update_grid()
    
    def _install_selected(self):
        """Installer les applications sélectionnées"""
        if not self.selected_apps:
            return
        
        # Créer fenêtre d'installation
        install_window = ctk.CTkToplevel(self)
        install_window.title("Installation en cours")
        install_window.geometry("600x400")
        install_window.resizable(False, False)
        
        # Centrer fenêtre
        install_window.update_idletasks()
        x = (install_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (install_window.winfo_screenheight() // 2) - (400 // 2)
        install_window.geometry(f"600x400+{x}+{y}")
        
        # Titre
        title = ctk.CTkLabel(
            install_window,
            text=f"📦 Installation de {len(self.selected_apps)} applications",
            font=(DesignTokens.FONT_FAMILY, 18, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY
        )
        title.pack(pady=20)
        
        # Progress
        progress_label = ctk.CTkLabel(
            install_window,
            text="Préparation...",
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_MD),
            text_color=DesignTokens.TEXT_SECONDARY
        )
        progress_label.pack(pady=10)
        
        progress_bar = ctk.CTkProgressBar(
            install_window,
            width=500,
            height=20,
            corner_radius=10,
            fg_color=DesignTokens.BG_SECONDARY,
            progress_color=DesignTokens.ACCENT_PRIMARY
        )
        progress_bar.pack(pady=10)
        progress_bar.set(0)
        
        # Log
        log_frame = ctk.CTkScrollableFrame(
            install_window,
            fg_color=DesignTokens.BG_SECONDARY,
            corner_radius=DesignTokens.RADIUS_MD
        )
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        def add_log(message):
            log = ctk.CTkLabel(
                log_frame,
                text=message,
                font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM),
                text_color=DesignTokens.TEXT_PRIMARY,
                anchor="w"
            )
            log.pack(anchor="w", padx=10, pady=2)
            log_frame._parent_canvas.yview_moveto(1.0)
        
        # Préparer liste d'installation
        apps_to_install = []
        for app_name in self.selected_apps:
            # Trouver dans programs_data pour obtenir package_id
            for category, apps in self.programs_data.items():
                if app_name in apps:
                    app_data = apps[app_name]
                    package_id = app_data.get('winget_id') or app_data.get('id') or app_name
                    method = app_data.get('install_method', 'winget')
                    apps_to_install.append((app_name, package_id, method))
                    break
        
        add_log(f"📋 {len(apps_to_install)} applications à installer")
        add_log(f"🔧 Gestionnaire: WinGet")
        add_log("")
        
        # Installer
        def on_app_complete(app_name, success, message):
            add_log(message)
        
        def on_all_complete(success_count, total_count):
            progress_bar.set(1.0)
            progress_label.configure(text=f"✅ Terminé: {success_count}/{total_count} réussies")
            add_log("")
            add_log(f"✅ Installation terminée: {success_count}/{total_count} réussies")
            
            # Bouton fermer
            close_btn = ctk.CTkButton(
                install_window,
                text="Fermer",
                command=install_window.destroy,
                fg_color=DesignTokens.ACCENT_PRIMARY
            )
            close_btn.pack(pady=10)
        
        # Lancer installations
        installer.install_multiple(
            apps_to_install,
            on_app_complete=on_app_complete,
            on_all_complete=on_all_complete
        )
        
        # Mettre à jour progress
        total = len(apps_to_install)
        def update_progress():
            # Simuler progression (à améliorer avec vrai progress)
            current = progress_bar.get()
            if current < 0.95:
                progress_bar.set(current + 0.01)
                install_window.after(500, update_progress)
        
        update_progress()
    
    def _open_website(self, app_name):
        """Ouvrir le site web de l'application"""
        import webbrowser
        
        # Dictionnaire de mapping pour URLs spécifiques
        website_map = {
            # Navigateurs
            "Google Chrome": "https://www.google.com/chrome/",
            "Mozilla Firefox": "https://www.mozilla.org/firefox/",
            "Microsoft Edge": "https://www.microsoft.com/edge",
            "Brave Browser": "https://brave.com/",
            "Opera": "https://www.opera.com/",
            "Vivaldi": "https://vivaldi.com/",
            
            # Office
            "LibreOffice": "https://www.libreoffice.org/",
            "WPS Office": "https://www.wps.com/",
            "Adobe Acrobat Reader DC": "https://get.adobe.com/reader/",
            
            # Développement
            "Visual Studio Code": "https://code.visualstudio.com/",
            "Git": "https://git-scm.com/",
            "Node.js": "https://nodejs.org/",
            "Python": "https://www.python.org/",
            "Docker Desktop": "https://www.docker.com/products/docker-desktop/",
            
            # Multimédia
            "VLC Media Player": "https://www.videolan.org/vlc/",
            "GIMP": "https://www.gimp.org/",
            "Audacity": "https://www.audacityteam.org/",
            "OBS Studio": "https://obsproject.com/",
            "HandBrake": "https://handbrake.fr/",
            
            # Utilitaires
            "7-Zip": "https://www.7-zip.org/",
            "WinRAR": "https://www.win-rar.com/",
            "CCleaner": "https://www.ccleaner.com/",
            "Everything": "https://www.voidtools.com/",
            "TreeSize Free": "https://www.jam-software.com/treesize_free",
            
            # Communication
            "Discord": "https://discord.com/",
            "Skype": "https://www.skype.com/",
            "Zoom": "https://zoom.us/",
            "Microsoft Teams": "https://www.microsoft.com/teams/",
            "Slack": "https://slack.com/",
            
            # Jeux
            "Steam": "https://store.steampowered.com/",
            "Epic Games Launcher": "https://www.epicgames.com/store/",
            "GOG Galaxy": "https://www.gog.com/galaxy",
            
            # Sécurité
            "Malwarebytes": "https://www.malwarebytes.com/",
            "Avast Free Antivirus": "https://www.avast.com/",
            "Bitdefender Antivirus Free": "https://www.bitdefender.com/",
            
            # Streaming
            "Spotify": "https://www.spotify.com/",
            "Netflix": "https://www.netflix.com/",
            "Disney+": "https://www.disneyplus.com/"
        }
        
        # Récupérer URL depuis le mapping ou générer URL de recherche
        if app_name in website_map:
            url = website_map[app_name]
        else:
            # Générer URL de recherche Google
            search_query = app_name.replace(" ", "+")
            url = f"https://www.google.com/search?q={search_query}+download+official+site"
        
        # Ouvrir dans navigateur par défaut
        try:
            webbrowser.open(url)
            print(f"🌐 Ouverture du site: {app_name} -> {url}")
        except Exception as e:
            print(f"❌ Erreur ouverture site pour {app_name}: {e}")


class OptimizedToolsPage(ctk.CTkFrame):
    """Page Outils optimisée avec sections repliables"""
    
    def __init__(self, parent, tools_data: Dict):
        super().__init__(parent, fg_color=DesignTokens.BG_PRIMARY)
        
        self.tools_data = tools_data
        
        self._create_header()
        self._create_sections()
    
    def _create_header(self):
        """Header"""
        header = ModernCard(self)
        header.pack(fill=tk.X, padx=20, pady=10)
        
        container = ctk.CTkFrame(header, fg_color="transparent")
        container.pack(fill=tk.X, padx=20, pady=15)
        
        title = ctk.CTkLabel(
            container,
            text="🛠️ Outils Système",
            font=(DesignTokens.FONT_FAMILY, 24, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY
        )
        title.pack(side=tk.LEFT)
        
        total = sum(len(tools) for tools in self.tools_data.values())
        subtitle = ctk.CTkLabel(
            container,
            text=f"{total} outils • {len(self.tools_data)} sections",
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_MD),
            text_color=DesignTokens.TEXT_SECONDARY
        )
        subtitle.pack(side=tk.LEFT, padx=20)
    
    def _create_sections(self):
        """Sections repliables"""
        scroll = ctk.CTkScrollableFrame(self, fg_color=DesignTokens.BG_PRIMARY)
        scroll.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        for section_name, tools in self.tools_data.items():
            self._create_section(scroll, section_name, tools)
    
    def _create_section(self, parent, section_name, tools):
        """Créer une section"""
        # Card section
        card = ModernCard(parent)
        card.pack(fill=tk.X, pady=5)
        
        # Container tools (caché par défaut)
        container = ctk.CTkFrame(card, fg_color="transparent")
        container.pack_forget()
        
        # État de la section (utiliser dictionnaire pour éviter erreur Pylance)
        section_state = {
            'container': container,
            'visible': False
        }
        
        # Header avec lambda qui capture section_state
        header = ctk.CTkButton(
            card,
            text=f"{section_name} ({len(tools)})",
            command=lambda: self._toggle_section(section_state, tools, section_name),
            fg_color="transparent",
            hover_color=DesignTokens.BG_HOVER,
            text_color=DesignTokens.TEXT_PRIMARY,
            font=(DesignTokens.FONT_FAMILY, 16, "bold"),
            anchor="w",
            corner_radius=0
        )
        header.pack(fill=tk.X, padx=10, pady=10)
    
    def _toggle_section(self, section_state, tools, section_name):
        """Basculer affichage section"""
        if section_state['visible']:
            # Cacher
            section_state['container'].pack_forget()
            section_state['visible'] = False
        else:
            # Afficher
            # Clear container
            for widget in section_state['container'].winfo_children():
                widget.destroy()
            
            # Ajouter TOUS les boutons - SANS LIMITE
            grid_frame = ctk.CTkFrame(section_state['container'], fg_color="transparent")
            grid_frame.pack(fill=tk.X, padx=10, pady=10)
            
            row, col = 0, 0
            max_cols = 2
            
            # Afficher TOUS les outils (pas de [:20])
            for tool_name, tool_action in tools:
                btn = ctk.CTkButton(
                    grid_frame,
                    text=tool_name,
                    command=lambda t=tool_name, a=tool_action: self._execute_tool(t, a),
                    fg_color=DesignTokens.BG_SECONDARY,
                    hover_color=DesignTokens.BG_HOVER,
                    corner_radius=DesignTokens.RADIUS_MD,
                    height=40,
                    font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM),
                    anchor="w"
                )
                btn.grid(row=row, column=col, sticky="ew", padx=5, pady=3)
                
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1
            
            # Configurer colonnes
            for i in range(max_cols):
                grid_frame.columnconfigure(i, weight=1)
            
            # Afficher total outils
            total_label = ctk.CTkLabel(
                section_state['container'],
                text=f"✅ {len(tools)} outils dans cette section",
                font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM),
                text_color=DesignTokens.SUCCESS
            )
            total_label.pack(pady=5)
            
            section_state['container'].pack(fill=tk.X)
            section_state['visible'] = True
    
    def _execute_tool(self, tool_name, tool_action):
        """Exécuter outil (commande ou URL)"""
        import subprocess
        import webbrowser
        import os
        
        print(f"🔧 Exécution: {tool_name}")
        print(f"   Action: {tool_action}")
        
        try:
            # Déterminer si c'est une URL ou une commande
            if tool_action.startswith(('http://', 'https://', 'ms-settings:', 'windowsdefender:')):
                # C'est une URL - ouvrir dans le navigateur
                print(f"🌐 Ouverture URL: {tool_action}")
                webbrowser.open(tool_action)
                
            else:
                # C'est une commande système - l'exécuter
                print(f"⚡ Exécution commande: {tool_action}")
                
                # Déterminer si on doit utiliser cmd.exe ou PowerShell
                if 'Get-AppXPackage' in tool_action or tool_action.startswith('Get-'):
                    # Commande PowerShell
                    subprocess.Popen(
                        ['powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', tool_action],
                        creationflags=subprocess.CREATE_NEW_CONSOLE
                    )
                else:
                    # Commande CMD standard
                    # Remplacer && par & pour Windows CMD
                    cmd_action = tool_action.replace('&&', '&')
                    
                    # Certaines commandes doivent être lancées directement
                    direct_commands = [
                        'msinfo32', 'dxdiag', 'eventvwr.msc', 'devmgmt.msc', 'taskmgr',
                        'resmon', 'diskmgmt.msc', 'compmgmt.msc', 'services.msc', 'perfmon',
                        'dfrgui', 'regedit', 'gpedit.msc', 'secpol.msc', 'netplwiz',
                        'printmanagement.msc', 'dcomcnfg', 'appwiz.cpl', 'systempropertiesadvanced',
                        'desk.cpl', 'mmsys.cpl', 'joy.cpl', 'main.cpl', 'intl.cpl',
                        'timedate.cpl', 'powercfg.cpl', 'cleanmgr', 'wsreset', 'ncpa.cpl',
                        'sndvol', 'systemreset'
                    ]
                    
                    # Vérifier si c'est une commande directe
                    is_direct = any(cmd in tool_action for cmd in direct_commands)
                    
                    if is_direct:
                        # Lancer directement sans cmd
                        subprocess.Popen(tool_action, shell=True)
                    else:
                        # Lancer avec cmd /k pour garder la fenêtre ouverte
                        subprocess.Popen(
                            f'cmd.exe /k {cmd_action}',
                            creationflags=subprocess.CREATE_NEW_CONSOLE
                        )
                
                print(f"✅ Commande lancée avec succès")
                
        except Exception as e:
            print(f"❌ Erreur lors de l'exécution de '{tool_name}': {e}")
            # Afficher une notification d'erreur à l'utilisateur
            try:
                import tkinter.messagebox as messagebox
                messagebox.showerror(
                    "Erreur d'exécution",
                    f"Impossible d'exécuter '{tool_name}':\n{str(e)}"
                )
            except:
                pass