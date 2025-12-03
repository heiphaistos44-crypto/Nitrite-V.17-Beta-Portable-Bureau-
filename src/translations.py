#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Système de traduction pour NiTriTe V13.1
Support: Français, English
"""

TRANSLATIONS = {
    "fr": {
        # Navigation
        "applications": "Applications",
        "tools": "Outils Système",
        "master_install": "Master Installation",
        "updates": "Mises à Jour",
        "backup": "Backup & Restore",
        "optimizations": "Optimisations",
        "diagnostic": "Diagnostic",
        "settings": "Paramètres",

        # Navigation subtitles
        "applications_subtitle": "715 apps disponibles",
        "tools_subtitle": "553+ boutons utiles",
        "master_install_subtitle": "Installation rapide Windows",
        "updates_subtitle": "Détection & Updates",
        "backup_subtitle": "Sauvegarde système",
        "optimizations_subtitle": "Tweaks Windows",
        "diagnostic_subtitle": "Benchmark & Santé PC",
        "settings_subtitle": "Thèmes & Configuration",

        # Footer
        "footer_brand": "💼 OrdiPlus Tools\n🚀 Portable Edition",

        # Applications page
        "apps_available": "apps disponibles",
        "tools_available": "boutons utiles",
        "search_placeholder": "Rechercher...",
        "install_selected": "INSTALLER SÉLECTION",
        "select_all": "Tout sélectionner",
        "deselect_all": "Tout désélectionner",

        # Diagnostic page
        "pc_health_score": "Score de Santé PC",
        "system_info": "Informations Système",
        "current_performance": "Performance Actuelle",
        "benchmark": "Benchmark & Tests",
        "refresh": "Rafraîchir",
        "cpu": "CPU",
        "ram": "RAM",
        "disk": "Disque",
        "gpu": "Carte Graphique",
        "os_version": "Version OS",
        "processor": "Processeur",
        "graphics_card": "Carte Graphique",
        "disk_type": "Type de Disque",
        "excellent": "Excellent",
        "good": "Bon",
        "average": "Moyen",
        "poor": "Faible",

        # Settings page
        "settings_themes": "⚙️ Paramètres & Thèmes",
        "available_themes": "Thèmes disponibles",
        "preferences": "Préférences",
        "language": "Langue",
        "appearance": "Apparence",
        "dark_mode": "Mode Sombre",
        "light_mode": "Mode Clair",
        "french": "Français",
        "english": "English",
        "apply": "Appliquer",
        "save": "Sauvegarder",
        "cancel": "Annuler",

        # Settings sections
        "themes_title": "🎨 Thèmes",
        "language_title": "🌍 Langue / Language",
        "font_size_title": "🔤 Taille de police",
        "ui_scale_title": "📐 Échelle de l'interface",
        "appearance_title": "🎨 Apparence",
        "advanced_title": "⚙️ Paramètres avancés",

        # Settings labels
        "apply_font": "✓ Appliquer la taille de police",
        "apply_scale": "✓ Appliquer l'échelle",
        "apply_corner": "✓ Appliquer l'arrondi",
        "font_current": "Taille actuelle: {size}px",
        "font_selected": "Taille sélectionnée: {size}px",
        "scale_current": "Échelle actuelle: {scale}%",
        "scale_selected": "Échelle sélectionnée: {scale}%",
        "corner_radius_label": "Arrondi des bords",
        "corner_current": "Arrondi actuel: {value}px",
        "corner_selected": "Arrondi sélectionné: {value}px",
        "small": "Petit",
        "large": "Grand",

        # Toggle settings
        "animations_label": "Animations",
        "animations_on": "✓ Animations activées",
        "animations_off": "Animations désactivées",
        "smooth_scroll_label": "Défilement fluide",
        "smooth_scroll_on": "✓ Défilement fluide",
        "smooth_scroll_off": "Défilement normal",
        "notifications_label": "Notifications",
        "notifications_on": "✓ Notifications activées",
        "notifications_off": "Notifications désactivées",
        "auto_update_label": "Mise à jour auto",
        "auto_update_on": "✓ Mise à jour auto",
        "auto_update_off": "Manuelle",

        # Optimizations page
        "windows_optimizations": "Optimisations Windows",
        "privacy_telemetry": "Confidentialité & Télémétrie",
        "services_management": "Gestion des Services",
        "startup_management": "Gestion du Démarrage",
        "registry_cleanup": "Nettoyage du Registre",
        "disable_telemetry": "Désactiver Télémétrie",
        "disable_cortana": "Désactiver Cortana",
        "disable_tracking": "Désactiver Tracking",

        # Backup page
        "backup_restore": "Backup & Restauration",
        "create_restore_point": "Créer Point de Restauration",
        "backup_drivers": "Backup Drivers",
        "backup_app_list": "Sauvegarder Liste Apps",

        # Updates page
        "updates_checks": "Vérifications & Mises à Jour",
        "detect_apps": "Détecter Apps Installées",
        "check_updates": "Vérifier Updates",
        "generate_script": "Générer Script",

        # Master Windows
        "master_windows": "Master Windows",
        "quick_actions": "Actions Rapides",
        "system_info_cmd": "Informations Système",
        "windows_version": "Version Windows (winver)",
    },
    "en": {
        # Navigation
        "applications": "Applications",
        "tools": "System Tools",
        "master_install": "Master Installation",
        "updates": "Updates",
        "backup": "Backup & Restore",
        "optimizations": "Optimizations",
        "diagnostic": "Diagnostic",
        "settings": "Settings",

        # Navigation subtitles
        "applications_subtitle": "715 apps available",
        "tools_subtitle": "553+ useful buttons",
        "master_install_subtitle": "Quick Windows Installation",
        "updates_subtitle": "Detection & Updates",
        "backup_subtitle": "System Backup",
        "optimizations_subtitle": "Windows Tweaks",
        "diagnostic_subtitle": "Benchmark & PC Health",
        "settings_subtitle": "Themes & Configuration",

        # Footer
        "footer_brand": "💼 OrdiPlus Tools\n🚀 Portable Edition",

        # Applications page
        "apps_available": "apps available",
        "tools_available": "useful buttons",
        "search_placeholder": "Search...",
        "install_selected": "INSTALL SELECTION",
        "select_all": "Select All",
        "deselect_all": "Deselect All",

        # Diagnostic page
        "pc_health_score": "PC Health Score",
        "system_info": "System Information",
        "current_performance": "Current Performance",
        "benchmark": "Benchmark & Tests",
        "refresh": "Refresh",
        "cpu": "CPU",
        "ram": "RAM",
        "disk": "Disk",
        "gpu": "Graphics Card",
        "os_version": "OS Version",
        "processor": "Processor",
        "graphics_card": "Graphics Card",
        "disk_type": "Disk Type",
        "excellent": "Excellent",
        "good": "Good",
        "average": "Average",
        "poor": "Poor",

        # Settings page
        "settings_themes": "⚙️ Settings & Themes",
        "available_themes": "Available Themes",
        "preferences": "Preferences",
        "language": "Language",
        "appearance": "Appearance",
        "dark_mode": "Dark Mode",
        "light_mode": "Light Mode",
        "french": "Français",
        "english": "English",
        "apply": "Apply",
        "save": "Save",
        "cancel": "Cancel",

        # Settings sections
        "themes_title": "🎨 Themes",
        "language_title": "🌍 Language / Langue",
        "font_size_title": "🔤 Font Size",
        "ui_scale_title": "📐 Interface Scale",
        "appearance_title": "🎨 Appearance",
        "advanced_title": "⚙️ Advanced Settings",

        # Settings labels
        "apply_font": "✓ Apply Font Size",
        "apply_scale": "✓ Apply Scale",
        "apply_corner": "✓ Apply Radius",
        "font_current": "Current size: {size}px",
        "font_selected": "Selected size: {size}px",
        "scale_current": "Current scale: {scale}%",
        "scale_selected": "Selected scale: {scale}%",
        "corner_radius_label": "Corner Radius",
        "corner_current": "Current radius: {value}px",
        "corner_selected": "Selected radius: {value}px",
        "small": "Small",
        "large": "Large",

        # Toggle settings
        "animations_label": "Animations",
        "animations_on": "✓ Animations enabled",
        "animations_off": "Animations disabled",
        "smooth_scroll_label": "Smooth scrolling",
        "smooth_scroll_on": "✓ Smooth scrolling",
        "smooth_scroll_off": "Normal scrolling",
        "notifications_label": "Notifications",
        "notifications_on": "✓ Notifications enabled",
        "notifications_off": "Notifications disabled",
        "auto_update_label": "Auto update",
        "auto_update_on": "✓ Auto update",
        "auto_update_off": "Manual",

        # Optimizations page
        "windows_optimizations": "Windows Optimizations",
        "privacy_telemetry": "Privacy & Telemetry",
        "services_management": "Services Management",
        "startup_management": "Startup Management",
        "registry_cleanup": "Registry Cleanup",
        "disable_telemetry": "Disable Telemetry",
        "disable_cortana": "Disable Cortana",
        "disable_tracking": "Disable Tracking",

        # Backup page
        "backup_restore": "Backup & Restore",
        "create_restore_point": "Create Restore Point",
        "backup_drivers": "Backup Drivers",
        "backup_app_list": "Backup App List",

        # Updates page
        "updates_checks": "Updates & Checks",
        "detect_apps": "Detect Installed Apps",
        "check_updates": "Check Updates",
        "generate_script": "Generate Script",

        # Master Windows
        "master_windows": "Master Windows",
        "quick_actions": "Quick Actions",
        "system_info_cmd": "System Information",
        "windows_version": "Windows Version (winver)",
    }
}

# Langue par défaut
CURRENT_LANGUAGE = "fr"

def set_language(lang_code):
    """Définir la langue de l'application"""
    global CURRENT_LANGUAGE
    if lang_code in TRANSLATIONS:
        CURRENT_LANGUAGE = lang_code
        return True
    return False

def get_text(key):
    """Obtenir le texte traduit pour une clé"""
    return TRANSLATIONS.get(CURRENT_LANGUAGE, {}).get(key, key)

def _(key):
    """Alias court pour get_text()"""
    return get_text(key)
