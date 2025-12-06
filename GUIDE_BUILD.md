# 🚀 Guide de Build - NiTriTe V17 Portable

Ce guide explique comment créer l'exécutable portable de NiTriTe V17 sur Windows 11.

---

## 📋 Prérequis

### 1. Python 3.8 à 3.12 (REQUIS)

- **Télécharger** : [Python 3.12](https://www.python.org/downloads/)
- **Important** : Cocher "Add Python to PATH" lors de l'installation !

### 2. Vérifier l'installation

Ouvrir un PowerShell ou CMD et taper :

```cmd
python --version
```

Devrait afficher : `Python 3.12.x` ou similaire (3.8-3.12)

---

## 🔧 Installation des Dépendances

### Méthode 1 : Automatique (RECOMMANDÉ)

Ouvrir un PowerShell dans le dossier du projet et lancer :

```cmd
pip install -r requirements.txt
```

### Méthode 2 : Manuelle

```cmd
pip install customtkinter>=5.2.0
pip install Pillow>=10.0.0
pip install requests>=2.31.0
pip install psutil>=5.9.0
pip install pyinstaller>=6.0.0
```

**Sur Windows uniquement :**
```cmd
pip install pywin32>=306
pip install wmi>=1.5.1
```

---

## 🏗️ Créer l'Exécutable Portable

### Option 1 : Script Python (Multi-plateforme)

```cmd
python build_portable.py
```

✅ **Avantages** :
- Vérification automatique des dépendances
- Installation auto des packages manquants
- Messages clairs et colorés
- Fonctionne sur Windows, Linux, macOS

### Option 2 : Script Batch Windows (Classique)

```cmd
build_portable_v17.bat
```

✅ **Avantages** :
- Traditionnel pour Windows
- Double-clic facile

### Option 3 : Commande PyInstaller directe

```cmd
pyinstaller --noconfirm --clean NiTriTe_V17_Portable.spec
```

---

## 📦 Résultat du Build

Après le build, vous trouverez :

```
📁 dist/
  └── 📄 NiTriTe_V17_Portable.exe  ← VOTRE EXÉCUTABLE
```

**Taille attendue** : ~50-100 MB (dépend des dépendances)

---

## ✅ Vérification

### 1. Tester l'exécutable

Double-cliquez sur `dist/NiTriTe_V17_Portable.exe`

L'application devrait :
- ✅ Démarrer sans console
- ✅ Afficher le splash screen "NiTriTe V17"
- ✅ Charger l'interface complète
- ✅ Fonctionner sans installation

### 2. Tester sur machine propre

Copiez `NiTriTe_V17_Portable.exe` sur une machine **sans Python installé** pour vérifier qu'il est vraiment portable.

---

## ❌ Résolution des Problèmes

### Problème 1 : "pyinstaller n'est pas reconnu"

**Solution** :
```cmd
pip install pyinstaller
```

Vérifier :
```cmd
pyinstaller --version
```

### Problème 2 : "Module 'customtkinter' not found"

**Solution** :
```cmd
pip install customtkinter Pillow requests psutil
```

### Problème 3 : Le build échoue avec erreur WMI/pywin32

**Solution (Windows uniquement)** :
```cmd
pip install --upgrade pywin32 wmi
```

Puis lancer une console en **Admin** et faire :
```cmd
python C:\PythonXX\Scripts\pywin32_postinstall.py -install
```
*(Remplacer XX par votre version Python)*

### Problème 4 : L'exe démarre avec une console noire

**Vérifier dans** `NiTriTe_V17_Portable.spec` :
```python
console=False,  # Doit être False pour GUI
```

### Problème 5 : Erreur "Failed to execute script"

**Causes possibles** :
1. Dossier `data/` manquant
2. Fichier `programs.json` manquant
3. Dépendances non embarquées

**Solution** :
Vérifier que le fichier `.spec` inclut bien :
```python
datas=[('data', 'data'), ('assets', 'assets'), ('src', 'src')],
```

### Problème 6 : L'interface ne s'affiche pas

**Solution** : Vérifier les imports cachés dans `.spec` :
```python
hiddenimports = [
    'customtkinter',
    'tkinter',
    'PIL',
    # ... etc
]
```

---

## 🔍 Debugging

### Mode Debug (avec console)

Modifier temporairement `NiTriTe_V17_Portable.spec` :
```python
console=True,  # Active la console pour voir les erreurs
```

Rebuilder et lancer l'exe. Vous verrez les messages d'erreur dans la console.

### Logs PyInstaller

Les logs détaillés sont dans :
```
build/NiTriTe_V17_Portable/warn-NiTriTe_V17_Portable.txt
```

---

## 📊 Structure des Fichiers Après Build

```
Nitrite-V.17-Beta-Portable-Bureau-/
│
├── dist/
│   └── NiTriTe_V17_Portable.exe  ← Distribuer CE fichier
│
├── build/                         ← Fichiers temporaires (peut être supprimé)
│   └── NiTriTe_V17_Portable/
│
├── data/                          ← Embarqué dans l'exe
│   ├── programs.json
│   └── ...
│
├── src/                           ← Code source (embarqué)
│   └── v14_mvp/
│       ├── main_app.py
│       └── ...
│
└── NiTriTe_V17_Portable.spec     ← Configuration PyInstaller
```

---

## 🎯 Distribution

### Fichier à distribuer

**Un seul fichier** suffit :
```
dist/NiTriTe_V17_Portable.exe
```

### Taille minimale

Pour réduire la taille de l'exe :

1. **Désactiver UPX** (si vous avez des problèmes) :
   ```python
   upx=False,
   ```

2. **Optimiser** :
   ```python
   optimize=2,
   ```

3. **Exclure modules inutiles** :
   ```python
   excludes=['unittest', 'email', 'html', 'http', 'xml', 'pydoc'],
   ```

---

## 📝 Checklist Avant Distribution

- [ ] Build réussi sans erreurs
- [ ] Exe testé sur la machine de dev
- [ ] Exe testé sur machine propre (sans Python)
- [ ] Toutes les pages fonctionnent
- [ ] Les outils système se lancent
- [ ] Les installations d'apps fonctionnent
- [ ] Pas de console qui s'affiche
- [ ] Taille de l'exe raisonnable (<150MB)
- [ ] Version correcte affichée (V17 Beta)

---

## 🆘 Support

Si vous rencontrez des problèmes :

1. **Vérifier ce guide** en premier
2. **Consulter les logs** PyInstaller
3. **Tester en mode debug** (console=True)
4. **Vérifier les dépendances** (pip list)
5. **Rebuild propre** (supprimer dist/ et build/)

---

## 🔄 Rebuild Propre

Si le build ne fonctionne pas :

```cmd
REM 1. Supprimer les anciens builds
rmdir /s /q dist
rmdir /s /q build
del /q *.spec~

REM 2. Nettoyer le cache Python
rmdir /s /q __pycache__
rmdir /s /q src\__pycache__
rmdir /s /q src\v14_mvp\__pycache__

REM 3. Rebuild
pyinstaller --noconfirm --clean NiTriTe_V17_Portable.spec
```

---

**Bonne chance avec votre build ! 🚀**
