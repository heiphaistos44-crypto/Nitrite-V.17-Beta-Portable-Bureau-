#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pages Simplifiées - NiTriTe V14 MVP
Versions simplifiées des pages pour MVP
"""

import customtkinter as ctk
import tkinter as tk
import json
import os
from v14_mvp.design_system import DesignTokens, ModernColors
from v14_mvp.components import ModernCard, ModernSearchBar, ModernStatsCard, ModernButton


class SimpleApplicationsPage(ctk.CTkFrame):
    """Page Applications simplifiée"""
    
    def __init__(self, parent, programs_data):
        super().__init__(parent, fg_color=DesignTokens.BG_PRIMARY)
        self.programs_data = programs_data
        
        self._create_header()
        self._create_stats()
        self._create_content()
    
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
        
        # Boutons actions
        actions = ctk.CTkFrame(container, fg_color="transparent")
        actions.pack(side=tk.RIGHT)
        
        ModernButton(
            actions,
            text="✓ Tout sélectionner",
            variant="outlined",
            size="sm"
        ).pack(side=tk.LEFT, padx=5)
        
        ModernButton(
            actions,
            text="✕ Désélectionner",
            variant="text",
            size="sm"
        ).pack(side=tk.LEFT)
    
    def _create_stats(self):
        """Stats"""
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        total_apps = sum(len(apps) for apps in self.programs_data.values())
        
        ModernStatsCard(
            stats_frame,
            "Applications",
            total_apps,
            "📦",
            DesignTokens.ACCENT_PRIMARY
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        ModernStatsCard(
            stats_frame,
            "Catégories",
            len(self.programs_data),
            "📁",
            DesignTokens.INFO
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        ModernStatsCard(
            stats_frame,
            "Sélectionnées",
            0,
            "✓",
            DesignTokens.SUCCESS
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    
    def _create_content(self):
        """Contenu"""
        # Recherche
        search = ModernSearchBar(
            self,
            placeholder="Rechercher parmi 716 applications..."
        )
        search.pack(fill=tk.X, padx=20, pady=10)
        
        # Message
        message = ModernCard(self)
        message.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        msg_label = ctk.CTkLabel(
            message,
            text=f"✅ {sum(len(apps) for apps in self.programs_data.values())} applications chargées\n\n"
                 "🚀 Version MVP - Interface simplifiée\n\n"
                 "📝 Fonctionnalités complètes disponibles en v1.1+",
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_LG),
            text_color=DesignTokens.TEXT_SECONDARY,
            justify=tk.CENTER
        )
        msg_label.pack(expand=True)


class SimpleToolsPage(ctk.CTkFrame):
    """Page Outils simplifiée"""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color=DesignTokens.BG_PRIMARY)
        
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
            text="🛠️ Outils Système",
            font=(DesignTokens.FONT_FAMILY, 24, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY
        )
        title.pack(side=tk.LEFT)
        
        subtitle = ctk.CTkLabel(
            container,
            text="548+ outils disponibles",
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_MD),
            text_color=DesignTokens.TEXT_SECONDARY
        )
        subtitle.pack(side=tk.LEFT, padx=20)
    
    def _create_content(self):
        """Contenu"""
        # Recherche
        search = ModernSearchBar(
            self,
            placeholder="Rechercher un outil..."
        )
        search.pack(fill=tk.X, padx=20, pady=10)
        
        # Message
        message = ModernCard(self)
        message.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        msg_label = ctk.CTkLabel(
            message,
            text="✅ 548+ outils système disponibles\n\n"
                 "🚀 Version MVP - Interface simplifiée\n\n"
                 "📝 Grille complète disponible en v1.1+",
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_LG),
            text_color=DesignTokens.TEXT_SECONDARY,
            justify=tk.CENTER
        )
        msg_label.pack(expand=True)


class SimplePlaceholderPage(ctk.CTkFrame):
    """Page placeholder pour les autres sections"""
    
    def __init__(self, parent, title, icon, message):
        super().__init__(parent, fg_color=DesignTokens.BG_PRIMARY)
        
        # Card centrée
        card = ModernCard(self)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        container = ctk.CTkFrame(card, fg_color="transparent")
        container.pack(padx=60, pady=60)
        
        # Icône
        icon_label = ctk.CTkLabel(
            container,
            text=icon,
            font=(DesignTokens.FONT_FAMILY, 48)
        )
        icon_label.pack(pady=10)
        
        # Titre
        title_label = ctk.CTkLabel(
            container,
            text=title,
            font=(DesignTokens.FONT_FAMILY, 24, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY
        )
        title_label.pack(pady=5)
        
        # Message
        msg_label = ctk.CTkLabel(
            container,
            text=message,
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_MD),
            text_color=DesignTokens.TEXT_SECONDARY,
            justify=tk.CENTER
        )
        msg_label.pack(pady=10)
        
        # Bouton
        ModernButton(
            container,
            text="Bientôt disponible",
            variant="outlined",
            size="md"
        ).pack(pady=10)