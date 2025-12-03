#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NiTriTe V13.0 - Lanceur Principal
Interface Moderne pour Techniciens de Maintenance Informatique
Version corrigée avec gestion propre du démarrage
"""

import sys
import os
import threading

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import élévation automatique (DOIT être importé en premier)
from elevation_helper import auto_elevate_at_startup

# Auto-élévation au démarrage (UAC bypass)
if auto_elevate_at_startup():
    # Le programme a été relancé avec élévation, terminer cette instance
    sys.exit(0)


def launch_with_splash():
    """Launch application with splash screen - Version améliorée"""
    from splash_screen import SplashScreen
    from gui_modern_v13 import main as launch_main_app
    
    try:
        # Create splash screen
        splash = SplashScreen()
        splash.show()

        # Run loading sequence with callback to main app
        splash.run_loading_sequence(callback=launch_main_app)

        # Start splash mainloop (will end when loading finishes)
        splash.mainloop()
        
    except Exception as e:
        print(f"Erreur lors du démarrage avec splash screen: {e}")
        # Fallback: lancer directement l'application sans splash
        try:
            launch_main_app()
        except Exception as e2:
            print(f"Erreur fatale: {e2}")
            sys.exit(1)


def launch_direct():
    """Launch application directly without splash screen"""
    from gui_modern_v13 import main
    main()


if __name__ == "__main__":
    # Vérifier les arguments de ligne de commande
    if "--no-splash" in sys.argv:
        launch_direct()
    else:
        launch_with_splash()
    
    # Exit proprement
    sys.exit(0)
