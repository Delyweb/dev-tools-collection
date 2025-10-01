# 🐍 Python Environment Configurator

Un outil automatique pour créer et configurer des environnements virtuels Python avec détection intelligente des dépendances.

[![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg)](https://github.com/votre-username/my-dev-tools/releases)
[![Platform](https://img.shields.io/badge/Platform-Windows-blue.svg)](https://microsoft.com/windows)
[![Python](https://img.shields.io/badge/Python-3.6%2B-green.svg)](https://python.org)

##  Fonctionnalités

###  Détection Automatique
- **Analyse intelligente** des imports dans vos fichiers Python
- **Détection Azure** : `azure-identity`, `azure-mgmt-resourcegraph` 
- **Détection Data Science** : `pandas`, `numpy`, `matplotlib`
- **Détection Web** : `flask`, `django`, `fastapi`
- **Extensible** : Facile d'ajouter de nouvelles bibliothèques

###  Configuration Complète
- **Environnement virtuel** isolé dans `env/`
- **Installation automatique** des dépendances détectées
- **requirements.txt** généré automatiquement
- **activate.bat** pour activation en un clic
- **.gitignore** configuré automatiquement

###  Gestion Intelligente
- **Détection d'environnement existant** avec option de recréation
- **Mise à jour pip** automatique
- **Confirmation utilisateur** avant installation
- **Messages clairs** et informatifs

##  Installation

### Méthode 1: Téléchargement Direct
```bash
curl -O https://raw.githubusercontent.com/votre-username/my-dev-tools/main/bootstrap-tools/python-env-configurator/setup_env.bat
```

### Méthode 2: Clone du Repository
```bash
git clone https://github.com/votre-username/my-dev-tools.git
cd my-dev-tools/bootstrap-tools/python-env-configurator
copy setup_env.bat C:\votre\projet\
```

##  Guide d'Utilisation

### Utilisation Basique

1. **Copiez** `setup_env.bat` dans votre dossier de projet Python
2. **Double-cliquez** sur le fichier
3. **Suivez** les instructions à l'écran
4. **Utilisez** `activate.bat` pour démarrer votre environnement

```bash
# Après configuration
activate.bat              # Active l'environnement
python votre_script.py    # Lance votre script
deactivate                # Désactive l'environnement
```

### Exemple Complet

```bash
# Votre projet contient :
my_azure_project/
├── azure_script.py       # Votre script avec imports Azure
└── setup_env.bat         # Configurateur copié

# Contenu de azure_script.py :
from azure.identity import DefaultAzureCredential
from azure.mgmt.resourcegraph import ResourceGraphClient
import pandas as pd

# 1. Double-clic sur setup_env.bat
# 2. Le script détecte automatiquement :
#    - azure-identity
#    - azure-mgmt-resourcegraph  
#    - pandas
# 3. Propose l'installation
# 4. Crée l'environnement configuré

# Résultat :
my_azure_project/
├── azure_script.py
├── activate.bat          #  Script d'activation
├── requirements.txt      #  Dépendances installées
├── .gitignore           #  Configuration Git
└── env/                 #  Environnement isolé
```

##  Exemples par Type de Projet

### Projet Azure Security
```python
# azure_security.py
from azure.identity import DefaultAzureCredential
from azure.mgmt.resourcegraph import ResourceGraphClient
import pandas as pd

# Détection automatique :
#  azure-identity
#  azure-mgmt-resourcegraph
#  pandas
```

### Projet Data Science
```python
# data_analysis.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Détection automatique :
#  pandas
#  numpy  
#  matplotlib
```

### Projet Web API
```python
# web_api.py
from flask import Flask, request
import requests

# Détection automatique :
#  flask
#  requests
```

##  Configuration Avancée

### Ajouter une Nouvelle Détection

Pour détecter automatiquement d'autres bibliothèques, modifiez `setup_env.bat` :

```batch
REM Exemple : Détecter NumPy
findstr /i "import numpy" *.py >nul
if not errorlevel 1 (
    echo Dependance NumPy detectee
    set /p install_numpy="Installer numpy? (O/n): "
    if /i not "!install_numpy!"=="n" (
        echo Installation numpy...
        env\Scripts\pip install numpy
    )
)
```

### Personnaliser les Messages

```batch
REM Personnaliser le nom du projet
echo Activation environnement: MonProjet
```

##  Structure Après Configuration

```
votre-projet/
├── votre_script.py          # Vos fichiers Python
├── setup_env.bat            # Configurateur (supprimable après usage)
├── activate.bat             # Script d'activation 
├── requirements.txt         # Liste des dépendances
├── .gitignore              # Exclusions Git
└── env/                    # Environnement virtuel isolé
    ├── Scripts/
    │   ├── python.exe
    │   ├── pip.exe
    │   └── activate.bat
    ├── Lib/
    └── Include/
```

## 🔧 Gestion des Dépendances

### Ajouter une Nouvelle Dépendance

```bash
# Dans l'environnement activé
activate.bat
pip install nouvelle_bibliotheque
pip freeze > requirements.txt    # Mettre à jour
```

### Installer depuis requirements.txt

```bash
# Nouveau collaborateur
activate.bat
pip install -r requirements.txt
```

### Mettre à Jour une Dépendance

```bash
activate.bat
pip install --upgrade nom_package
pip freeze > requirements.txt
```

##  Résolution de Problèmes

### Erreur "Python non trouvé"
```bash
# Vérifier l'installation
python --version

# Ajouter Python au PATH si nécessaire
```

### Erreur "Permission refusée"
```bash
# Solution 1: Exécuter en tant qu'administrateur
# Clic droit > "Exécuter en tant qu'administrateur"

# Solution 2: Vérifier les permissions du dossier
```

### Environnement ne s'active pas
```bash
# Vérifier que env/ existe
dir env

# Recréer si nécessaire
setup_env.bat
# Choisir "o" pour recréer
```

### Dépendances non détectées
```bash
# Vérifier la syntaxe des imports dans vos fichiers .py
# Le script cherche : "import module" et "from module"
```

##  Commandes Utiles

### Gestion de l'Environnement
```bash
activate.bat                    # Activer l'environnement
deactivate                      # Désactiver l'environnement
```

### Gestion des Packages
```bash
pip list                        # Lister les packages installés
pip show package_name           # Informations sur un package
pip uninstall package_name      # Désinstaller un package
pip freeze > requirements.txt   # Sauvegarder les dépendances
```

### Nettoyage
```bash
rmdir /s env                    # Supprimer l'environnement
del requirements.txt            # Supprimer les dépendances
setup_env.bat                   # Recréer l'environnement
```

##  Contribution

Les améliorations sont les bienvenues ! Pour contribuer :

1. Forkez le repository principal
2. Créez une branche pour votre amélioration
3. Testez vos modifications
4. Soumettez une Pull Request

### Idées d'Amélioration

- [ ] Support Linux/macOS (scripts .sh)
- [ ] Détection de plus de bibliothèques
- [ ] Configuration par fichier de configuration
- [ ] Interface graphique simple
- [ ] Intégration avec IDE (VS Code, PyCharm)

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](../../LICENSE) pour plus de détails.

## 🔗 Liens Utiles

- [Python Virtual Environments Guide](https://docs.python.org/3/tutorial/venv.html)
- [Pip Documentation](https://pip.pypa.io/en/stable/)
- [Azure SDK for Python](https://docs.microsoft.com/en-us/azure/developer/python/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

**Version :** 1.0.0  
**Dernière mise à jour :** $(date)  
**Compatibilité :** Windows, Python 3.6+
