# 🔐 Audit de Sécurité - NiTriTe V13

## Date : 2024-11-24

---

## 📊 RÉSUMÉ EXÉCUTIF

### ✅ Points Forts
- ✅ UAC bypass nécessaire et correctement implémenté
- ✅ Isolation des scripts dans dossier dédié
- ✅ Logging des actions pour traçabilité
- ✅ Timeouts sur opérations critiques
- ✅ Gestion d'erreurs robuste

### ⚠️ Risques Identifiés
- 🔴 **CRITIQUE**: Exécution de scripts sans sandboxing (ligne 375-429, script_automation.py)
- 🟠 **ÉLEVÉ**: Pas de validation des entrées utilisateur avant exécution
- 🟠 **ÉLEVÉ**: Scripts stockés sans chiffrement
- 🟡 **MOYEN**: Élévation de privilèges automatique sans confirmation
- 🟡 **MOYEN**: Pas de limite sur la taille des scripts
- 🟢 **FAIBLE**: Logs non chiffrés

---

## 🔴 VULNÉRABILITÉS CRITIQUES

### 1. Exécution de Scripts Sans Sandboxing

**Fichier**: `src/script_automation.py:375-429`

**Problème**:
```python
def execute_script(self, script_id: str, output_callback: Optional[Callable] = None) -> Dict:
    # ...
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=300  # Aucune restriction sur les actions du script
    )
```

**Risque**:
- Scripts peuvent accéder à TOUS les fichiers système
- Scripts peuvent modifier le registre sans restriction
- Scripts peuvent installer des logiciels malveillants
- Scripts peuvent désactiver antivirus
- Scripts peuvent exfiltrer des données

**Impact**: 🔴 **CRITIQUE** - Exécution de code arbitraire avec privilèges admin

**Recommandations**:

#### Solution 1: Sandbox PowerShell (Recommandé pour production)
```powershell
# Créer une session restreinte PowerShell
$sessionConfig = New-PSSessionConfiguration -Name 'RestrictedSession' `
    -SessionType RestrictedRemoteServer `
    -LanguageMode RestrictedLanguage

# Exécuter le script dans la session
Invoke-Command -Session $session -FilePath $scriptPath
```

#### Solution 2: Whitelist de Commandes Autorisées
```python
ALLOWED_COMMANDS = {
    'powershell': [
        'Get-Process', 'Get-Service', 'Get-EventLog',
        'Stop-Process', 'Stop-Service', 'Restart-Service'
        # Liste exhaustive des commandes autorisées
    ],
    'batch': ['echo', 'dir', 'ipconfig', 'netstat'],
    'forbidden': [
        'Remove-Item', 'rm', 'del', 'format',  # Suppression
        'Set-ExecutionPolicy',  # Modification sécurité
        'Disable-WindowsOptionalFeature',  # Désactivation features
        'net user', 'net localgroup',  # Gestion utilisateurs
    ]
}

def validate_script(code: str, language: str) -> bool:
    """Valide que le script ne contient que des commandes autorisées"""
    # Vérifier chaque ligne du script
    for line in code.split('\n'):
        # Extraire la commande
        cmd = line.strip().split()[0] if line.strip() else ''

        # Vérifier contre forbidden list
        if any(forbidden in line for forbidden in ALLOWED_COMMANDS['forbidden']):
            raise SecurityError(f"Commande interdite détectée: {line}")

        # Vérifier contre whitelist si en mode strict
        if cmd and cmd not in ALLOWED_COMMANDS.get(language, []):
            raise SecurityError(f"Commande non autorisée: {cmd}")

    return True
```

#### Solution 3: Analyse Statique Avant Exécution
```python
def analyze_script_security(code: str) -> Dict:
    """Analyse statique du script pour détecter comportements dangereux"""
    warnings = []
    risks = []

    # Patterns dangereux
    DANGEROUS_PATTERNS = [
        r'Remove-Item.*-Recurse',  # Suppression récursive
        r'rm\s+-rf',  # Suppression forcée Unix-style
        r'Format-Volume',  # Formatage disque
        r'Invoke-WebRequest.*\|\s*Invoke-Expression',  # Download & execute
        r'Start-Process.*-Verb\s+RunAs',  # Nouvelle élévation
        r'Set-MpPreference.*-DisableRealtimeMonitoring',  # Désactiver antivirus
        r'Add-MpPreference.*-ExclusionPath',  # Exclure de l'antivirus
        r'New-Object.*Net\.WebClient',  # Download de fichiers
        r'Invoke-Expression',  # Exécution de code dynamique
        r'[Ss]tart-[Pp]rocess.*powershell',  # Spawn PowerShell
        r'reg\s+add',  # Modification registre
        r'schtasks\s+/create',  # Création tâches planifiées
    ]

    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, code, re.IGNORECASE):
            risks.append(f"⚠️ Pattern dangereux détecté: {pattern}")

    return {
        'safe': len(risks) == 0,
        'warnings': warnings,
        'risks': risks,
        'risk_level': 'HIGH' if len(risks) > 0 else 'LOW'
    }
```

---

### 2. Pas de Validation des Entrées Utilisateur

**Fichier**: `src/script_automation.py:253-305`

**Problème**:
```python
def create_script(self, name: str, code: str, language: str = 'powershell', ...):
    # AUCUNE validation du 'code' avant sauvegarde
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(code)  # ❌ Code non validé
```

**Risque**:
- Injection de code malveillant
- Scripts contenant des payloads cachés
- Noms de fichiers malformés causant des erreurs

**Recommandations**:

```python
import re
from pathlib import Path

def sanitize_script_name(name: str) -> str:
    """Nettoie le nom du script pour éviter path traversal"""
    # Retirer caractères spéciaux
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    # Limiter longueur
    name = name[:100]
    # Éviter noms réservés Windows
    reserved = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'LPT1']
    if name.upper() in reserved:
        name = f"script_{name}"
    return name

def validate_script_code(code: str, max_size: int = 1_000_000) -> bool:
    """Valide le code du script"""
    # Taille maximale (1 MB par défaut)
    if len(code.encode('utf-8')) > max_size:
        raise ValueError(f"Script trop volumineux (max {max_size} bytes)")

    # Vérifier encodage valide
    try:
        code.encode('utf-8')
    except UnicodeEncodeError:
        raise ValueError("Encodage du script invalide")

    # Analyser sécurité
    security_check = analyze_script_security(code)
    if not security_check['safe']:
        # Avertir l'utilisateur des risques
        return False, security_check['risks']

    return True, []

def create_script(self, name: str, code: str, language: str = 'powershell', ...):
    # ✅ VALIDATION
    name = sanitize_script_name(name)
    is_valid, risks = validate_script_code(code)

    if not is_valid:
        # Demander confirmation utilisateur
        if not user_confirms_risks(risks):
            raise SecurityError("Script rejeté par l'utilisateur")

    # Reste du code...
```

---

### 3. Scripts Non Chiffrés

**Fichier**: `src/script_automation.py:280-284`

**Problème**:
```python
# Scripts stockés en clair sur le disque
with open(script_file, 'w', encoding='utf-8') as f:
    f.write(code)  # ❌ Stockage non chiffré
```

**Risque**:
- Scripts contenant credentials lisibles par malware
- Reverse engineering facile
- Vol de propriété intellectuelle

**Recommandations**:

```python
from cryptography.fernet import Fernet
import base64
import hashlib

class SecureScriptStorage:
    """Stockage sécurisé des scripts avec chiffrement"""

    def __init__(self):
        # Générer clé à partir du hardware ID de la machine
        self.key = self._get_machine_key()
        self.cipher = Fernet(self.key)

    def _get_machine_key(self) -> bytes:
        """Génère une clé basée sur le hardware de la machine"""
        import subprocess
        # Utiliser UUID du système comme seed
        result = subprocess.run(
            ['wmic', 'csproduct', 'get', 'UUID'],
            capture_output=True, text=True
        )
        uuid = result.stdout.split('\n')[1].strip()

        # Dériver clé de chiffrement
        key = hashlib.sha256(uuid.encode()).digest()
        return base64.urlsafe_b64encode(key)

    def encrypt_script(self, code: str) -> bytes:
        """Chiffre le code du script"""
        return self.cipher.encrypt(code.encode('utf-8'))

    def decrypt_script(self, encrypted_code: bytes) -> str:
        """Déchiffre le code du script"""
        return self.cipher.decrypt(encrypted_code).decode('utf-8')

# Utilisation
storage = SecureScriptStorage()

def save_script(self, script_id: str, code: str):
    # Chiffrer avant sauvegarde
    encrypted = storage.encrypt_script(code)
    with open(script_file, 'wb') as f:  # Mode binaire
        f.write(encrypted)

def load_script(self, script_id: str) -> str:
    # Déchiffrer après lecture
    with open(script_file, 'rb') as f:
        encrypted = f.read()
    return storage.decrypt_script(encrypted)
```

---

## 🟠 VULNÉRABILITÉS ÉLEVÉES

### 4. Élévation Automatique Sans Confirmation

**Fichier**: `src/elevation_helper.py:42-73`

**Problème**:
```python
def auto_elevate_at_startup():
    if not is_admin():
        # Relance AUTOMATIQUEMENT avec admin
        ctypes.windll.shell32.ShellExecuteW(...)
        sys.exit(0)
```

**Risque**:
- L'utilisateur peut ne pas vouloir donner admin
- Popup UAC surprenant pour l'utilisateur
- Vecteur d'attaque si l'application est compromise

**Recommandations**:

```python
def auto_elevate_at_startup(ask_user: bool = True) -> bool:
    """
    Élève les privilèges avec confirmation optionnelle

    Args:
        ask_user: Si True, demande confirmation avant élévation
    """
    if not is_admin():
        if ask_user:
            # Afficher dialogue de confirmation
            response = messagebox.askyesno(
                "Privilèges Administrateur",
                "NiTriTe nécessite des privilèges administrateur pour:\n"
                "• Installer des applications\n"
                "• Exécuter des scripts système\n"
                "• Modifier les paramètres réseau\n\n"
                "Voulez-vous continuer avec élévation ?",
                icon='warning'
            )

            if not response:
                # Continuer en mode limité
                print("⚠️ Mode limité - Certaines fonctionnalités désactivées")
                return False

        # Élever après confirmation
        try:
            ctypes.windll.shell32.ShellExecuteW(...)
            sys.exit(0)
        except Exception as e:
            print(f"❌ Élévation échouée: {e}")
            return False

    return False
```

---

### 5. Scan Réseau Sans Limitation

**Fichier**: `src/network_manager.py:140-198`

**Problème**:
- Le scanner réseau peut être utilisé pour reconnaissance malveillante
- Pas de limitation du nombre d'hôtes scannés
- Pas de throttling (pourrait surcharger le réseau)

**Recommandations**:

```python
def scan_network(self, network: Optional[str] = None,
                 timeout: float = 0.5,
                 max_hosts: int = 255,
                 throttle_delay: float = 0.01,
                 progress_callback: Optional[Callable] = None) -> List[Dict]:
    """
    Scanner réseau avec limitations de sécurité

    Args:
        max_hosts: Nombre maximum d'hôtes à scanner
        throttle_delay: Délai entre chaque scan (en secondes)
    """
    # Limiter la plage de scan
    if ip_network(network).num_addresses > max_hosts:
        raise ValueError(f"Réseau trop large (max {max_hosts} hôtes)")

    # Vérifier si on scanne le réseau local uniquement
    if not self._is_private_network(network):
        raise SecurityError("Scan de réseaux publics interdit")

    results = []
    for ip in ip_network(network).hosts():
        # Throttling pour éviter surcharge
        time.sleep(throttle_delay)

        # Scanner l'hôte
        # ...

    return results

def _is_private_network(self, network: str) -> bool:
    """Vérifie si c'est un réseau privé (RFC 1918)"""
    net = ip_network(network)
    return net.is_private
```

---

## 🟡 VULNÉRABILITÉS MOYENNES

### 6. Logs Non Protégés

**Problème**: Les logs peuvent contenir des informations sensibles

**Recommandations**:

```python
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_secure_logging():
    """Configure un logging sécurisé"""
    log_file = Path.home() / "NiTriTe_Logs" / "app.log"
    log_file.parent.mkdir(exist_ok=True)

    # Permissions restrictives (Windows)
    os.chmod(log_file.parent, 0o700)

    # Handler avec rotation
    handler = RotatingFileHandler(
        log_file,
        maxBytes=10_000_000,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )

    # Format sans informations sensibles
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)

    # Filtrer les données sensibles
    class SensitiveDataFilter(logging.Filter):
        def filter(self, record):
            # Masquer patterns sensibles
            patterns = [
                (r'password=\S+', 'password=***'),
                (r'token=\S+', 'token=***'),
                (r'\d{3}-\d{2}-\d{4}', 'XXX-XX-XXXX'),  # SSN
            ]
            for pattern, replacement in patterns:
                record.msg = re.sub(pattern, replacement, str(record.msg))
            return True

    handler.addFilter(SensitiveDataFilter())

    logging.getLogger().addHandler(handler)
```

---

### 7. Pas de Vérification d'Intégrité

**Problème**: Fichiers de configuration peuvent être modifiés malicieusement

**Recommandations**:

```python
import hashlib
import json

class IntegrityChecker:
    """Vérification d'intégrité des fichiers critiques"""

    def __init__(self):
        self.hashes_file = Path("data") / ".integrity"
        self.hashes = self._load_hashes()

    def compute_hash(self, file_path: Path) -> str:
        """Calcule SHA-256 d'un fichier"""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for block in iter(lambda: f.read(4096), b''):
                sha256.update(block)
        return sha256.hexdigest()

    def verify_file(self, file_path: Path) -> bool:
        """Vérifie l'intégrité d'un fichier"""
        current_hash = self.compute_hash(file_path)
        expected_hash = self.hashes.get(str(file_path))

        if expected_hash is None:
            # Première vérification, enregistrer le hash
            self.hashes[str(file_path)] = current_hash
            self._save_hashes()
            return True

        if current_hash != expected_hash:
            logging.error(f"⚠️ Intégrité compromise: {file_path}")
            return False

        return True

    def verify_critical_files(self):
        """Vérifie tous les fichiers critiques au démarrage"""
        critical_files = [
            Path("data/programs.json"),
            Path("data/config.json"),
            Path("src/elevation_helper.py"),
        ]

        for file_path in critical_files:
            if not self.verify_file(file_path):
                raise SecurityError(
                    f"Fichier critique modifié: {file_path}\n"
                    "L'application va se fermer pour sécurité."
                )
```

---

## ✅ BONNES PRATIQUES DÉJÀ IMPLÉMENTÉES

### 1. Timeouts sur Opérations
```python
# ✅ BON
result = subprocess.run(cmd, timeout=300)
```

### 2. Gestion d'Erreurs
```python
# ✅ BON
try:
    # opération risquée
except Exception as e:
    self.logger.error(f"Erreur: {e}")
    return safe_default
```

### 3. Logging des Actions
```python
# ✅ BON
self.logger.info(f"Script créé: {name} ({script_id})")
```

---

## 🎯 PLAN D'ACTION RECOMMANDÉ

### Phase 1: Corrections Critiques (1-2 jours)
1. ✅ Implémenter validation des scripts avant exécution
2. ✅ Ajouter analyse statique de sécurité
3. ✅ Limiter les commandes autorisées

### Phase 2: Améliorations Élevées (3-4 jours)
4. ✅ Chiffrer le stockage des scripts
5. ✅ Ajouter confirmation avant élévation
6. ✅ Limiter les scans réseau

### Phase 3: Durcissement (5-7 jours)
7. ✅ Protéger les logs
8. ✅ Vérification d'intégrité des fichiers
9. ✅ Documentation sécurité pour utilisateurs
10. ✅ Audit de code complet par expert externe

---

## 📝 RECOMMANDATIONS POUR COMMERCIALISATION

### Avant Vente

1. **Signature de Code**
   - Obtenir certificat de signature de code
   - Signer tous les .exe et .dll
   - Évite les avertissements Windows Defender

2. **Documentation Sécurité**
   - Guide de déploiement sécurisé
   - Politiques de sécurité recommandées
   - Liste des privilèges requis

3. **Tests de Pénétration**
   - Faire auditer par un expert en sécurité
   - Tests d'injection de code
   - Tests d'élévation de privilèges

4. **Conformité**
   - RGPD si collecte de données
   - Clause de non-responsabilité claire
   - Conditions d'utilisation strictes

5. **Mise à Jour Automatique Sécurisée**
   - Updates signés cryptographiquement
   - Vérification d'intégrité avant installation
   - Rollback automatique en cas d'échec

---

## 🔒 CONCLUSION

### Niveau de Risque Actuel: 🟠 **ÉLEVÉ**

L'application est **fonctionnelle** mais présente des **risques de sécurité** qui doivent être corrigés avant commercialisation:

- 🔴 **Exécution de code arbitraire** sans sandbox
- 🟠 **Pas de validation** des entrées utilisateur
- 🟠 **Stockage non sécurisé** des scripts

### Niveau de Risque Après Corrections: 🟢 **ACCEPTABLE**

Avec les corrections recommandées:
- ✅ Sandbox ou whitelist des commandes
- ✅ Validation stricte des entrées
- ✅ Chiffrement du stockage
- ✅ Audit et signature de code

L'application sera **prête pour commercialisation** avec un niveau de sécurité professionnel.

---

**Audit réalisé le**: 24 novembre 2024
**Prochaine révision**: Après implémentation des corrections critiques
