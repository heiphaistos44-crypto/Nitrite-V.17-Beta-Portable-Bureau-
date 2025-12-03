#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de gestion sécurisée de l'affichage et logging
Évite les erreurs d'encodage Unicode sur Windows
"""

import sys
import io
import logging

# Configuration automatique de l'encodage UTF-8 sur Windows
if sys.platform == 'win32':
    # Wrapper stdout et stderr avec UTF-8
    if not isinstance(sys.stdout, io.TextIOWrapper) or sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    if not isinstance(sys.stderr, io.TextIOWrapper) or sys.stderr.encoding != 'utf-8':
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def safe_print(*args, **kwargs):
    """
    Version sécurisée de print() qui gère automatiquement l'encodage UTF-8
    Remplace les caractères non encodables par des alternatives ASCII
    """
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        # Fallback: convertir en ASCII safe
        safe_args = []
        for arg in args:
            if isinstance(arg, str):
                # Remplacer les emojis par des alternatives ASCII
                safe_str = (arg
                    .replace('✅', '[OK]')
                    .replace('⚠️', '[!]')
                    .replace('🔄', '[*]')
                    .replace('❌', '[X]')
                    .replace('ℹ️', '[i]')
                    .replace('✓', '[v]')
                    .replace('⭐', '[*]')
                    .replace('🔑', '[KEY]')
                    .replace('💾', '[DISK]')
                    .replace('⚡', '[>]')
                    .replace('📦', '[PKG]')
                    .replace('🛠️', '[TOOL]')
                    .replace('🚀', '[GO]')
                    .replace('💼', '[CASE]')
                    .replace('🌍', '[GLOBE]')
                    .replace('🔧', '[WRENCH]')
                    .replace('📁', '[FOLDER]')
                    .replace('🌐', '[WEB]')
                    .replace('💻', '[PC]')
                    .replace('🔍', '[SEARCH]')
                    .replace('📊', '[CHART]')
                    .replace('⚙️', '[GEAR]')
                    .replace('📋', '[CLIPBOARD]')
                    .replace('🪟', '[WINDOW]')
                    .replace('🔤', '[ABC]')
                    .replace('📐', '[RULER]')
                    .replace('🎨', '[PALETTE]')
                )
                safe_args.append(safe_str)
            else:
                safe_args.append(arg)
        print(*safe_args, **kwargs)


class SafeLogger:
    """
    Wrapper pour logging qui gère automatiquement l'encodage UTF-8
    """
    
    def __init__(self, logger):
        self.logger = logger
    
    def _safe_message(self, message):
        """Convertir un message en version ASCII-safe si nécessaire"""
        if isinstance(message, str):
            try:
                # Tester si le message est encodable
                message.encode(sys.stdout.encoding or 'utf-8')
                return message
            except (UnicodeEncodeError, AttributeError):
                # Remplacer les emojis par des alternatives ASCII
                return (message
                    .replace('✅', '[OK]')
                    .replace('⚠️', '[!]')
                    .replace('🔄', '[*]')
                    .replace('❌', '[X]')
                    .replace('ℹ️', '[i]')
                    .replace('✓', '[v]')
                    .replace('⭐', '[*]')
                    .replace('🔑', '[KEY]')
                    .replace('💾', '[DISK]')
                    .replace('⚡', '[>]')
                    .replace('📦', '[PKG]')
                    .replace('🛠️', '[TOOL]')
                    .replace('🚀', '[GO]')
                    .replace('💼', '[CASE]')
                    .replace('🌍', '[GLOBE]')
                    .replace('🔧', '[WRENCH]')
                    .replace('📁', '[FOLDER]')
                    .replace('🌐', '[WEB]')
                    .replace('💻', '[PC]')
                    .replace('🔍', '[SEARCH]')
                    .replace('📊', '[CHART]')
                    .replace('⚙️', '[GEAR]')
                    .replace('📋', '[CLIPBOARD]')
                    .replace('🪟', '[WINDOW]')
                    .replace('🔤', '[ABC]')
                    .replace('📐', '[RULER]')
                    .replace('🎨', '[PALETTE]')
                )
        return message
    
    def debug(self, message, *args, **kwargs):
        self.logger.debug(self._safe_message(message), *args, **kwargs)
    
    def info(self, message, *args, **kwargs):
        self.logger.info(self._safe_message(message), *args, **kwargs)
    
    def warning(self, message, *args, **kwargs):
        self.logger.warning(self._safe_message(message), *args, **kwargs)
    
    def error(self, message, *args, **kwargs):
        self.logger.error(self._safe_message(message), *args, **kwargs)
    
    def critical(self, message, *args, **kwargs):
        self.logger.critical(self._safe_message(message), *args, **kwargs)
    
    def exception(self, message, *args, **kwargs):
        self.logger.exception(self._safe_message(message), *args, **kwargs)


def get_safe_logger(name):
    """
    Obtenir un logger sécurisé qui gère automatiquement l'encodage UTF-8
    
    Usage:
        from safe_print import get_safe_logger
        logger = get_safe_logger(__name__)
        logger.info("Message avec emoji ✅")  # Fonctionne toujours
    """
    return SafeLogger(logging.getLogger(name))


# Export des fonctions principales
__all__ = ['safe_print', 'SafeLogger', 'get_safe_logger']