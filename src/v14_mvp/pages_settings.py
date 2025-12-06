#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Page Paramètres Complète - NiTriTe V14
10 sections de configuration
"""

import customtkinter as ctk
import tkinter as tk
from typing import Callable
from v14_mvp.design_system import DesignTokens
from v14_mvp.components import ModernCard, ModernButton


class SettingsPage(ctk.CTkFrame):
    """Page Paramètres complète avec 10 sections"""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color=DesignTokens.BG_PRIMARY)
        
        self._create_header()
        self._create_settings()
    
    def _create_header(self):
        """Header"""
        header = ModernCard(self)
        header.pack(fill=tk.X, padx=20, pady=10)
        
        container = ctk.CTkFrame(header, fg_color="transparent")
        container.pack(fill=tk.X, padx=20, pady=15)
        
        title = ctk.CTkLabel(
            container,
            text="⚙️ Paramètres",
            font=(DesignTokens.FONT_FAMILY, 24, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY
        )
        title.pack(side=tk.LEFT)
        
        subtitle = ctk.CTkLabel(
            container,
            text="Configuration complète de l'application",
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_MD),
            text_color=DesignTokens.TEXT_SECONDARY
        )
        subtitle.pack(side=tk.LEFT, padx=20)
    
    def _create_settings(self):
        """Créer sections de paramètres"""
        scroll = ctk.CTkScrollableFrame(self, fg_color=DesignTokens.BG_PRIMARY)
        scroll.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 1. Apparence
        self._create_appearance_section(scroll)
        
        # 2. Langue
        self._create_language_section(scroll)
        
        # 3. Mises à jour
        self._create_updates_section(scroll)
        
        # 4. Performances
        self._create_performance_section(scroll)
        
        # 5. Installation
        self._create_installation_section(scroll)
        
        # 6. Sauvegarde
        self._create_backup_section(scroll)
        
        # 7. Notifications
        self._create_notifications_section(scroll)
        
        # 8. Avancé
        self._create_advanced_section(scroll)
        
        # 9. À propos
        self._create_about_section(scroll)
        
        # 10. Actions
        self._create_actions_section(scroll)
    
    def _create_appearance_section(self, parent):
        """Section Apparence"""
        card = ModernCard(parent)
        card.pack(fill=tk.X, pady=10)
        
        # Titre
        self._create_section_title(card, "🎨 Apparence", "Personnalisation de l'interface")
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Thème
        self._create_option(
            content,
            "Thème",
            "Sélectionner le jeu de couleurs",
            self._create_theme_selector
        )
        
        # Mode
        self._create_option(
            content,
            "Mode d'affichage",
            "Clair ou sombre",
            self._create_mode_selector
        )
        
        # Taille police
        self._create_option(
            content,
            "Taille de police",
            "Ajuster la lisibilité",
            self._create_font_slider
        )
    
    def _create_language_section(self, parent):
        """Section Langue"""
        card = ModernCard(parent)
        card.pack(fill=tk.X, pady=10)
        
        self._create_section_title(card, "🌍 Langue", "Sélection de la langue")
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        self._create_option(
            content,
            "Langue de l'interface",
            "Français ou Anglais",
            self._create_language_selector
        )
    
    def _create_updates_section(self, parent):
        """Section Mises à jour"""
        card = ModernCard(parent)
        card.pack(fill=tk.X, pady=10)
        
        self._create_section_title(card, "🔄 Mises à jour", "Gestion des mises à jour")
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        self._create_option(
            content,
            "Vérification automatique",
            "Chercher les mises à jour au démarrage",
            self._create_auto_update_toggle
        )
        
        self._create_option(
            content,
            "Canal de mise à jour",
            "Stable ou Beta",
            self._create_update_channel_selector
        )
    
    def _create_performance_section(self, parent):
        """Section Performances"""
        card = ModernCard(parent)
        card.pack(fill=tk.X, pady=10)
        
        self._create_section_title(card, "⚡ Performances", "Optimisation de l'application")
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        self._create_option(
            content,
            "Limite d'apps par catégorie",
            "Nombre maximum d'applications affichées",
            self._create_app_limit_slider
        )
        
        self._create_option(
            content,
            "Animation",
            "Activer les animations d'interface",
            self._create_animation_toggle
        )
    
    def _create_installation_section(self, parent):
        """Section Installation"""
        card = ModernCard(parent)
        card.pack(fill=tk.X, pady=10)
        
        self._create_section_title(card, "📦 Installation", "Options d'installation")
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        self._create_option(
            content,
            "Gestionnaire par défaut",
            "WinGet, Chocolatey ou Téléchargement",
            self._create_package_manager_selector
        )
        
        self._create_option(
            content,
            "Dossier de téléchargement",
            "Emplacement des fichiers téléchargés",
            self._create_download_folder_selector
        )
    
    def _create_backup_section(self, parent):
        """Section Sauvegarde"""
        card = ModernCard(parent)
        card.pack(fill=tk.X, pady=10)
        
        self._create_section_title(card, "💾 Sauvegarde", "Sauvegarde automatique")
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        self._create_option(
            content,
            "Sauvegarde automatique",
            "Sauvegarder la configuration régulièrement",
            self._create_auto_backup_toggle
        )
    
    def _create_notifications_section(self, parent):
        """Section Notifications"""
        card = ModernCard(parent)
        card.pack(fill=tk.X, pady=10)
        
        self._create_section_title(card, "🔔 Notifications", "Alertes et notifications")
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        self._create_option(
            content,
            "Notifications système",
            "Afficher les notifications Windows",
            self._create_notifications_toggle
        )
        
        self._create_option(
            content,
            "Sons",
            "Activer les sons de notification",
            self._create_sounds_toggle
        )
    
    def _create_advanced_section(self, parent):
        """Section Avancé"""
        card = ModernCard(parent)
        card.pack(fill=tk.X, pady=10)
        
        self._create_section_title(card, "🔧 Avancé", "Options avancées")
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        self._create_option(
            content,
            "Mode Debug",
            "Activer les logs détaillés",
            self._create_debug_toggle
        )
        
        self._create_option(
            content,
            "Portable",
            "Mode portable (données dans le dossier app)",
            self._create_portable_toggle
        )
    
    def _create_about_section(self, parent):
        """Section À propos"""
        card = ModernCard(parent)
        card.pack(fill=tk.X, pady=10)
        
        self._create_section_title(card, "ℹ️ À propos", "Informations sur l'application")
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        info_text = """
        NiTriTe V17.0 Beta
        Maintenance Informatique Professionnelle

        ✅ 700+ applications disponibles
        ✅ 500+ outils système
        ✅ Installation automatisée
        ✅ Interface moderne Material Design 3

        © 2024 - Tous droits réservés
        """
        
        info = ctk.CTkLabel(
            content,
            text=info_text,
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM),
            text_color=DesignTokens.TEXT_SECONDARY,
            justify="left"
        )
        info.pack(pady=10)
    
    def _create_actions_section(self, parent):
        """Section Actions"""
        card = ModernCard(parent)
        card.pack(fill=tk.X, pady=10)
        
        self._create_section_title(card, "🚀 Actions", "Actions rapides")
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        actions_frame = ctk.CTkFrame(content, fg_color="transparent")
        actions_frame.pack(fill=tk.X, pady=10)
        
        ModernButton(
            actions_frame,
            text="💾 Sauvegarder Configuration",
            variant="filled",
            command=self._save_config
        ).pack(side=tk.LEFT, padx=5)
        
        ModernButton(
            actions_frame,
            text="🔄 Réinitialiser",
            variant="outlined",
            command=self._reset_config
        ).pack(side=tk.LEFT, padx=5)
        
        ModernButton(
            actions_frame,
            text="📂 Ouvrir Dossier Config",
            variant="text",
            command=self._open_config_folder
        ).pack(side=tk.LEFT, padx=5)
    
    # Helpers
    def _create_section_title(self, parent, title, subtitle):
        """Créer titre de section"""
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        title_label = ctk.CTkLabel(
            header,
            text=title,
            font=(DesignTokens.FONT_FAMILY, 18, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY,
            anchor="w"
        )
        title_label.pack(anchor="w")
        
        subtitle_label = ctk.CTkLabel(
            header,
            text=subtitle,
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM),
            text_color=DesignTokens.TEXT_TERTIARY,
            anchor="w"
        )
        subtitle_label.pack(anchor="w")
    
    def _create_option(self, parent, label, description, widget_creator):
        """Créer une option de paramètre"""
        frame = ctk.CTkFrame(
            parent,
            fg_color=DesignTokens.BG_SECONDARY,
            corner_radius=DesignTokens.RADIUS_MD
        )
        frame.pack(fill=tk.X, pady=5)
        
        content = ctk.CTkFrame(frame, fg_color="transparent")
        content.pack(fill=tk.X, padx=15, pady=12)
        
        # Label et description à gauche
        left = ctk.CTkFrame(content, fg_color="transparent")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        label_widget = ctk.CTkLabel(
            left,
            text=label,
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_MD, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY,
            anchor="w"
        )
        label_widget.pack(anchor="w")
        
        desc_widget = ctk.CTkLabel(
            left,
            text=description,
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM),
            text_color=DesignTokens.TEXT_TERTIARY,
            anchor="w"
        )
        desc_widget.pack(anchor="w")
        
        # Widget de contrôle à droite
        right = ctk.CTkFrame(content, fg_color="transparent")
        right.pack(side=tk.RIGHT)
        
        widget_creator(right)
    
    # Widget creators
    def _create_theme_selector(self, parent):
        themes = ["Orange NiTriTe", "Bleu Pro", "Vert Tech", "Violet Creative", "Rouge Energy"]
        selector = ctk.CTkOptionMenu(
            parent,
            values=themes,
            command=self._on_theme_change,
            fg_color=DesignTokens.ACCENT_PRIMARY,
            button_color=DesignTokens.ACCENT_PRIMARY,
            button_hover_color=DesignTokens.BG_HOVER
        )
        selector.set("Orange NiTriTe")
        selector.pack()
    
    def _create_mode_selector(self, parent):
        modes = ["Sombre", "Clair", "Auto"]
        selector = ctk.CTkOptionMenu(
            parent,
            values=modes,
            command=self._on_mode_change,
            fg_color=DesignTokens.ACCENT_PRIMARY
        )
        selector.set("Sombre")
        selector.pack()
    
    def _create_font_slider(self, parent):
        slider = ctk.CTkSlider(
            parent,
            from_=12,
            to=20,
            number_of_steps=8,
            command=self._on_font_size_change,
            fg_color=DesignTokens.BG_HOVER,
            progress_color=DesignTokens.ACCENT_PRIMARY,
            button_color=DesignTokens.ACCENT_PRIMARY,
            button_hover_color=DesignTokens.BG_HOVER
        )
        slider.set(14)
        slider.pack()
    
    def _create_language_selector(self, parent):
        languages = ["🇫🇷 Français", "🇬🇧 English"]
        selector = ctk.CTkOptionMenu(
            parent,
            values=languages,
            command=self._on_language_change,
            fg_color=DesignTokens.ACCENT_PRIMARY
        )
        selector.set("🇫🇷 Français")
        selector.pack()
    
    def _create_auto_update_toggle(self, parent):
        switch = ctk.CTkSwitch(
            parent,
            text="",
            command=self._on_auto_update_toggle,
            fg_color=DesignTokens.BG_HOVER,
            progress_color=DesignTokens.SUCCESS,
            button_color=DesignTokens.TEXT_PRIMARY,
            button_hover_color=DesignTokens.TEXT_SECONDARY
        )
        switch.select()
        switch.pack()
    
    def _create_update_channel_selector(self, parent):
        channels = ["Stable", "Beta"]
        selector = ctk.CTkOptionMenu(
            parent,
            values=channels,
            command=self._on_channel_change,
            fg_color=DesignTokens.ACCENT_PRIMARY
        )
        selector.set("Stable")
        selector.pack()
    
    def _create_app_limit_slider(self, parent):
        slider = ctk.CTkSlider(
            parent,
            from_=10,
            to=50,
            number_of_steps=8,
            command=self._on_app_limit_change,
            fg_color=DesignTokens.BG_HOVER,
            progress_color=DesignTokens.ACCENT_PRIMARY
        )
        slider.set(20)
        slider.pack()
    
    def _create_animation_toggle(self, parent):
        switch = ctk.CTkSwitch(
            parent,
            text="",
            command=self._on_animation_toggle,
            fg_color=DesignTokens.BG_HOVER,
            progress_color=DesignTokens.SUCCESS
        )
        switch.select()
        switch.pack()
    
    def _create_package_manager_selector(self, parent):
        managers = ["WinGet", "Chocolatey", "Téléchargement Direct"]
        selector = ctk.CTkOptionMenu(
            parent,
            values=managers,
            command=self._on_package_manager_change,
            fg_color=DesignTokens.ACCENT_PRIMARY
        )
        selector.set("WinGet")
        selector.pack()
    
    def _create_download_folder_selector(self, parent):
        btn = ModernButton(
            parent,
            text="📂 Parcourir...",
            variant="outlined",
            size="sm",
            command=self._browse_download_folder
        )
        btn.pack()
    
    def _create_auto_backup_toggle(self, parent):
        switch = ctk.CTkSwitch(
            parent,
            text="",
            command=self._on_auto_backup_toggle,
            fg_color=DesignTokens.BG_HOVER,
            progress_color=DesignTokens.SUCCESS
        )
        switch.select()
        switch.pack()
    
    def _create_notifications_toggle(self, parent):
        switch = ctk.CTkSwitch(
            parent,
            text="",
            command=self._on_notifications_toggle,
            fg_color=DesignTokens.BG_HOVER,
            progress_color=DesignTokens.SUCCESS
        )
        switch.select()
        switch.pack()
    
    def _create_sounds_toggle(self, parent):
        switch = ctk.CTkSwitch(
            parent,
            text="",
            command=self._on_sounds_toggle,
            fg_color=DesignTokens.BG_HOVER,
            progress_color=DesignTokens.SUCCESS
        )
        switch.pack()
    
    def _create_debug_toggle(self, parent):
        switch = ctk.CTkSwitch(
            parent,
            text="",
            command=self._on_debug_toggle,
            fg_color=DesignTokens.BG_HOVER,
            progress_color=DesignTokens.WARNING
        )
        switch.pack()
    
    def _create_portable_toggle(self, parent):
        switch = ctk.CTkSwitch(
            parent,
            text="",
            command=self._on_portable_toggle,
            fg_color=DesignTokens.BG_HOVER,
            progress_color=DesignTokens.INFO
        )
        switch.pack()
    
    # Callbacks
    def _on_theme_change(self, value):
        print(f"🎨 Thème changé: {value}")
    
    def _on_mode_change(self, value):
        """Changer le mode d'affichage (clair/sombre)"""
        print(f"🌓 Mode changé: {value}")
        
        # Mapper les valeurs
        mode_map = {
            "Sombre": "dark",
            "Clair": "light",
            "Auto": "system"
        }
        
        if value in mode_map:
            ctk_mode = mode_map[value]
            try:
                ctk.set_appearance_mode(ctk_mode)
                print(f"✅ Mode appliqué: {ctk_mode}")
            except Exception as e:
                print(f"❌ Erreur changement mode: {e}")
    
    def _on_font_size_change(self, value):
        print(f"🔤 Taille police: {int(value)}px")
    
    def _on_language_change(self, value):
        print(f"🌍 Langue: {value}")
    
    def _on_auto_update_toggle(self):
        print("🔄 Auto-update toggled")
    
    def _on_channel_change(self, value):
        print(f"📡 Canal: {value}")
    
    def _on_app_limit_change(self, value):
        print(f"📊 Limite apps: {int(value)}")
    
    def _on_animation_toggle(self):
        print("✨ Animations toggled")
    
    def _on_package_manager_change(self, value):
        print(f"📦 Gestionnaire: {value}")
    
    def _browse_download_folder(self):
        print("📂 Parcourir dossier téléchargement")
    
    def _on_auto_backup_toggle(self):
        print("💾 Auto-backup toggled")
    
    def _on_notifications_toggle(self):
        print("🔔 Notifications toggled")
    
    def _on_sounds_toggle(self):
        print("🔊 Sons toggled")
    
    def _on_debug_toggle(self):
        print("🐛 Debug mode toggled")
    
    def _on_portable_toggle(self):
        print("💼 Mode portable toggled")
    
    def _save_config(self):
        print("💾 Sauvegarde configuration...")
    
    def _reset_config(self):
        print("🔄 Réinitialisation configuration...")
    
    def _open_config_folder(self):
        print("📂 Ouverture dossier config...")