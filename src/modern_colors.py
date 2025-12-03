#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NiTriTe V13.1 - Définition des couleurs et système Premium
Module séparé pour éviter les imports circulaires
"""

import os
import json
from datetime import datetime


class PremiumManager:
    """Gestionnaire de licence premium pour NiTriTe"""
    
    LICENSE_FILE = "config/license.json"
    
    # Types de licences
    LICENSE_FREE = "free"
    LICENSE_PRO = "pro"
    LICENSE_ENTERPRISE = "enterprise"
    
    # Fonctionnalités par licence
    FEATURES = {
        LICENSE_FREE: {
            "max_apps": 50,
            "max_tools": 100,
            "themes": ["Orange NiTriTe", "Bleu Nuit"],
            "backup": False,
            "remote_support": False,
            "priority_support": False,
            "custom_branding": False,
            "batch_install": False,
            "auto_update": False,
            "export_reports": False,
        },
        LICENSE_PRO: {
            "max_apps": -1,  # Illimité
            "max_tools": -1,  # Illimité
            "themes": "all",
            "backup": True,
            "remote_support": True,
            "priority_support": True,
            "custom_branding": False,
            "batch_install": True,
            "auto_update": True,
            "export_reports": True,
        },
        LICENSE_ENTERPRISE: {
            "max_apps": -1,
            "max_tools": -1,
            "themes": "all",
            "backup": True,
            "remote_support": True,
            "priority_support": True,
            "custom_branding": True,
            "batch_install": True,
            "auto_update": True,
            "export_reports": True,
            "api_access": True,
            "multi_device": True,
        },
    }
    
    _instance = None
    _license_type = LICENSE_FREE
    _license_key = None
    _expiry_date = None
    
    @classmethod
    def get_instance(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        self._load_license()
    
    def _load_license(self):
        """Charger la licence depuis le fichier"""
        try:
            if os.path.exists(self.LICENSE_FILE):
                with open(self.LICENSE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._license_key = data.get('key')
                    self._license_type = data.get('type', self.LICENSE_FREE)
                    expiry = data.get('expiry')
                    if expiry:
                        self._expiry_date = datetime.fromisoformat(expiry)
                        # Vérifier expiration
                        if datetime.now() > self._expiry_date:
                            self._license_type = self.LICENSE_FREE
        except Exception:
            self._license_type = self.LICENSE_FREE
    
    def _save_license(self):
        """Sauvegarder la licence"""
        try:
            os.makedirs(os.path.dirname(self.LICENSE_FILE), exist_ok=True)
            with open(self.LICENSE_FILE, 'w', encoding='utf-8') as f:
                json.dump({
                    'key': self._license_key,
                    'type': self._license_type,
                    'expiry': self._expiry_date.isoformat() if self._expiry_date else None
                }, f, indent=2)
        except Exception:
            pass
    
    def activate_license(self, license_key: str) -> tuple:
        """Activer une licence avec une clé"""
        # Simulation de validation de licence
        # Dans une version réelle, cela ferait un appel API
        if license_key.startswith("NITRITE-PRO-"):
            self._license_type = self.LICENSE_PRO
            self._license_key = license_key
            self._expiry_date = datetime(2026, 12, 31)
            self._save_license()
            return True, "Licence Pro activée avec succès !"
        elif license_key.startswith("NITRITE-ENT-"):
            self._license_type = self.LICENSE_ENTERPRISE
            self._license_key = license_key
            self._expiry_date = datetime(2026, 12, 31)
            self._save_license()
            return True, "Licence Enterprise activée avec succès !"
        else:
            return False, "Clé de licence invalide"
    
    def is_premium(self) -> bool:
        """Vérifier si l'utilisateur a une licence premium"""
        return self._license_type in [self.LICENSE_PRO, self.LICENSE_ENTERPRISE]
    
    def is_enterprise(self) -> bool:
        """Vérifier si l'utilisateur a une licence enterprise"""
        return self._license_type == self.LICENSE_ENTERPRISE
    
    def get_license_type(self) -> str:
        """Obtenir le type de licence"""
        return self._license_type
    
    def get_license_name(self) -> str:
        """Obtenir le nom de la licence"""
        names = {
            self.LICENSE_FREE: "Version Gratuite",
            self.LICENSE_PRO: "Version Pro",
            self.LICENSE_ENTERPRISE: "Version Enterprise"
        }
        return names.get(self._license_type, "Inconnu")
    
    def has_feature(self, feature: str) -> bool:
        """Vérifier si une fonctionnalité est disponible"""
        features = self.FEATURES.get(self._license_type, {})
        return features.get(feature, False)
    
    def get_max_apps(self) -> int:
        """Obtenir le nombre maximum d'applications"""
        features = self.FEATURES.get(self._license_type, {})
        return features.get('max_apps', 50)
    
    def get_available_themes(self) -> list:
        """Obtenir les thèmes disponibles"""
        features = self.FEATURES.get(self._license_type, {})
        themes = features.get('themes', [])
        if themes == "all":
            return None  # Tous les thèmes
        return themes


class ModernColors:
    """Palette de couleurs moderne Noir & Orange Premium - Alignée sur la version web"""
    # Backgrounds (matching web version)
    BG_DARK = "#1a1a1a"  # Primary background (--bg-primary)
    BG_MEDIUM = "#2d2d2d"  # Secondary background (--bg-secondary)
    BG_LIGHT = "#3a3a3a"  # Tertiary background (--bg-tertiary)
    BG_CARD = "#252525"  # Card background (--bg-card)
    BG_HOVER = "#333333"  # Hover state (--bg-hover)

    # Orange accents (matching web version)
    ORANGE_PRIMARY = "#FF6B35"  # Primary orange (--primary-color)
    ORANGE_LIGHT = "#FF8C5A"  # Light orange (--primary-light)
    ORANGE_DARK = "#E85A28"  # Dark orange (--primary-dark)
    ORANGE_GLOW = "#FF6B35"  # Glow effect
    ORANGE_SECONDARY = "#F7931E"  # Secondary orange (--secondary-color)
    ORANGE_HOVER = "#ff8555"  # Hover state
    ORANGE_PRESSED = "#e55525"  # Pressed state
    ORANGE_WARNING = "#ff9800"  # Warning orange

    # Textes (matching web version)
    TEXT_PRIMARY = "#ffffff"  # Primary text (--text-primary)
    TEXT_SECONDARY = "#b0b0b0"  # Secondary text (--text-secondary)
    TEXT_MUTED = "#808080"  # Tertiary text (--text-tertiary)

    # Borders (matching web version)
    BORDER_COLOR = "#404040"  # Primary border (--border-color)
    BORDER_LIGHT = "#505050"  # Light border (--border-light)

    # Accents (matching web version)
    GREEN_SUCCESS = "#4CAF50"  # Success color (--success-color)
    RED_ERROR = "#F44336"  # Error color (--error-color)
    RED_DANGER = "#f44336"  # Danger color (alias)
    BLUE_INFO = "#2196F3"  # Info color
    PURPLE_PREMIUM = "#9C27B0"  # Premium color
    YELLOW_WARNING = "#FFA726"  # Warning color (--warning-color)
    
    # Premium colors
    GOLD_PREMIUM = "#FFD700"  # Gold for premium features
    GRADIENT_START = "#FF6B35"
    GRADIENT_END = "#FF8C5A"

    # Borders (additional)
    BORDER_HOVER = "#606060"  # Border hover state


# Global corner radius setting (can be modified at runtime)
CORNER_RADIUS = 15


def set_corner_radius(radius):
    """Set the global corner radius value"""
    global CORNER_RADIUS
    CORNER_RADIUS = int(radius)


def get_corner_radius():
    """Get the current global corner radius value"""
    return CORNER_RADIUS


def bind_mousewheel(canvas, scrollable_frame):
    """
    Bind mousewheel to canvas for smooth scrolling.
    Activates when mouse enters the area and deactivates when it leaves.
    Version améliorée avec gestion des erreurs
    """
    def on_mousewheel(event):
        try:
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except:
            pass

    def bound_to_mousewheel(event):
        try:
            canvas.bind_all("<MouseWheel>", on_mousewheel)
        except:
            pass

    def unbound_to_mousewheel(event):
        try:
            canvas.unbind_all("<MouseWheel>")
        except:
            pass

    # Bind sur le canvas et le frame scrollable
    try:
        canvas.bind('<Enter>', bound_to_mousewheel)
        canvas.bind('<Leave>', unbound_to_mousewheel)
        scrollable_frame.bind('<Enter>', bound_to_mousewheel)
        scrollable_frame.bind('<Leave>', unbound_to_mousewheel)
    except:
        pass


def get_premium_badge_color():
    """Obtenir la couleur du badge premium selon le niveau de licence"""
    pm = PremiumManager.get_instance()
    if pm.is_enterprise():
        return ModernColors.GOLD_PREMIUM
    elif pm.is_premium():
        return ModernColors.PURPLE_PREMIUM
    return ModernColors.TEXT_MUTED
