"""
Système d'automation de scripts pour NiTriTe V13
Éditeur de scripts, templates, planificateur de tâches, macros
"""

import os
import json
import logging
import subprocess
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Callable, Tuple
import sched
import time
import re


class ScriptSecurityValidator:
    """Validateur de sécurité pour scripts"""

    # Patterns dangereux à détecter
    DANGEROUS_PATTERNS = [
        (r'Remove-Item.*-Recurse.*-Force', 'Suppression récursive dangereuse'),
        (r'rm\s+-rf', 'Suppression forcée dangereuse'),
        (r'Format-Volume', 'Formatage de disque'),
        (r'Invoke-WebRequest.*\|\s*(?:Invoke-Expression|iex)', 'Téléchargement et exécution'),
        (r'Set-MpPreference.*-DisableRealtimeMonitoring', 'Désactivation antivirus'),
        (r'Add-MpPreference.*-ExclusionPath', 'Exclusion antivirus'),
        (r'Invoke-Expression\s*\(', 'Exécution de code dynamique'),
        (r'iex\s+\(', 'Exécution de code dynamique'),
        (r'Start-Process.*powershell.*-WindowStyle\s+Hidden', 'Processus PowerShell caché'),
        (r'reg\s+delete', 'Suppression clé registre'),
        (r'Set-ExecutionPolicy\s+Bypass', 'Modification politique exécution'),
        (r'Disable-WindowsOptionalFeature', 'Désactivation fonctionnalité Windows'),
        (r'net\s+user.*\/add', 'Ajout utilisateur'),
        (r'net\s+localgroup.*administrators.*\/add', 'Ajout au groupe admin'),
        (r'bcdedit', 'Modification boot'),
        (r'wevtutil\s+cl', 'Effacement logs événements'),
    ]

    # Commandes interdites
    FORBIDDEN_COMMANDS = [
        'format', 'fdisk', 'diskpart',  # Formatage disques
        'cipher /w',  # Effacement sécurisé
        'takeown', 'icacls /reset',  # Prise de contrôle fichiers
    ]

    @classmethod
    def sanitize_script_name(cls, name: str) -> str:
        """Nettoie le nom du script"""
        # Retirer caractères spéciaux dangereux
        name = re.sub(r'[<>:"/\\|?*]', '', name)
        # Limiter longueur
        name = name[:100].strip()
        # Éviter noms réservés Windows
        reserved = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'LPT1', 'LPT2']
        if name.upper() in reserved:
            name = f"script_{name}"
        # S'assurer qu'il n'est pas vide
        if not name:
            name = "script_sans_nom"
        return name

    @classmethod
    def validate_script_code(cls, code: str, max_size: int = 1_000_000) -> Tuple[bool, List[str], str]:
        """
        Valide le code du script

        Returns:
            Tuple[bool, List[str], str]: (is_safe, warnings, risk_level)
        """
        warnings = []

        # Vérifier taille
        code_size = len(code.encode('utf-8'))
        if code_size > max_size:
            return False, [f"Script trop volumineux ({code_size} bytes, max {max_size})"], "CRITICAL"

        # Vérifier encodage
        try:
            code.encode('utf-8')
        except UnicodeEncodeError:
            return False, ["Encodage invalide"], "CRITICAL"

        # Vérifier patterns dangereux
        risk_level = "LOW"
        for pattern, description in cls.DANGEROUS_PATTERNS:
            matches = re.finditer(pattern, code, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                warnings.append(f"⚠️ {description}: {match.group()}")
                risk_level = "HIGH"

        # Vérifier commandes interdites
        for forbidden in cls.FORBIDDEN_COMMANDS:
            if re.search(rf'\b{re.escape(forbidden)}\b', code, re.IGNORECASE):
                warnings.append(f"🚫 Commande interdite: {forbidden}")
                risk_level = "CRITICAL"

        # Déterminer si sûr
        is_safe = risk_level in ["LOW", "MEDIUM"]

        return is_safe, warnings, risk_level

    @classmethod
    def analyze_script(cls, code: str, language: str) -> Dict:
        """Analyse complète de sécurité du script"""
        is_safe, warnings, risk_level = cls.validate_script_code(code)

        # Statistiques
        lines = code.split('\n')
        stats = {
            'lines': len(lines),
            'size_bytes': len(code.encode('utf-8')),
            'language': language,
        }

        return {
            'safe': is_safe,
            'risk_level': risk_level,
            'warnings': warnings,
            'stats': stats,
            'recommendation': 'OK' if is_safe else 'REVIEW_REQUIRED'
        }


class ScriptTemplate:
    """Templates de scripts prédéfinis"""

    TEMPLATES = {
        'maintenance_complete': {
            'name': 'Maintenance Complète',
            'description': 'Script de maintenance système complète',
            'language': 'powershell',
            'code': '''# Script de maintenance système complète
Write-Host "=== Maintenance Système Démarrée ===" -ForegroundColor Green

# 1. Nettoyage des fichiers temporaires
Write-Host "`n[1/5] Nettoyage fichiers temporaires..." -ForegroundColor Cyan
Remove-Item -Path "$env:TEMP\\*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "C:\\Windows\\Temp\\*" -Recurse -Force -ErrorAction SilentlyContinue

# 2. Nettoyage du cache DNS
Write-Host "`n[2/5] Nettoyage cache DNS..." -ForegroundColor Cyan
ipconfig /flushdns

# 3. Vérification du disque
Write-Host "`n[3/5] Vérification disque..." -ForegroundColor Cyan
chkdsk C: /scan

# 4. Analyse SFC
Write-Host "`n[4/5] Vérification fichiers système..." -ForegroundColor Cyan
sfc /scannow

# 5. Mise à jour Windows Update
Write-Host "`n[5/5] Recherche mises à jour..." -ForegroundColor Cyan
Start-Process "ms-settings:windowsupdate-action"

Write-Host "`n=== Maintenance Terminée ===" -ForegroundColor Green
'''
        },
        'backup_drivers': {
            'name': 'Sauvegarde Pilotes',
            'description': 'Exporte tous les pilotes installés',
            'language': 'powershell',
            'code': '''# Sauvegarde des pilotes
$BackupPath = "$env:USERPROFILE\\Desktop\\Drivers_Backup_$(Get-Date -Format 'yyyy-MM-dd')"
New-Item -ItemType Directory -Path $BackupPath -Force

Write-Host "Exportation des pilotes vers: $BackupPath" -ForegroundColor Green
Export-WindowsDriver -Online -Destination $BackupPath

Write-Host "`nSauvegarde terminée!" -ForegroundColor Green
'''
        },
        'network_reset': {
            'name': 'Réinitialisation Réseau',
            'description': 'Reset complet de la configuration réseau',
            'language': 'batch',
            'code': '''@echo off
echo === Réinitialisation Réseau ===
echo.

echo [1/6] Reset Winsock...
netsh winsock reset

echo [2/6] Reset IP...
netsh int ip reset

echo [3/6] Libération IP...
ipconfig /release

echo [4/6] Renouvellement IP...
ipconfig /renew

echo [5/6] Flush DNS...
ipconfig /flushdns

echo [6/6] Reset pare-feu...
netsh advfirewall reset

echo.
echo === Réinitialisation Terminée ===
echo REDÉMARRAGE RECOMMANDÉ
pause
'''
        },
        'disk_cleanup': {
            'name': 'Nettoyage Disque Avancé',
            'description': 'Nettoyage approfondi du disque',
            'language': 'powershell',
            'code': '''# Nettoyage disque avancé
Write-Host "=== Nettoyage Disque Avancé ===" -ForegroundColor Green

# Windows Update Cleanup
Write-Host "`n[1/7] Nettoyage Windows Update..." -ForegroundColor Cyan
Dism.exe /online /Cleanup-Image /StartComponentCleanup /ResetBase

# Temp files
Write-Host "`n[2/7] Fichiers temporaires..." -ForegroundColor Cyan
Remove-Item -Path "$env:TEMP\\*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "C:\\Windows\\Temp\\*" -Recurse -Force -ErrorAction SilentlyContinue

# Prefetch
Write-Host "`n[3/7] Prefetch..." -ForegroundColor Cyan
Remove-Item -Path "C:\\Windows\\Prefetch\\*" -Force -ErrorAction SilentlyContinue

# Error Reports
Write-Host "`n[4/7] Rapports d'erreurs..." -ForegroundColor Cyan
Remove-Item -Path "C:\\ProgramData\\Microsoft\\Windows\\WER\\*" -Recurse -Force -ErrorAction SilentlyContinue

# Delivery Optimization
Write-Host "`n[5/7] Cache Delivery Optimization..." -ForegroundColor Cyan
Remove-Item -Path "C:\\Windows\\SoftwareDistribution\\DeliveryOptimization\\*" -Recurse -Force -ErrorAction SilentlyContinue

# Thumbnails
Write-Host "`n[6/7] Cache miniatures..." -ForegroundColor Cyan
Remove-Item -Path "$env:LOCALAPPDATA\\Microsoft\\Windows\\Explorer\\thumbcache_*" -Force -ErrorAction SilentlyContinue

# Recycle Bin
Write-Host "`n[7/7] Corbeille..." -ForegroundColor Cyan
Clear-RecycleBin -Force -ErrorAction SilentlyContinue

Write-Host "`n=== Nettoyage Terminé ===" -ForegroundColor Green
'''
        },
        'system_info_export': {
            'name': 'Export Infos Système',
            'description': 'Exporte toutes les informations système',
            'language': 'powershell',
            'code': '''# Export informations système
$OutputPath = "$env:USERPROFILE\\Desktop\\SystemInfo_$(Get-Date -Format 'yyyy-MM-dd_HH-mm').txt"

Write-Host "Export des informations système..." -ForegroundColor Green

# Informations système
systeminfo > $OutputPath

# Liste des programmes installés
Add-Content -Path $OutputPath -Value "`n`n=== PROGRAMMES INSTALLÉS ==="
Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* |
    Select-Object DisplayName, DisplayVersion, Publisher |
    Format-Table -AutoSize >> $OutputPath

# Liste des drivers
Add-Content -Path $OutputPath -Value "`n`n=== DRIVERS ==="
Get-WindowsDriver -Online |
    Select-Object Driver, ClassName, ProviderName, Date, Version |
    Format-Table -AutoSize >> $OutputPath

# Liste des services
Add-Content -Path $OutputPath -Value "`n`n=== SERVICES ==="
Get-Service |
    Select-Object Name, DisplayName, Status, StartType |
    Format-Table -AutoSize >> $OutputPath

Write-Host "`nExport terminé: $OutputPath" -ForegroundColor Green
'''
        },
        'performance_optimization': {
            'name': 'Optimisation Performance',
            'description': 'Tweaks pour améliorer les performances',
            'language': 'powershell',
            'code': '''# Optimisation des performances
Write-Host "=== Optimisation Performance ===" -ForegroundColor Green

# Désactiver effets visuels
Write-Host "`n[1/5] Optimisation effets visuels..." -ForegroundColor Cyan
Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" -Name "VisualFXSetting" -Value 2

# Optimiser services
Write-Host "`n[2/5] Optimisation services..." -ForegroundColor Cyan
Stop-Service -Name "SysMain" -Force # Superfetch
Set-Service -Name "SysMain" -StartupType Disabled

# Désactiver Cortana
Write-Host "`n[3/5] Désactivation Cortana..." -ForegroundColor Cyan
Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search" -Name "AllowCortana" -Value 0

# Désactiver télémétrie
Write-Host "`n[4/5] Désactivation télémétrie..." -ForegroundColor Cyan
Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" -Name "AllowTelemetry" -Value 0

# Optimiser plan d'alimentation
Write-Host "`n[5/5] Plan d'alimentation haute performance..." -ForegroundColor Cyan
powercfg /setactive SCHEME_MIN

Write-Host "`n=== Optimisation Terminée ===" -ForegroundColor Green
Write-Host "REDÉMARRAGE RECOMMANDÉ" -ForegroundColor Yellow
'''
        }
    }

    @classmethod
    def get_all_templates(cls) -> Dict:
        """Retourne tous les templates"""
        return cls.TEMPLATES

    @classmethod
    def get_template(cls, template_id: str) -> Optional[Dict]:
        """Retourne un template spécifique"""
        return cls.TEMPLATES.get(template_id)


class ScriptManager:
    """Gestionnaire de scripts personnalisés"""

    def __init__(self, scripts_dir: Optional[Path] = None):
        self.logger = logging.getLogger(__name__)

        # Dossier de stockage des scripts
        if scripts_dir:
            self.scripts_dir = scripts_dir
        else:
            self.scripts_dir = Path.home() / "NiTriTe_Scripts"

        self.scripts_dir.mkdir(exist_ok=True)

        # Index des scripts
        self.index_file = self.scripts_dir / "scripts_index.json"
        self.scripts = self._load_index()

    def _load_index(self) -> Dict:
        """Charge l'index des scripts"""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Erreur chargement index: {e}")

        return {}

    def _save_index(self):
        """Sauvegarde l'index des scripts"""
        try:
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(self.scripts, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde index: {e}")

    def create_script(self, name: str, code: str, language: str = 'powershell',
                     description: str = '', tags: List[str] = None) -> str:
        """
        Crée un nouveau script avec validation de sécurité

        Args:
            name: Nom du script
            code: Code du script
            language: Langage (powershell, batch, python)
            description: Description
            tags: Tags pour catégorisation

        Returns:
            ID du script créé

        Raises:
            ValueError: Si le script contient du code dangereux
        """
        # ✅ SÉCURITÉ: Nettoyer le nom
        name = ScriptSecurityValidator.sanitize_script_name(name)

        # ✅ SÉCURITÉ: Valider le code
        is_safe, warnings, risk_level = ScriptSecurityValidator.validate_script_code(code)

        if not is_safe or risk_level == "CRITICAL":
            error_msg = "Script rejeté pour raisons de sécurité:\n" + "\n".join(warnings)
            self.logger.warning(f"Script rejeté: {name} - {risk_level}")
            raise ValueError(error_msg)

        # Avertir si risque élevé mais non critique
        if warnings:
            self.logger.warning(f"Script '{name}' créé avec avertissements: {warnings}")

        # Générer ID unique
        script_id = f"script_{int(datetime.now().timestamp())}"

        # Extension selon langage
        extensions = {
            'powershell': '.ps1',
            'batch': '.bat',
            'python': '.py'
        }
        ext = extensions.get(language, '.txt')

        # Créer fichier
        script_file = self.scripts_dir / f"{script_id}{ext}"

        try:
            with open(script_file, 'w', encoding='utf-8') as f:
                f.write(code)

            # Ajouter à l'index avec informations de sécurité
            self.scripts[script_id] = {
                'name': name,
                'description': description,
                'language': language,
                'file': str(script_file),
                'tags': tags or [],
                'created': datetime.now().isoformat(),
                'modified': datetime.now().isoformat(),
                'runs': 0,
                'security': {
                    'risk_level': risk_level,
                    'warnings': warnings,
                    'validated': True
                }
            }

            self._save_index()
            self.logger.info(f"Script créé: {name} ({script_id}) - Risque: {risk_level}")

            return script_id

        except Exception as e:
            self.logger.error(f"Erreur création script: {e}")
            raise

    def update_script(self, script_id: str, code: str):
        """Met à jour le code d'un script avec validation de sécurité"""
        if script_id not in self.scripts:
            raise ValueError(f"Script {script_id} non trouvé")

        # ✅ SÉCURITÉ: Valider le nouveau code
        is_safe, warnings, risk_level = ScriptSecurityValidator.validate_script_code(code)

        if not is_safe or risk_level == "CRITICAL":
            error_msg = "Mise à jour rejetée pour raisons de sécurité:\n" + "\n".join(warnings)
            self.logger.warning(f"Mise à jour script rejetée: {script_id} - {risk_level}")
            raise ValueError(error_msg)

        script_file = Path(self.scripts[script_id]['file'])

        try:
            with open(script_file, 'w', encoding='utf-8') as f:
                f.write(code)

            self.scripts[script_id]['modified'] = datetime.now().isoformat()
            # Mettre à jour les infos de sécurité
            self.scripts[script_id]['security'] = {
                'risk_level': risk_level,
                'warnings': warnings,
                'validated': True
            }
            self._save_index()

            self.logger.info(f"Script mis à jour: {script_id} - Risque: {risk_level}")
            if warnings:
                self.logger.warning(f"Avertissements: {warnings}")

        except Exception as e:
            self.logger.error(f"Erreur mise à jour script: {e}")
            raise

    def delete_script(self, script_id: str):
        """Supprime un script"""
        if script_id not in self.scripts:
            raise ValueError(f"Script {script_id} non trouvé")

        script_file = Path(self.scripts[script_id]['file'])

        try:
            if script_file.exists():
                script_file.unlink()

            del self.scripts[script_id]
            self._save_index()

            self.logger.info(f"Script supprimé: {script_id}")

        except Exception as e:
            self.logger.error(f"Erreur suppression script: {e}")
            raise

    def get_script(self, script_id: str) -> Dict:
        """Récupère les informations d'un script"""
        if script_id not in self.scripts:
            raise ValueError(f"Script {script_id} non trouvé")

        script_info = self.scripts[script_id].copy()

        # Charger le code
        try:
            with open(script_info['file'], 'r', encoding='utf-8') as f:
                script_info['code'] = f.read()
        except Exception as e:
            self.logger.error(f"Erreur lecture script: {e}")
            script_info['code'] = ""

        return script_info

    def get_all_scripts(self) -> List[Dict]:
        """Retourne tous les scripts"""
        scripts_list = []

        for script_id, info in self.scripts.items():
            script_data = info.copy()
            script_data['id'] = script_id
            scripts_list.append(script_data)

        return sorted(scripts_list, key=lambda x: x['created'], reverse=True)

    def execute_script(self, script_id: str, output_callback: Optional[Callable] = None) -> Dict:
        """
        Exécute un script avec validation de sécurité préalable

        Args:
            script_id: ID du script
            output_callback: Fonction appelée avec la sortie

        Returns:
            Résultat de l'exécution
        """
        script_info = self.get_script(script_id)

        try:
            # ✅ SÉCURITÉ: Re-valider le code avant exécution
            # (au cas où le fichier aurait été modifié manuellement)
            code = script_info.get('code', '')
            is_safe, warnings, risk_level = ScriptSecurityValidator.validate_script_code(code)

            if not is_safe or risk_level == "CRITICAL":
                error_msg = "Exécution refusée pour raisons de sécurité:\n" + "\n".join(warnings)
                self.logger.error(f"Exécution script refusée: {script_id} - {risk_level}")
                return {
                    'success': False,
                    'error': error_msg,
                    'security_blocked': True,
                    'risk_level': risk_level,
                    'executed_at': datetime.now().isoformat()
                }

            # Avertir si risque élevé
            if risk_level == "HIGH":
                self.logger.warning(f"Exécution script à risque élevé: {script_id}")

            # Commande selon langage
            if script_info['language'] == 'powershell':
                cmd = ['powershell', '-ExecutionPolicy', 'Bypass', '-File', script_info['file']]
            elif script_info['language'] == 'batch':
                cmd = [script_info['file']]
            elif script_info['language'] == 'python':
                cmd = ['python', script_info['file']]
            else:
                raise ValueError(f"Langage non supporté: {script_info['language']}")

            self.logger.info(f"Exécution script: {script_id} ({script_info.get('name', 'Sans nom')})")

            # Exécuter avec timeout de sécurité
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes max
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )

            # Callback avec sortie
            if output_callback:
                output_callback(result.stdout)

            # Incrémenter compteur
            self.scripts[script_id]['runs'] += 1
            self.scripts[script_id]['last_execution'] = datetime.now().isoformat()
            self._save_index()

            self.logger.info(f"Script terminé: {script_id} - Code retour: {result.returncode}")

            return {
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'security_blocked': False,
                'risk_level': risk_level,
                'executed_at': datetime.now().isoformat()
            }

        except subprocess.TimeoutExpired:
            self.logger.error(f"Timeout script: {script_id}")
            return {
                'success': False,
                'error': 'Timeout: Script a dépassé 5 minutes',
                'executed_at': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Erreur exécution script: {e}")
            return {
                'success': False,
                'error': str(e),
                'executed_at': datetime.now().isoformat()
            }


class TaskScheduler:
    """Planificateur de tâches pour automatisation"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.tasks = {}
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.is_running = False
        self.scheduler_thread = None

        # Fichier de persistance
        self.tasks_file = Path.home() / "NiTriTe_Scripts" / "scheduled_tasks.json"
        self._load_tasks()

    def _load_tasks(self):
        """Charge les tâches planifiées"""
        if self.tasks_file.exists():
            try:
                with open(self.tasks_file, 'r', encoding='utf-8') as f:
                    self.tasks = json.load(f)
                self.logger.info(f"{len(self.tasks)} tâches chargées")
            except Exception as e:
                self.logger.error(f"Erreur chargement tâches: {e}")

    def _save_tasks(self):
        """Sauvegarde les tâches"""
        try:
            self.tasks_file.parent.mkdir(exist_ok=True)
            with open(self.tasks_file, 'w', encoding='utf-8') as f:
                json.dump(self.tasks, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde tâches: {e}")

    def add_task(self, name: str, script_id: str, schedule_type: str,
                 schedule_value: str, enabled: bool = True) -> str:
        """
        Ajoute une tâche planifiée

        Args:
            name: Nom de la tâche
            script_id: ID du script à exécuter
            schedule_type: Type (daily, weekly, monthly, once, startup)
            schedule_value: Valeur (ex: "14:30" pour daily, "Monday,14:30" pour weekly)
            enabled: Activée ou non

        Returns:
            ID de la tâche
        """
        task_id = f"task_{int(datetime.now().timestamp())}"

        self.tasks[task_id] = {
            'name': name,
            'script_id': script_id,
            'schedule_type': schedule_type,
            'schedule_value': schedule_value,
            'enabled': enabled,
            'created': datetime.now().isoformat(),
            'last_run': None,
            'next_run': self._calculate_next_run(schedule_type, schedule_value),
            'runs': 0
        }

        self._save_tasks()
        self.logger.info(f"Tâche créée: {name} ({task_id})")

        return task_id

    def _calculate_next_run(self, schedule_type: str, schedule_value: str) -> str:
        """Calcule la prochaine exécution"""
        now = datetime.now()

        try:
            if schedule_type == 'daily':
                # Format: "HH:MM"
                hour, minute = map(int, schedule_value.split(':'))
                next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

                if next_run <= now:
                    next_run += timedelta(days=1)

            elif schedule_type == 'weekly':
                # Format: "Monday,HH:MM"
                day_name, time_str = schedule_value.split(',')
                hour, minute = map(int, time_str.split(':'))

                days = {
                    'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
                    'Friday': 4, 'Saturday': 5, 'Sunday': 6
                }
                target_day = days[day_name]

                next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                days_ahead = target_day - now.weekday()

                if days_ahead <= 0 or (days_ahead == 0 and next_run <= now):
                    days_ahead += 7

                next_run = next_run + timedelta(days=days_ahead)

            elif schedule_type == 'once':
                # Format: "YYYY-MM-DD HH:MM"
                next_run = datetime.strptime(schedule_value, '%Y-%m-%d %H:%M')

            else:
                return "N/A"

            return next_run.isoformat()

        except Exception as e:
            self.logger.error(f"Erreur calcul next_run: {e}")
            return "Error"

    def get_all_tasks(self) -> List[Dict]:
        """Retourne toutes les tâches"""
        tasks_list = []

        for task_id, info in self.tasks.items():
            task_data = info.copy()
            task_data['id'] = task_id
            tasks_list.append(task_data)

        return sorted(tasks_list, key=lambda x: x['created'], reverse=True)

    def toggle_task(self, task_id: str):
        """Active/désactive une tâche"""
        if task_id in self.tasks:
            self.tasks[task_id]['enabled'] = not self.tasks[task_id]['enabled']
            self._save_tasks()

    def delete_task(self, task_id: str):
        """Supprime une tâche"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            self._save_tasks()


# Test du module
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Test templates
    print("=== Templates Disponibles ===")
    for template_id, template in ScriptTemplate.get_all_templates().items():
        print(f"- {template['name']}: {template['description']}")

    # Test script manager
    print("\n=== Script Manager ===")
    manager = ScriptManager()

    # Créer un script de test
    test_code = "Write-Host 'Hello from NiTriTe!' -ForegroundColor Green"
    script_id = manager.create_script("Test Script", test_code, "powershell", "Script de test")
    print(f"Script créé: {script_id}")

    # Lister scripts
    scripts = manager.get_all_scripts()
    print(f"Total scripts: {len(scripts)}")
