# Roblox Downloader

Application de téléchargement de contenus Roblox avec interface graphique moderne.

## Caractéristiques

✨ **Interface noire et rouge** - Design moderne et élégant
🔍 **Recherche par ID** - Entrez votre ID Roblox pour télécharger
📥 **Téléchargement automatique** - Récupère les fichiers depuis l'API rbxdl
📂 **Gestion des fichiers** - Visualisez, rafraîchissez et supprimez vos téléchargements
🎯 **Interface intuitive** - Facile à utiliser pour tous

## Prérequis

- Python 3.7+
- PyQt5
- requests

## Installation

### 1. Cloner le projet (si ce n'est pas déjà fait)
```bash
cd /workspaces/maybe-new-software
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

## Utilisation

### Lancer l'application
```bash
python3 app.py
```

Ou utiliser le script d'exécution:
```bash
chmod +x run.sh
./run.sh
```

### Guide d'utilisation

1. **Entrer un ID Roblox**: Tapez l'ID Roblox dans le champ d'entrée
2. **Cliquer sur "SEARCH"**: Le bouton lance le téléchargement
3. **Attendre le téléchargement**: L'application vous informera du statut
4. **Consulter les fichiers**: Les fichiers téléchargés apparaissent dans la liste
5. **Gérer les fichiers**: 
   - **OUVRIR DOSSIER**: Ouvre le dossier de téléchargement dans l'explorateur
   - **SUPPRIMER FICHIER**: Supprime le fichier sélectionné
   - **RAFRAÎCHIR**: Met à jour la liste des fichiers

## Structure du projet

```
maybe-new-software/
├── app.py              # Application principale
├── requirements.txt    # Dépendances Python
├── run.sh             # Script de lancement
├── README.md          # Ce fichier
├── downloads/         # Dossier des téléchargements (créé automatiquement)
└── test/             # Dossier de tests
```

## Dossier de téléchargement

Les fichiers téléchargés sont organisés par ID Roblox:
```
downloads/
├── [ID1]/
│   ├── fichier1.json
│   └── fichier2.rbx
└── [ID2]/
    └── fichier3.rbx
```

## API utilisée

- **Endpoint**: `https://rbxdl.johnmarctumulak.com/api/download/{id}`
- L'application envoie l'ID Roblox et récupère les fichiers correspondants

## Couleurs et style

- **Fond**: Noir (#000000)
- **Texte**: Rouge (#FF0000)
- **Bordures**: Rouge (#FF0000)
- **Boutons**: Rouge (#FF0000) avec fond noir

## Dépannage

### "Erreur: Impossible de se connecter au serveur"
- Vérifiez votre connexion Internet
- Le serveur rbxdl.johnmarctumulak.com est peut-être indisponible

### "Délai d'attente dépassé"
- Le serveur répond lentement
- Réessayez dans quelques instants

### PyQt5 non trouvé
```bash
pip install --upgrade pip
pip install PyQt5==5.15.9
```

## Développement

Pour modifier l'interface ou ajouter des fonctionnalités:
1. Éditez `app.py`
2. Relancez l'application

## Sécurité

⚠️ **Note importante**: Cette application télécharge du contenu depuis une API tierce. Utilisez-la de manière responsable et respectez les conditions d'utilisation du site.

## Licence

Ce projet est fourni à titre d'exemple éducatif.

---

**Version**: 1.0  
**Auteur**: Roblox Downloader Team  
**Dernière mise à jour**: 2026
