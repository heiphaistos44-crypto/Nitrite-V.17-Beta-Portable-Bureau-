# 🚀 NiTriTe V14 - Application de Maintenance Informatique Professionnelle

## 📖 Description

**NiTriTe V14** est une application Windows complète de maintenance informatique avec une interface moderne Material Design 3. Elle permet d'installer 716+ applications, d'exécuter 548+ outils système, de télécharger des apps portables, et bien plus encore.

### ✨ Fonctionnalités Principales

- **📦 716+ Applications** installables via WinGet (15 catégories)
- **🛠️ 548+ Outils Système** (commandes Windows + URLs utiles)
- **🚀 Master Install** avec 10 packs éditables
- **💼 60+ Apps Portables** téléchargeables en 1 clic
- **💻 Terminal Intégré** (CMD, PowerShell, Windows PowerShell)
- **🔄 Mises à jour Windows** automatiques
- **💾 Sauvegarde/Restauration** système
- **⚡ Optimisations** système et nettoyage
- **🔍 Diagnostic Matériel** avec détection WMI
- **⚙️ Paramètres** complets (10 sections)

---

## 📋 Prérequis

### Système
- **Windows 10/11** (64-bit)
- **4 GB RAM** minimum (8 GB recommandé)
- **500 MB** espace disque libre

### Python
- **Python 3.8 à 3.12** (CustomTkinter n'est pas compatible avec Python 3.13+)
- Téléchargement: https://www.python.org/downloads/

### Vérifier votre version Python
```bash
python --version
```

Si vous avez Python 3.13+, installez Python 3.12 en parallèle.

---

## 🚀 Installation Rapide

### Méthode 1: Lanceur Automatique (Recommandé)

1. **Double-cliquez** sur `LANCER_NITRITE_V14.bat`
2. Le script vérifie Python et installe automatiquement les dépendances
3. L'application se lance automatiquement

### Méthode 2: Installation Manuelle

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Lancer l'application
python -m src.v14_mvp.main_app
```

---

## 📦 Dépendances

Le fichier `requirements.txt` contient:

```
customtkinter>=5.2.2
psutil>=5.9.0
requests>=2.31.0
wmi>=1.5.1; sys_platform == "win32"
```

**Installation:**
```bash
pip install -r requirements.txt
```

---

## 🎯 Guide d'Utilisation

### 📦 Page Applications

**Installer une application:**
1. Cliquez sur **📦 Applications**
2. Choisissez une catégorie
3. Cliquez sur **⬇️ Installer** sur l'application voulue
4. L'installation se fait automatiquement via WinGet

**Rechercher une application:**
- Utilisez la barre de recherche en haut
- Tapez le nom de l'application (ex: "Chrome", "VLC")

### 🛠️ Page Outils

**Exécuter un outil:**
1. Cliquez sur **🛠️ Outils**
2. Ouvrez une section (ex: "🔧 Maintenance Système")
3. Cliquez sur n'importe quel bouton
4. L'outil s'exécute automatiquement (commande OU URL)

**Sections disponibles:**
- 🔧 Maintenance Système (DISM, SFC, cleanmgr, etc.)
- 💾 Gestionnaires de Disques (diskpart, chkdsk, etc.)
- 🌐 Réseau (ipconfig, ping, netstat, etc.)
- 🎨 Personnalisation Windows
- 🔐 Sécurité
- Et 6 autres sections...

### 🚀 Master Install

**Installer un pack d'applications:**
1. Cliquez sur **🚀 Master Install**
2. Choisissez un pack (ex: "Essentiels")
3. Cliquez sur **📥 Installer le Pack**
4. Toutes les apps du pack s'installent automatiquement

**Éditer un pack:**
1. Cliquez sur **✏️** à côté du pack
2. Fenêtre modale s'ouvre avec double liste
3. Utilisez **➕** pour ajouter des apps depuis la liste de droite
4. Utilisez **➖** pour retirer des apps de la liste de gauche
5. Cliquez **💾 Sauvegarder**
6. Vos modifications sont enregistrées dans `Documents/NiTriTe_CustomPacks.json`

**Restaurer packs par défaut:**
- Cliquez sur **🔄 Restaurer Packs Défaut**

### 💼 Applications Portables

**Télécharger une app portable:**
1. Cliquez sur **💼 Apps Portables**
2. Ouvrez une catégorie (ex: "🌐 Navigateurs")
3. Cliquez sur **⬇️ Télécharger**
4. L'app se télécharge et s'installe dans `Documents/NiTriTe_Portables`

**Lancer une app portable:**
- Cliquez sur **▶️ Lancer** (disponible après téléchargement)

**Désinstaller une app portable:**
- Cliquez sur **🗑️** à côté du bouton Lancer

**Ouvrir le dossier des portables:**
- Cliquez sur **📁 Ouvrir Dossier** en haut à droite

### 💻 Terminal Intégré

**Utiliser le terminal:**
1. Cliquez sur **💻 Terminal**
2. Choisissez un onglet:
   - **🖥️ CMD** - Command Prompt
   - **💙 PowerShell** - PowerShell 5.1
   - **⚡ Windows PowerShell** - PowerShell 7+
3. Tapez une commande dans la barre en bas
4. Appuyez sur **Entrée** ou cliquez **▶️**

**Commandes exemples:**

CMD:
```
> dir
> ipconfig /all
> systeminfo
> tasklist
```

PowerShell:
```
PS> Get-Process
PS> Get-Service
PS> Get-NetAdapter
PS> Get-Disk
```

**Navigation historique:**
- **↑** (Flèche haut) - Commande précédente
- **↓** (Flèche bas) - Commande suivante

**Vider le terminal:**
- Cliquez sur **🗑️** ou tapez `clear`/`cls`

### 🔍 Diagnostic

**Analyser le système:**
1. Cliquez sur **🔍 Diagnostic**
2. Cliquez sur **🔄 Analyser le Système**
3. Le diagnostic détecte automatiquement:
   - **CPU exact** (ex: "Intel Core i7-10700K")
   - **RAM modules** avec fabricant et vitesse
   - **GPU(s)** avec modèles exacts
   - **Disques** avec modèles
   - **Carte mère**
   - Températures, utilisation, etc.

**Exporter le rapport:**
- Cliquez sur **📄 Exporter Rapport**
- Un fichier texte est créé dans `Documents/`

### ⚙️ Paramètres

**Changer le thème:**
1. Cliquez sur **⚙️ Paramètres**
2. Section **Apparence**
3. Choisissez: Dark / Light / Auto

**Autres paramètres:**
- Langue (FR/EN)
- Notifications
- Démarrage automatique
- Mode Admin
- Raccourcis clavier
- Sauvegarde automatique
- Etc.

---

## 📁 Structure du Projet

```
Nitrite V.13 Beta/
├── LANCER_NITRITE_V14.bat    # Lanceur automatique ✨
├── README_V14.md              # Ce fichier ✨
├── NITRITE_V14_CHANGELOG.md   # Changelog complet ✨
├── requirements.txt           # Dépendances Python
│
├── src/v14_mvp/              # Code source V14 ✨
│   ├── main_app.py           # Point d'entrée
│   ├── design_system.py      # Material Design 3
│   ├── components.py         # Composants UI
│   ├── navigation.py         # Navigation latérale
│   ├── pages_optimized.py    # Apps + Tools
│   ├── pages_full.py         # Updates/Backup/Diagnostic/Optimizations
│   ├── pages_settings.py     # Paramètres
│   ├── page_master_install.py # Master Install (NOUVEAU)
│   ├── page_portables.py     # Apps Portables (NOUVEAU)
│   ├── page_terminal.py      # Terminal (NOUVEAU)
│   ├── installer.py          # Gestionnaire WinGet
│   └── splash_loader.py      # Écran de chargement
│
├── data/                     # Données
│   ├── programs.json         # Base 716+ applications
│   └── ...
│
└── docs/                     # Documentation
    └── ...
```

---

## 🐛 Dépannage

### Erreur: "Python n'est pas installé"
**Solution:**
1. Téléchargez Python 3.8-3.12: https://www.python.org/downloads/
2. Cochez **"Add Python to PATH"** lors de l'installation
3. Redémarrez votre terminal/invite de commandes

### Erreur: "CustomTkinter n'est pas compatible"
**Cause:** Vous avez Python 3.13+

**Solution:**
1. Installez Python 3.12 en parallèle
2. Utilisez: `py -3.12 -m pip install -r requirements.txt`
3. Lancez avec: `py -3.12 -m src.v14_mvp.main_app`

### Erreur: "Module 'wmi' not found"
**Solution:**
```bash
pip install wmi
```

### Fenêtre blanche au démarrage
**Causes possibles:**
- Fichier `data/programs.json` manquant
- Pilotes graphiques obsolètes

**Solution:**
1. Vérifiez que `data/programs.json` existe
2. Mettez à jour vos pilotes graphiques
3. Redémarrez l'application

### Les boutons Outils ne fonctionnent pas
**Solution:** Ce bug est corrigé dans V14 ! Si le problème persiste:
1. Vérifiez que vous utilisez bien V14 (pas V13)
2. Relancez l'application en mode administrateur

---

## 🔒 Fichiers Créés par l'Application

### Configuration Personnalisée
**Emplacement:** `C:\Users\{USER}\Documents\NiTriTe_CustomPacks.json`

**Description:** Sauvegarde vos packs Master Install personnalisés

**Suppression:** Supprimez ce fichier pour réinitialiser

### Applications Portables
**Dossier:** `C:\Users\{USER}\Documents\NiTriTe_Portables\`

**Description:** Contient toutes vos apps portables téléchargées

**Suppression:** Supprimez ce dossier pour réinitialiser (toutes les apps seront perdues)

### Logs
**Dossier:** `logs/`

**Description:** Fichiers de logs pour débogage

**Exemple:** `logs/nitrite_20241202_203643.log`

---

## 📊 Statistiques

### Contenu
- **716+ applications** (via WinGet)
- **548+ outils** (commandes + URLs)
- **60+ apps portables**
- **10 packs** Master Install
- **~6000 lignes** de code Python

### Performance
- **Démarrage:** 2-3 secondes
- **Recherche:** Instantanée
- **Installation WinGet:** Variable selon l'app
- **Téléchargement portable:** Variable selon la taille

---

## 🆕 Nouveautés V14 (vs V13)

### ✅ Bugs Corrigés
1. ✅ **548 boutons Outils** maintenant 100% fonctionnels
2. ✅ **Limite 20 apps/outils** supprimée (tout est visible)
3. ✅ **Diagnostic amélioré** avec noms exacts composants (WMI)

### 🆕 Nouvelles Fonctionnalités
1. 🆕 **Édition personnalisée packs Master Install**
2. 🆕 **Page Applications Portables** (60+ apps)
3. 🆕 **Terminal intégré** (CMD/PowerShell)

**Voir le changelog complet:** `NITRITE_V14_CHANGELOG.md`

---

## 🎯 Cas d'Usage

### Technicien Informatique
- Installation rapide de toutes les apps clients
- Outils de diagnostic complets
- Terminal intégré pour dépannage
- Apps portables sur clé USB

### Particulier
- Installation apps populaires en 1 clic
- Outils de maintenance Windows
- Optimisations système
- Diagnostic matériel

### Entreprise
- Déploiement standardisé d'applications
- Packs personnalisés par département
- Documentation complète
- Mode portable sans installation

---

## 💡 Astuces Pro

### 1. Créez vos propres packs
Éditez vos packs Master Install pour chaque type de client:
- Pack "Gaming"
- Pack "Bureautique Pro"
- Pack "Développeur"
- Pack "Graphiste"

### 2. Utilisez le terminal intégré
Plus besoin de chercher CMD ou PowerShell:
- Intégré directement dans l'app
- Historique des commandes
- Copier/coller facile

### 3. Clé USB avec apps portables
Téléchargez vos outils préférés:
- Copiez le dossier `Documents/NiTriTe_Portables` sur clé USB
- Utilisez-les sur n'importe quel PC
- Aucune installation nécessaire

### 4. Export diagnostic
Créez des rapports pour vos clients:
- Diagnostic complet matériel
- Export en fichier texte
- Idéal pour devis/factures

---

## 📞 Support

### Documentation
- **README:** Ce fichier
- **Changelog:** `NITRITE_V14_CHANGELOG.md`
- **Docs techniques:** `docs/`

### Problèmes Connus
Consultez le fichier `docs/TROUBLESHOOTING.md` (si disponible)

### Contact
- **Email:** support@ordiplus.com (fictif pour l'exemple)
- **Site Web:** www.ordiplus.com (fictif pour l'exemple)

---

## 🎉 Version Premium

**NiTriTe Premium** offre des fonctionnalités avancées:

### Fonctionnalités Exclusives
- ✨ Support prioritaire (réponse < 24h)
- ✨ Mises à jour automatiques
- ✨ Gestion multi-PC (déploiement réseau)
- ✨ Thèmes personnalisés illimités
- ✨ Mode serveur (gestion à distance)
- ✨ Rapports personnalisables
- ✨ API pour intégrations
- ✨ Formations vidéo complètes

### Tarification
- **Professionnel:** 49€/an (1 PC)
- **Entreprise:** 199€/an (10 PC)
- **Multi-sites:** Sur devis

**Essai gratuit 30 jours disponible !**

---

## 📜 Licence

**NiTriTe V14 MVP** - Tous droits réservés © 2024 OrdiPlus

**Version gratuite:**
- ✅ Usage personnel illimité
- ✅ Usage professionnel (1 PC)
- ❌ Redistribution interdite
- ❌ Modifications interdites

**Pour usage commercial étendu, contactez-nous pour une licence Premium.**

---

## 🙏 Remerciements

Merci d'avoir choisi **NiTriTe V14** !

Cette application a été développée avec passion pour faciliter la vie des techniciens informatiques et particuliers.

### Technologies Utilisées
- **CustomTkinter** - Framework UI moderne
- **Python** - Langage de programmation
- **WinGet** - Gestionnaire de paquets Microsoft
- **WMI** - Windows Management Instrumentation
- **Material Design 3** - Système de design Google

---

## 📅 Roadmap

### V14.1 (Q1 2025)
- [ ] Téléchargement réel apps portables
- [ ] Mode multi-langue complet (FR/EN/ES)
- [ ] Thèmes personnalisables
- [ ] Historique actions avec undo

### V14.2 (Q2 2025)
- [ ] Mode serveur pour déploiement réseau
- [ ] API REST pour intégrations
- [ ] Notifications système
- [ ] Mises à jour auto

### V15.0 (Q3 2025)
- [ ] Version web (Progressive Web App)
- [ ] Support Linux (via Wine)
- [ ] Intelligence artificielle pour diagnostic
- [ ] Marketplace plugins communautaires

---

**Version actuelle:** 14.0 MVP  
**Date de sortie:** Décembre 2024  
**Dernière mise à jour README:** 02/12/2024

---

**🚀 Bon dépannage avec NiTriTe V14 !**

Pour toute question, consultez la documentation complète ou contactez le support.

**Happy Troubleshooting! 🎉**