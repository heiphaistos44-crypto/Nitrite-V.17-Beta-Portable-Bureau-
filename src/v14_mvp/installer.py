#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module d'Installation - NiTriTe V14
Gestion des installations via WinGet, Chocolatey et téléchargement direct
"""

import subprocess
import threading
from typing import Callable, Optional, List
import json
from pathlib import Path


class InstallationManager:
    """Gestionnaire d'installations"""
    
    def __init__(self):
        self.winget_available = self._check_winget()
        self.chocolatey_available = self._check_chocolatey()
        self.current_installations = []
        self.installation_queue = []
    
    def _check_winget(self) -> bool:
        """Vérifier si WinGet est disponible"""
        try:
            result = subprocess.run(
                ["winget", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def _check_chocolatey(self) -> bool:
        """Vérifier si Chocolatey est disponible"""
        try:
            result = subprocess.run(
                ["choco", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def install_app(
        self,
        app_name: str,
        package_id: Optional[str] = None,
        method: str = "winget",
        on_progress: Optional[Callable[[str, int], None]] = None,
        on_complete: Optional[Callable[[bool, str], None]] = None
    ):
        """
        Installer une application
        
        Args:
            app_name: Nom de l'application
            package_id: ID du package (WinGet ID, Choco ID, URL)
            method: "winget", "chocolatey" ou "download"
            on_progress: Callback (message, progress_percent)
            on_complete: Callback (success, message)
        """
        # Lancer installation dans un thread séparé
        thread = threading.Thread(
            target=self._install_app_thread,
            args=(app_name, package_id, method, on_progress, on_complete),
            daemon=True
        )
        thread.start()
    
    def _install_app_thread(
        self,
        app_name: str,
        package_id: Optional[str],
        method: str,
        on_progress: Optional[Callable],
        on_complete: Optional[Callable]
    ):
        """Thread d'installation"""
        try:
            if on_progress:
                on_progress(f"🔍 Recherche de {app_name}...", 10)
            
            if method == "winget":
                success, message = self._install_with_winget(
                    app_name, package_id, on_progress
                )
            elif method == "chocolatey":
                success, message = self._install_with_chocolatey(
                    app_name, package_id, on_progress
                )
            elif method == "download":
                success, message = self._install_with_download(
                    app_name, package_id, on_progress
                )
            else:
                success = False
                message = f"Méthode d'installation inconnue: {method}"
            
            if on_complete:
                on_complete(success, message)
        
        except Exception as e:
            if on_complete:
                on_complete(False, f"Erreur: {str(e)}")
    
    def _install_with_winget(
        self,
        app_name: str,
        package_id: Optional[str],
        on_progress: Optional[Callable]
    ) -> tuple[bool, str]:
        """Installation via WinGet"""
        if not self.winget_available:
            return False, "WinGet n'est pas disponible"
        
        try:
            # Utiliser package_id ou app_name pour la recherche
            search_term = package_id or app_name
            
            if on_progress:
                on_progress(f"📦 Installation via WinGet...", 30)
            
            # Commande WinGet
            cmd = [
                "winget", "install",
                "--id", search_term,
                "--silent",
                "--accept-source-agreements",
                "--accept-package-agreements"
            ]
            
            if on_progress:
                on_progress(f"⚙️ Exécution de l'installation...", 50)
            
            # Exécuter commande
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Attendre fin
            stdout, stderr = process.communicate()
            
            if on_progress:
                on_progress(f"✅ Finalisation...", 90)
            
            if process.returncode == 0:
                return True, f"✅ {app_name} installé avec succès"
            else:
                return False, f"❌ Échec installation: {stderr}"
        
        except Exception as e:
            return False, f"❌ Erreur WinGet: {str(e)}"
    
    def _install_with_chocolatey(
        self,
        app_name: str,
        package_id: Optional[str],
        on_progress: Optional[Callable]
    ) -> tuple[bool, str]:
        """Installation via Chocolatey"""
        if not self.chocolatey_available:
            return False, "Chocolatey n'est pas disponible"
        
        try:
            search_term = package_id or app_name
            
            if on_progress:
                on_progress(f"🍫 Installation via Chocolatey...", 30)
            
            cmd = [
                "choco", "install", search_term,
                "-y",
                "--no-progress"
            ]
            
            if on_progress:
                on_progress(f"⚙️ Exécution de l'installation...", 50)
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate()
            
            if on_progress:
                on_progress(f"✅ Finalisation...", 90)
            
            if process.returncode == 0:
                return True, f"✅ {app_name} installé avec succès"
            else:
                return False, f"❌ Échec installation: {stderr}"
        
        except Exception as e:
            return False, f"❌ Erreur Chocolatey: {str(e)}"
    
    def _install_with_download(
        self,
        app_name: str,
        url: Optional[str],
        on_progress: Optional[Callable]
    ) -> tuple[bool, str]:
        """Installation par téléchargement direct"""
        if not url:
            return False, "URL de téléchargement manquante"
        
        try:
            import urllib.request
            
            if on_progress:
                on_progress(f"🌐 Téléchargement depuis {url}...", 20)
            
            # Créer dossier downloads
            download_dir = Path("downloads")
            download_dir.mkdir(exist_ok=True)
            
            # Nom fichier
            filename = url.split("/")[-1]
            filepath = download_dir / filename
            
            if on_progress:
                on_progress(f"⬇️ Téléchargement en cours...", 50)
            
            # Télécharger
            urllib.request.urlretrieve(url, filepath)
            
            if on_progress:
                on_progress(f"✅ Téléchargé: {filename}", 80)
            
            # Exécuter installeur si .exe ou .msi
            if filename.endswith(('.exe', '.msi')):
                if on_progress:
                    on_progress(f"🚀 Lancement de l'installeur...", 90)
                
                subprocess.Popen([str(filepath)])
                return True, f"✅ Installeur lancé: {filename}"
            else:
                return True, f"✅ Fichier téléchargé: {filename}"
        
        except Exception as e:
            return False, f"❌ Erreur téléchargement: {str(e)}"
    
    def install_multiple(
        self,
        apps: List[tuple[str, Optional[str], str]],
        on_app_complete: Optional[Callable[[str, bool, str], None]] = None,
        on_all_complete: Optional[Callable[[int, int], None]] = None
    ):
        """
        Installer plusieurs applications
        
        Args:
            apps: Liste de (app_name, package_id, method)
            on_app_complete: Callback (app_name, success, message)
            on_all_complete: Callback (success_count, total_count)
        """
        def install_next(index: int, results: List[bool]):
            if index >= len(apps):
                # Toutes les apps traitées
                if on_all_complete:
                    success_count = sum(results)
                    on_all_complete(success_count, len(apps))
                return
            
            app_name, package_id, method = apps[index]
            
            def on_complete(success: bool, message: str):
                results.append(success)
                if on_app_complete:
                    on_app_complete(app_name, success, message)
                # Installer suivante
                install_next(index + 1, results)
            
            self.install_app(app_name, package_id, method, None, on_complete)
        
        # Démarrer installation séquentielle
        install_next(0, [])
    
    def search_winget(self, query: str) -> List[dict]:
        """Rechercher dans WinGet"""
        if not self.winget_available:
            return []
        
        try:
            result = subprocess.run(
                ["winget", "search", query, "--accept-source-agreements"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                # Parser résultat (simplifié)
                lines = result.stdout.split('\n')
                apps = []
                for line in lines[2:]:  # Skip headers
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 2:
                            apps.append({
                                'name': parts[0],
                                'id': parts[1] if len(parts) > 1 else parts[0],
                                'version': parts[2] if len(parts) > 2 else 'Unknown'
                            })
                return apps
            return []
        except:
            return []
    
    def get_installed_apps(self) -> List[dict]:
        """Obtenir liste des apps installées via WinGet"""
        if not self.winget_available:
            return []
        
        try:
            result = subprocess.run(
                ["winget", "list"],
                capture_output=True,
                text=True,
                timeout=15
            )
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                apps = []
                for line in lines[2:]:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 2:
                            apps.append({
                                'name': parts[0],
                                'version': parts[1] if len(parts) > 1 else 'Unknown'
                            })
                return apps
            return []
        except:
            return []


# Instance globale
installer = InstallationManager()