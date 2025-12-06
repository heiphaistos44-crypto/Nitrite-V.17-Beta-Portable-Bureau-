#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Design System - NiTriTe V17 Beta
Système de design moderne avec tokens réutilisables
"""

class DesignTokens:
    """Tokens de design - Material Design 3 inspired"""
    
    # === COULEURS ===
    # Surfaces
    BG_PRIMARY = "#0a0a0a"      # Noir profond
    BG_SECONDARY = "#151515"     # Gris très foncé
    BG_TERTIARY = "#202020"      # Gris foncé
    BG_ELEVATED = "#252525"      # Cartes surélevées
    BG_HOVER = "#2a2a2a"         # Hover state
    
    # Accent Orange
    ACCENT_PRIMARY = "#ff6b35"   # Orange principal
    ACCENT_HOVER = "#ff8555"     # Orange hover
    ACCENT_PRESSED = "#ff5020"   # Orange pressed
    ACCENT_SUBTLE = "#ff6b3520"  # Orange transparent
    
    # Texte
    TEXT_PRIMARY = "#ffffff"     # Blanc pur
    TEXT_SECONDARY = "#b0b0b0"   # Gris clair
    TEXT_TERTIARY = "#808080"    # Gris moyen
    TEXT_DISABLED = "#4a4a4a"    # Gris foncé
    
    # Sémantique
    SUCCESS = "#4caf50"          # Vert
    WARNING = "#ff9800"          # Orange foncé
    ERROR = "#f44336"            # Rouge
    INFO = "#2196f3"             # Bleu
    
    # Bordures
    BORDER_DEFAULT = "#2a2a2a"
    BORDER_FOCUS = "#ff6b35"
    BORDER_ERROR = "#f44336"
    
    # === ESPACEMENTS ===
    SPACING_XS = 4
    SPACING_SM = 8
    SPACING_MD = 16
    SPACING_LG = 24
    SPACING_XL = 32
    
    # === BORDURES ARRONDIES ===
    RADIUS_SM = 8
    RADIUS_MD = 16
    RADIUS_LG = 24
    RADIUS_FULL = 9999
    
    # === TYPOGRAPHIE ===
    FONT_FAMILY = "Segoe UI"
    FONT_SIZE_XS = 10
    FONT_SIZE_SM = 11
    FONT_SIZE_MD = 13
    FONT_SIZE_LG = 16
    FONT_SIZE_XL = 20
    FONT_SIZE_2XL = 24
    
    # === ANIMATIONS ===
    TRANSITION_FAST = 150
    TRANSITION_NORMAL = 300
    TRANSITION_SLOW = 500


class ModernColors:
    """Alias pour compatibilité avec ancien code"""
    BG_DARK = DesignTokens.BG_PRIMARY
    BG_MEDIUM = DesignTokens.BG_SECONDARY
    BG_LIGHT = DesignTokens.BG_TERTIARY
    BG_CARD = DesignTokens.BG_ELEVATED
    BG_HOVER = DesignTokens.BG_HOVER
    
    ORANGE_PRIMARY = DesignTokens.ACCENT_PRIMARY
    ORANGE_HOVER = DesignTokens.ACCENT_HOVER
    ORANGE_DARK = DesignTokens.ACCENT_PRESSED
    ORANGE_LIGHT = DesignTokens.ACCENT_SUBTLE
    
    TEXT_PRIMARY = DesignTokens.TEXT_PRIMARY
    TEXT_SECONDARY = DesignTokens.TEXT_SECONDARY
    TEXT_MUTED = DesignTokens.TEXT_TERTIARY
    
    GREEN_SUCCESS = DesignTokens.SUCCESS
    YELLOW_WARNING = DesignTokens.WARNING
    ORANGE_WARNING = DesignTokens.WARNING
    RED_ERROR = DesignTokens.ERROR
    RED_DANGER = DesignTokens.ERROR
    BLUE_INFO = DesignTokens.INFO
    
    BORDER_COLOR = DesignTokens.BORDER_DEFAULT
    BORDER_HOVER = DesignTokens.BORDER_FOCUS
    
    PURPLE_PREMIUM = "#9c27b0"  # Ajout pour compatibilité