"""
CustomTkinter Wrapper pour NiTriTe V13
Wrapper de compatibilité pour migration progressive vers CustomTkinter
"""

import customtkinter as ctk
from typing import Optional, Callable


# ============================================================================
# CONFIGURATION DU THÈME
# ============================================================================

def configure_ctk_theme():
    """Configure le thème CustomTkinter pour NiTriTe"""
    try:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
    except Exception as e:
        print(f"Warning: Erreur configuration thème CTk: {e}")


# ============================================================================
# COULEURS NITRITE (importées depuis modern_colors.py)
# ============================================================================

class NiTriTeColors:
    """Palette de couleurs NiTriTe pour CustomTkinter"""

    # Couleurs de fond
    BG_DARK = "#1a1a1a"          # Fond principal
    BG_MEDIUM = "#2d2d2d"        # Fond secondaire
    BG_LIGHT = "#3a3a3a"         # Fond tertiaire
    BG_CARD = "#252525"          # Fond des cartes

    # Couleur principale
    ORANGE_PRIMARY = "#FF6B35"   # Orange NiTriTe
    ORANGE_HOVER = "#ff8555"     # Orange hover
    ORANGE_PRESSED = "#e55525"   # Orange cliqué

    # Texte
    TEXT_PRIMARY = "#ffffff"     # Texte blanc
    TEXT_SECONDARY = "#b0b0b0"   # Texte gris
    TEXT_MUTED = "#808080"       # Texte atténué

    # États
    SUCCESS = "#4caf50"          # Vert succès
    WARNING = "#ff9800"          # Orange warning
    DANGER = "#f44336"           # Rouge danger
    INFO = "#2196f3"             # Bleu info

    # Bordures
    BORDER_COLOR = "#404040"     # Bordure normale
    BORDER_HOVER = "#606060"     # Bordure hover


# ============================================================================
# WIDGETS CUSTOMTKINTER COMPATIBLES
# ============================================================================

class ModernFrame(ctk.CTkFrame):
    """Frame CustomTkinter avec style NiTriTe"""

    def __init__(self, parent, corner_radius=0, **kwargs):
        # Convertir bg -> fg_color si présent
        if 'bg' in kwargs:
            kwargs['fg_color'] = kwargs.pop('bg')

        super().__init__(
            parent,
            corner_radius=corner_radius,
            fg_color=kwargs.get('fg_color', NiTriTeColors.BG_DARK),
            **{k: v for k, v in kwargs.items() if k != 'fg_color'}
        )


class ModernLabel(ctk.CTkLabel):
    """Label CustomTkinter avec style NiTriTe"""

    def __init__(self, parent, text="", **kwargs):
        # Convertir fg -> text_color et bg -> fg_color
        if 'fg' in kwargs:
            kwargs['text_color'] = kwargs.pop('fg')
        if 'bg' in kwargs:
            kwargs['fg_color'] = kwargs.pop('bg')

        super().__init__(
            parent,
            text=text,
            text_color=kwargs.get('text_color', NiTriTeColors.TEXT_PRIMARY),
            fg_color=kwargs.get('fg_color', "transparent"),
            **{k: v for k, v in kwargs.items() if k not in ['text_color', 'fg_color']}
        )


class ModernButton(ctk.CTkButton):
    """Button CustomTkinter avec style NiTriTe"""

    def __init__(self, parent, text="", command=None, **kwargs):
        # Convertir fg -> text_color et bg -> fg_color
        if 'fg' in kwargs:
            kwargs['text_color'] = kwargs.pop('fg')
        if 'bg' in kwargs:
            kwargs['fg_color'] = kwargs.pop('bg')

        super().__init__(
            parent,
            text=text,
            command=command,
            fg_color=kwargs.get('fg_color', NiTriTeColors.ORANGE_PRIMARY),
            hover_color=kwargs.get('hover_color', NiTriTeColors.ORANGE_HOVER),
            text_color=kwargs.get('text_color', NiTriTeColors.TEXT_PRIMARY),
            corner_radius=kwargs.get('corner_radius', 10),
            border_width=kwargs.get('border_width', 0),
            **{k: v for k, v in kwargs.items() if k not in [
                'fg_color', 'hover_color', 'text_color', 'corner_radius', 'border_width'
            ]}
        )


class ModernEntry(ctk.CTkEntry):
    """Entry CustomTkinter avec style NiTriTe"""

    def __init__(self, parent, **kwargs):
        # Convertir fg -> text_color et bg -> fg_color
        if 'fg' in kwargs:
            kwargs['text_color'] = kwargs.pop('fg')
        if 'bg' in kwargs:
            kwargs['fg_color'] = kwargs.pop('bg')

        super().__init__(
            parent,
            fg_color=kwargs.get('fg_color', NiTriTeColors.BG_CARD),
            text_color=kwargs.get('text_color', NiTriTeColors.TEXT_PRIMARY),
            border_color=kwargs.get('border_color', NiTriTeColors.BORDER_COLOR),
            corner_radius=kwargs.get('corner_radius', 10),
            **{k: v for k, v in kwargs.items() if k not in [
                'fg_color', 'text_color', 'border_color', 'corner_radius'
            ]}
        )


class ModernTextbox(ctk.CTkTextbox):
    """Textbox CustomTkinter avec style NiTriTe"""

    def __init__(self, parent, **kwargs):
        # Convertir fg -> text_color et bg -> fg_color
        if 'fg' in kwargs:
            kwargs['text_color'] = kwargs.pop('fg')
        if 'bg' in kwargs:
            kwargs['fg_color'] = kwargs.pop('bg')

        super().__init__(
            parent,
            fg_color=kwargs.get('fg_color', NiTriTeColors.BG_CARD),
            text_color=kwargs.get('text_color', NiTriTeColors.TEXT_PRIMARY),
            border_color=kwargs.get('border_color', NiTriTeColors.BORDER_COLOR),
            corner_radius=kwargs.get('corner_radius', 10),
            **{k: v for k, v in kwargs.items() if k not in [
                'fg_color', 'text_color', 'border_color', 'corner_radius'
            ]}
        )


class ModernProgressBar(ctk.CTkProgressBar):
    """ProgressBar CustomTkinter avec style NiTriTe"""

    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color=kwargs.get('fg_color', NiTriTeColors.BG_CARD),
            progress_color=kwargs.get('progress_color', NiTriTeColors.ORANGE_PRIMARY),
            corner_radius=kwargs.get('corner_radius', 10),
            **{k: v for k, v in kwargs.items() if k not in [
                'fg_color', 'progress_color', 'corner_radius'
            ]}
        )


# ============================================================================
# WIDGETS SPÉCIALISÉS
# ============================================================================

class CardFrame(ModernFrame):
    """Frame en forme de carte avec coins arrondis"""

    def __init__(self, parent, corner_radius=15, **kwargs):
        super().__init__(
            parent,
            corner_radius=corner_radius,
            fg_color=kwargs.get('fg_color', NiTriTeColors.BG_CARD),
            border_width=kwargs.get('border_width', 0),
            **{k: v for k, v in kwargs.items() if k not in ['fg_color', 'border_width']}
        )


class TitleLabel(ModernLabel):
    """Label de titre avec style prédéfini"""

    def __init__(self, parent, text="", size=20, **kwargs):
        super().__init__(
            parent,
            text=text,
            font=kwargs.get('font', ("Segoe UI", size, "bold")),
            text_color=kwargs.get('text_color', NiTriTeColors.TEXT_PRIMARY),
            **{k: v for k, v in kwargs.items() if k not in ['font', 'text_color']}
        )


class SuccessButton(ModernButton):
    """Bouton vert de succès"""

    def __init__(self, parent, text="", **kwargs):
        super().__init__(
            parent,
            text=text,
            fg_color=NiTriTeColors.SUCCESS,
            hover_color="#45a049",
            **kwargs
        )


class DangerButton(ModernButton):
    """Bouton rouge de danger"""

    def __init__(self, parent, text="", **kwargs):
        super().__init__(
            parent,
            text=text,
            fg_color=NiTriTeColors.DANGER,
            hover_color="#da190b",
            **kwargs
        )


class InfoButton(ModernButton):
    """Bouton bleu d'information"""

    def __init__(self, parent, text="", **kwargs):
        super().__init__(
            parent,
            text=text,
            fg_color=NiTriTeColors.INFO,
            hover_color="#0b7dda",
            **kwargs
        )


# ============================================================================
# UTILITAIRES
# ============================================================================

def create_hover_button(parent, text: str, command: Callable,
                       icon: Optional[str] = None) -> ModernButton:
    """
    Crée un bouton avec effet hover avancé

    Args:
        parent: Widget parent
        text: Texte du bouton
        command: Fonction à appeler
        icon: Icône optionnelle (emoji)

    Returns:
        ModernButton configuré
    """
    button_text = f"{icon} {text}" if icon else text

    return ModernButton(
        parent,
        text=button_text,
        command=command,
        corner_radius=10
    )


def create_info_card(parent, title: str, value: str,
                    icon: Optional[str] = None) -> CardFrame:
    """
    Crée une carte d'information

    Args:
        parent: Widget parent
        title: Titre de la carte
        value: Valeur à afficher
        icon: Icône optionnelle

    Returns:
        CardFrame avec contenu
    """
    card = CardFrame(parent, corner_radius=15)
    card.pack(fill="x", padx=10, pady=5)

    if icon:
        icon_label = ModernLabel(card, text=icon, font=("Segoe UI", 24))
        icon_label.pack(pady=(10, 0))

    title_label = TitleLabel(card, text=title, size=14)
    title_label.pack(pady=(5, 0))

    value_label = ModernLabel(
        card,
        text=value,
        font=("Segoe UI", 18, "bold"),
        text_color=NiTriTeColors.ORANGE_PRIMARY
    )
    value_label.pack(pady=(0, 10))

    return card
