#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Composants Modernes - NiTriTe V14 MVP
Composants réutilisables avec design moderne
"""

import customtkinter as ctk
import tkinter as tk
from typing import Callable, Optional
from v14_mvp.design_system import DesignTokens, ModernColors


class ModernButton(ctk.CTkButton):
    """Bouton moderne avec 3 variantes"""
    
    def __init__(self, parent, variant="filled", size="md", **kwargs):
        # Styles selon variante
        if variant == "filled":
            fg_color = DesignTokens.ACCENT_PRIMARY
            hover_color = DesignTokens.ACCENT_HOVER
            text_color = DesignTokens.TEXT_PRIMARY
            border_width = 0
        elif variant == "outlined":
            fg_color = "transparent"
            hover_color = DesignTokens.BG_HOVER
            text_color = DesignTokens.ACCENT_PRIMARY
            border_width = 2
            kwargs['border_color'] = DesignTokens.ACCENT_PRIMARY
        else:  # text
            fg_color = "transparent"
            hover_color = DesignTokens.BG_HOVER
            text_color = DesignTokens.TEXT_PRIMARY
            border_width = 0
        
        # Tailles
        sizes = {
            'sm': (100, 32, DesignTokens.FONT_SIZE_SM),
            'md': (140, 40, DesignTokens.FONT_SIZE_MD),
            'lg': (180, 48, DesignTokens.FONT_SIZE_LG)
        }
        width, height, font_size = sizes.get(size, sizes['md'])
        
        super().__init__(
            parent,
            fg_color=fg_color,
            hover_color=hover_color,
            text_color=text_color,
            border_width=border_width,
            corner_radius=DesignTokens.RADIUS_MD,
            width=width,
            height=height,
            font=(DesignTokens.FONT_FAMILY, font_size, "bold"),
            cursor="hand2",
            **kwargs
        )


class ModernCard(ctk.CTkFrame):
    """Carte moderne avec coins très arrondis"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color=DesignTokens.BG_ELEVATED,
            corner_radius=DesignTokens.RADIUS_LG,
            **kwargs
        )


class ModernSearchBar(ctk.CTkFrame):
    """Barre de recherche moderne"""
    
    def __init__(self, parent, placeholder="Rechercher...", on_search=None, **kwargs):
        super().__init__(
            parent,
            fg_color=DesignTokens.BG_ELEVATED,
            corner_radius=DesignTokens.RADIUS_LG,
            **kwargs
        )
        
        self.on_search = on_search
        
        # Container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill=tk.BOTH, expand=True, padx=DesignTokens.SPACING_SM, pady=DesignTokens.SPACING_SM)
        
        # Icône
        icon = ctk.CTkLabel(
            container,
            text="🔍",
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_LG),
            text_color=DesignTokens.ACCENT_PRIMARY
        )
        icon.pack(side=tk.LEFT, padx=DesignTokens.SPACING_SM)
        
        # Entry
        self.entry = ctk.CTkEntry(
            container,
            placeholder_text=placeholder,
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_MD),
            fg_color="transparent",
            border_width=0
        )
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.entry.bind('<KeyRelease>', self._on_key_release)
        
        # Bouton clear
        self.clear_btn = ctk.CTkLabel(
            container,
            text="✕",
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_MD, "bold"),
            text_color=DesignTokens.TEXT_TERTIARY,
            cursor="hand2"
        )
        self.clear_btn.pack(side=tk.RIGHT, padx=DesignTokens.SPACING_SM)
        self.clear_btn.bind('<Button-1>', self._clear)
    
    def _on_key_release(self, event):
        if self.on_search:
            self.on_search(self.entry.get())
    
    def _clear(self, event):
        self.entry.delete(0, tk.END)
        if self.on_search:
            self.on_search("")


class ModernStatsCard(ctk.CTkFrame):
    """Carte statistique moderne"""
    
    def __init__(self, parent, title, value, icon, color, **kwargs):
        super().__init__(
            parent,
            fg_color=DesignTokens.BG_ELEVATED,
            corner_radius=DesignTokens.RADIUS_LG,
            **kwargs
        )
        
        # Container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill=tk.BOTH, expand=True, padx=DesignTokens.SPACING_MD, pady=DesignTokens.SPACING_MD)
        
        # Icône
        icon_label = ctk.CTkLabel(
            container,
            text=icon,
            font=(DesignTokens.FONT_FAMILY, 24),
            text_color=color
        )
        icon_label.pack(side=tk.LEFT, padx=(0, DesignTokens.SPACING_MD))
        
        # Texte
        text_frame = ctk.CTkFrame(container, fg_color="transparent")
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        title_label = ctk.CTkLabel(
            text_frame,
            text=title,
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM),
            text_color=DesignTokens.TEXT_SECONDARY,
            anchor='w'
        )
        title_label.pack(fill=tk.X)
        
        self.value_label = ctk.CTkLabel(
            text_frame,
            text=str(value),
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_2XL, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY,
            anchor='w'
        )
        self.value_label.pack(fill=tk.X)
    
    def update_value(self, new_value):
        """Mettre à jour la valeur"""
        self.value_label.configure(text=str(new_value))