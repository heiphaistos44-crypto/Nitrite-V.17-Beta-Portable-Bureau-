#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Navigation Moderne - NiTriTe V14 MVP
Barre de navigation latérale
"""

import customtkinter as ctk
import tkinter as tk
from v14_mvp.design_system import DesignTokens, ModernColors


class ModernNavigation(ctk.CTkFrame):
    """Barre de navigation latérale moderne"""
    
    def __init__(self, parent, on_page_change):
        super().__init__(
            parent,
            fg_color=DesignTokens.BG_SECONDARY,
            width=280,
            corner_radius=0
        )
        
        self.on_page_change = on_page_change
        self.current_page = "applications"
        self.nav_buttons = {}
        
        self._create_header()
        self._create_nav_buttons()
        self._create_footer()
    
    def _create_header(self):
        """Header avec logo"""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill=tk.X, padx=DesignTokens.SPACING_MD, pady=DesignTokens.SPACING_LG)
        
        # Logo
        logo_frame = ctk.CTkFrame(
            header,
            fg_color=DesignTokens.ACCENT_PRIMARY,
            width=50,
            height=50,
            corner_radius=DesignTokens.RADIUS_MD
        )
        logo_frame.pack(side=tk.LEFT)
        logo_frame.pack_propagate(False)
        
        logo_label = ctk.CTkLabel(
            logo_frame,
            text="N",
            font=(DesignTokens.FONT_FAMILY, 28, "bold"),
            text_color="white"
        )
        logo_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Info
        info_frame = ctk.CTkFrame(header, fg_color="transparent")
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=DesignTokens.SPACING_MD)
        
        title = ctk.CTkLabel(
            info_frame,
            text="NiTriTe",
            font=(DesignTokens.FONT_FAMILY, 20, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY,
            anchor='w'
        )
        title.pack(fill=tk.X)
        
        version = ctk.CTkLabel(
            info_frame,
            text="Version 14.0 MVP",
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM),
            text_color=DesignTokens.TEXT_SECONDARY,
            anchor='w'
        )
        version.pack(fill=tk.X)
        
        # Séparateur
        sep = ctk.CTkFrame(self, fg_color=DesignTokens.BORDER_DEFAULT, height=1)
        sep.pack(fill=tk.X, padx=DesignTokens.SPACING_MD, pady=DesignTokens.SPACING_MD)
    
    def _create_nav_buttons(self):
        """Créer boutons navigation"""
        pages = [
            ("applications", "📦", "Applications"),
            ("tools", "🛠️", "Outils"),
            ("master_install", "🚀", "Master Install"),
            ("portables", "💼", "Apps Portables"),
            ("terminal", "💻", "Terminal"),
            ("updates", "🔄", "Mises à jour"),
            ("backup", "💾", "Sauvegarde"),
            ("optimizations", "⚡", "Optimisations"),
            ("diagnostic", "🔍", "Diagnostic"),
            ("settings", "⚙️", "Paramètres"),
        ]
        
        for page_id, icon, title in pages:
            btn = self._create_nav_button(page_id, icon, title)
            self.nav_buttons[page_id] = btn
        
        # Sélectionner première page
        self._select_page("applications")
    
    def _create_nav_button(self, page_id, icon, title):
        """Créer un bouton de navigation"""
        btn_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
            corner_radius=DesignTokens.RADIUS_MD,
            cursor="hand2"
        )
        btn_frame.pack(fill=tk.X, padx=DesignTokens.SPACING_MD, pady=DesignTokens.SPACING_XS)
        
        # Content
        content = ctk.CTkFrame(btn_frame, fg_color="transparent")
        content.pack(fill=tk.BOTH, expand=True, padx=DesignTokens.SPACING_SM, pady=DesignTokens.SPACING_SM)
        
        # Icône
        icon_label = ctk.CTkLabel(
            content,
            text=icon,
            font=(DesignTokens.FONT_FAMILY, 18),
            text_color=DesignTokens.TEXT_SECONDARY
        )
        icon_label.pack(side=tk.LEFT, padx=DesignTokens.SPACING_SM)
        
        # Titre
        title_label = ctk.CTkLabel(
            content,
            text=title,
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_MD),
            text_color=DesignTokens.TEXT_SECONDARY,
            anchor='w'
        )
        title_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Store references
        btn_frame.icon_label = icon_label
        btn_frame.title_label = title_label
        
        # Bind events
        for widget in [btn_frame, content, icon_label, title_label]:
            widget.bind('<Button-1>', lambda e, pid=page_id: self._on_click(pid))
            widget.bind('<Enter>', lambda e, b=btn_frame: self._on_hover(b, True))
            widget.bind('<Leave>', lambda e, b=btn_frame: self._on_hover(b, False))
        
        return btn_frame
    
    def _on_click(self, page_id):
        """Gérer clic navigation"""
        self._select_page(page_id)
        self.on_page_change(page_id)
    
    def _on_hover(self, btn, is_enter):
        """Gérer hover"""
        is_active = btn.cget('fg_color') == DesignTokens.ACCENT_PRIMARY
        
        if not is_active:
            if is_enter:
                btn.configure(fg_color=DesignTokens.BG_HOVER)
            else:
                btn.configure(fg_color="transparent")
    
    def _select_page(self, page_id):
        """Sélectionner une page"""
        # Désélectionner tout
        for pid, btn in self.nav_buttons.items():
            if pid != page_id:
                btn.configure(fg_color="transparent")
                btn.icon_label.configure(text_color=DesignTokens.TEXT_SECONDARY)
                btn.title_label.configure(text_color=DesignTokens.TEXT_SECONDARY)
        
        # Sélectionner nouveau
        if page_id in self.nav_buttons:
            btn = self.nav_buttons[page_id]
            btn.configure(fg_color=DesignTokens.ACCENT_PRIMARY)
            btn.icon_label.configure(text_color="white")
            btn.title_label.configure(text_color="white")
            self.current_page = page_id
    
    def _create_footer(self):
        """Footer"""
        spacer = ctk.CTkFrame(self, fg_color="transparent")
        spacer.pack(fill=tk.BOTH, expand=True)
        
        footer = ctk.CTkFrame(self, fg_color=DesignTokens.BG_PRIMARY)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        
        footer_text = ctk.CTkLabel(
            footer,
            text="© 2024 OrdiPlus",
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_XS),
            text_color=DesignTokens.TEXT_TERTIARY
        )
        footer_text.pack(pady=DesignTokens.SPACING_MD)