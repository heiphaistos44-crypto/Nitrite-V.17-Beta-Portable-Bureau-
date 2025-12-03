# 💻 CODE COMPLET - NiTriTe V14 MVP

**INSTRUCTIONS :** Copiez chaque bloc de code dans le fichier correspondant.

---

## 📁 STRUCTURE À CRÉER

```
src/v14_mvp/
├── design_system.py          ✅ DÉJÀ CRÉÉ
├── components.py              ← À CRÉER
├── navigation.py              ← À CRÉER
├── pages_simple.py            ← À CRÉER
└── main_app.py                ← À CRÉER

LANCER_V14_MVP.bat             ← À CRÉER (racine projet)
```

---

## 📄 FICHIER 1 : `src/v14_mvp/components.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Composants Modernes - NiTriTe V14 MVP
Composants réutilisables avec design moderne
"""

import customtkinter as ctk
import tkinter as tk
from typing import Callable, Optional
from .design_system import DesignTokens, ModernColors


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
```

---

## 📄 FICHIER 2 : `src/v14_mvp/navigation.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Navigation Moderne - NiTriTe V14 MVP
Barre de navigation latérale
"""

import customtkinter as ctk
import tkinter as tk
from .design_system import DesignTokens, ModernColors


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
```

---

## 📄 FICHIER 3 : `src/v14_mvp/pages_simple.py`

```python
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
from .design_system import DesignTokens, ModernColors
from .components import ModernCard, ModernSearchBar, ModernStatsCard, ModernButton


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
```

**[SUITE DANS LE PROCHAIN MESSAGE - Fichiers 4 et 5]**