
# 📁 Dossier data

Ce dossier regroupe toutes les données essentielles au fonctionnement de NiTriTe V.17 :

---

## 🗂️ Schéma du dossier data

```ascii
data/
│
├── programs.json           # Liste complète des applications et outils
├── config.json             # Configuration générale de l’application
├── office_links.json       # Liens vers les outils bureautiques
├── programs_backup.json    # Sauvegarde de la base apps/outils
├── theme_config.json       # Configuration des thèmes graphiques
├── README_FICHIERS.txt     # Détail de chaque fichier
├── README.md               # Ce fichier
└── RAPPORT_EXPANSION.md    # Historique et évolutions de la base
```

---

## 📊 Tableau des fichiers

| Fichier                | Rôle principal                                 | Format      | Mise à jour |
|------------------------|------------------------------------------------|-------------|-------------|
| programs.json          | Base de données des applications/outils        | JSON        | Automatique |
| config.json            | Paramètres globaux de l’application           | JSON        | Manuel      |
| office_links.json      | Liens vers suites bureautiques                 | JSON        | Manuel      |
| programs_backup.json   | Sauvegarde/restauration de la base             | JSON        | Script      |
| theme_config.json      | Thèmes graphiques et couleurs                  | JSON        | Manuel      |
| RAPPORT_EXPANSION.md   | Historique des ajouts/suppressions             | Markdown    | Manuel      |
| README_FICHIERS.txt    | Description détaillée de chaque fichier        | Texte       | Manuel      |

---

## 🔄 Sauvegarde & restauration

Des scripts intégrés permettent de :
- Sauvegarder la base d’applications et outils (`programs_backup.json`)
- Restaurer la base en cas de corruption ou d’erreur
- Exporter/importer les configurations

**Conseil :** Utilisez toujours les scripts de backup avant toute modification manuelle.

---

## 📝 Bonnes pratiques

- Ne modifiez jamais les fichiers critiques sans sauvegarde préalable
- Utilisez les scripts de backup pour restaurer rapidement
- Documentez toute modification dans `RAPPORT_EXPANSION.md`
- Vérifiez la cohérence des fichiers JSON (syntaxe, clés)

---

## 📚 Pour aller plus loin

Consultez `README_FICHIERS.txt` pour le détail de chaque fichier et leur structure interne.

---

**Le dossier data est le cœur de la personnalisation et de la sauvegarde de NiTriTe V.17 !**

# 📊 Données NiTriTe V.17

Ce dossier contient toutes les données nécessaires au fonctionnement de NiTriTe V.17 Portable/Bureau.

## 📋 Fichiers principaux


## 📁 Structure des fichiers

### Exemple de config.json
```json
{
  "app_version": "17.0.0",
  "language": "fr",
  "theme": "orange_dark",
  "auto_cleanup": true
}
```

### Exemple de programs.json
```json
{
  "Bureautique": [
    {
      "nom": "LibreOffice",
      "description": "Suite bureautique open source",
      "download_url": "https://...",
      "install_args": "/silent",
      "portable": true
    }
  ],
  ...
}
```

## 🔄 Sauvegardes

Des sauvegardes automatiques sont générées lors des modifications importantes.

## ℹ️ Notes

Tous les fichiers ici sont utilisés par l’application pour l’affichage, la gestion des profils, la personnalisation et l’installation des applications/outils.

Ne pas supprimer ou modifier sans connaissance du fonctionnement interne.

## ⚠️ Notes importantes


*Configuration organisée le 9 novembre 2025*
