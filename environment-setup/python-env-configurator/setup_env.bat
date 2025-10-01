@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ================================
echo  CONFIGURATEUR D'ENVIRONNEMENT
echo ================================
echo.

REM Selection du repertoire de travail
echo SELECTION DU REPERTOIRE DE TRAVAIL
echo.
echo Options disponibles:
echo   1. Repertoire actuel: %CD%
echo   2. Specifier un autre repertoire
echo   3. Parcourir avec l'explorateur
echo.
set /p choice="Votre choix (1-3): "

if "%choice%"=="1" (
    set "WORK_DIR=%CD%"
    echo Repertoire selectionne: !WORK_DIR!
) else if "%choice%"=="2" (
    set /p WORK_DIR="Entrez le chemin complet du repertoire: "
    if not exist "!WORK_DIR!" (
        echo ERREUR: Le repertoire n'existe pas
        pause
        exit /b 1
    )
) else if "%choice%"=="3" (
    echo Ouverture de l'explorateur de fichiers...
    echo Selectionnez le dossier de votre projet, puis revenez ici
    echo.
    explorer.exe
    set /p WORK_DIR="Collez le chemin du repertoire selectionne: "
    if not exist "!WORK_DIR!" (
        echo ERREUR: Le repertoire n'existe pas
        pause
        exit /b 1
    )
) else (
    echo Choix invalide, utilisation du repertoire actuel
    set "WORK_DIR=%CD%"
)

REM Changer vers le repertoire de travail
echo.
echo Changement vers le repertoire: !WORK_DIR!
cd /d "!WORK_DIR!"
echo Repertoire actuel: %CD%
echo.

REM Verification Python
echo Verification Python...
python --version
if errorlevel 1 (
    echo ERREUR: Python non trouve
    pause
    exit /b 1
)
echo.

REM Creation environnement virtuel
echo Creation environnement virtuel...
if exist env (
    echo Environnement existant trouve
    set /p recreate="Recreer l'environnement? (o/N): "
    if /i "!recreate!"=="o" (
        echo Suppression ancien environnement...
        rmdir /s /q env
    ) else (
        echo Conservation environnement existant
        goto :activate_creation
    )
)

echo Creation nouvel environnement...
python -m venv env
if errorlevel 1 (
    echo ERREUR: Impossible de creer l'environnement
    pause
    exit /b 1
)
echo Environnement cree avec succes
echo.

REM Mise a jour pip
echo Mise a jour pip...
env\Scripts\pip install --upgrade pip
echo.

REM Detection automatique des dependances dans tous les fichiers .py
echo Detection des dependances dans les fichiers Python...
set "DEPS_FOUND="

REM Recherche Azure
for %%f in (*.py) do (
    findstr /i "import azure\|from azure" "%%f" >nul 2>&1
    if not errorlevel 1 (
        echo   - Azure detecte dans %%f
        set "DEPS_FOUND=!DEPS_FOUND! azure"
    )
)

REM Recherche Pandas
for %%f in (*.py) do (
    findstr /i "import pandas\|from pandas" "%%f" >nul 2>&1
    if not errorlevel 1 (
        echo   - Pandas detecte dans %%f
        set "DEPS_FOUND=!DEPS_FOUND! pandas"
    )
)

REM Recherche Requests
for %%f in (*.py) do (
    findstr /i "import requests\|from requests" "%%f" >nul 2>&1
    if not errorlevel 1 (
        echo   - Requests detecte dans %%f
        set "DEPS_FOUND=!DEPS_FOUND! requests"
    )
)

REM Recherche Flask
for %%f in (*.py) do (
    findstr /i "import flask\|from flask" "%%f" >nul 2>&1
    if not errorlevel 1 (
        echo   - Flask detecte dans %%f
        set "DEPS_FOUND=!DEPS_FOUND! flask"
    )
)

REM Recherche NumPy
for %%f in (*.py) do (
    findstr /i "import numpy\|from numpy" "%%f" >nul 2>&1
    if not errorlevel 1 (
        echo   - NumPy detecte dans %%f
        set "DEPS_FOUND=!DEPS_FOUND! numpy"
    )
)

echo.

REM Installation des dependances detectees
echo DEPS_FOUND | findstr /i "azure" >nul
if not errorlevel 1 (
    echo Dependances Azure detectees
    set /p install_azure="Installer azure-identity et azure-mgmt-resourcegraph? (O/n): "
    if /i not "!install_azure!"=="n" (
        echo Installation azure-identity...
        env\Scripts\pip install azure-identity
        echo Installation azure-mgmt-resourcegraph...
        env\Scripts\pip install azure-mgmt-resourcegraph
    )
)

echo DEPS_FOUND | findstr /i "pandas" >nul
if not errorlevel 1 (
    echo Dependance pandas detectee
    set /p install_pandas="Installer pandas? (O/n): "
    if /i not "!install_pandas!"=="n" (
        echo Installation pandas...
        env\Scripts\pip install pandas
    )
)

echo DEPS_FOUND | findstr /i "requests" >nul
if not errorlevel 1 (
    echo Dependance requests detectee
    set /p install_requests="Installer requests? (O/n): "
    if /i not "!install_requests!"=="n" (
        echo Installation requests...
        env\Scripts\pip install requests
    )
)

echo DEPS_FOUND | findstr /i "flask" >nul
if not errorlevel 1 (
    echo Dependance flask detectee
    set /p install_flask="Installer flask? (O/n): "
    if /i not "!install_flask!"=="n" (
        echo Installation flask...
        env\Scripts\pip install flask
    )
)

echo DEPS_FOUND | findstr /i "numpy" >nul
if not errorlevel 1 (
    echo Dependance numpy detectee
    set /p install_numpy="Installer numpy? (O/n): "
    if /i not "!install_numpy!"=="n" (
        echo Installation numpy...
        env\Scripts\pip install numpy
    )
)

REM Si aucune dependance detectee, proposer des stacks
if "!DEPS_FOUND!"=="" (
    echo Aucune dependance detectee automatiquement
    echo.
    echo Stacks predefinies disponibles:
    echo   1. Azure (azure-identity, azure-mgmt-resourcegraph)
    echo   2. Data Science (pandas, numpy, matplotlib)
    echo   3. Web Development (flask, requests)
    echo   4. Aucune installation
    echo.
    set /p stack_choice="Choisir une stack (1-4): "
    
    if "!stack_choice!"=="1" (
        echo Installation stack Azure...
        env\Scripts\pip install azure-identity azure-mgmt-resourcegraph
    ) else if "!stack_choice!"=="2" (
        echo Installation stack Data Science...
        env\Scripts\pip install pandas numpy matplotlib
    ) else if "!stack_choice!"=="3" (
        echo Installation stack Web Development...
        env\Scripts\pip install flask requests
    )
)

echo.
echo Generation requirements.txt...
env\Scripts\pip freeze > requirements.txt
echo.

:activate_creation
REM Obtenir le nom du projet depuis le repertoire
for %%i in ("!WORK_DIR!") do set "PROJECT_NAME=%%~ni"

echo Creation script d'activation...
(
echo @echo off
echo chcp 65001 ^>nul
echo echo Activation environnement: !PROJECT_NAME!
echo call env\Scripts\activate
echo echo Environnement Python active !
echo echo Repertoire: !WORK_DIR!
echo echo Tapez 'deactivate' pour quitter
echo cmd /k
) > activate.bat

echo Creation .gitignore...
if not exist .gitignore (
    (
    echo env/
    echo __pycache__/
    echo *.pyc
    echo *.pyo
    echo .env
    echo logs/
    echo temp/
    echo *.log
    ) > .gitignore
)

echo.
echo ================================
echo  CONFIGURATION TERMINEE !
echo ================================
echo.
echo PROJET: !PROJECT_NAME!
echo REPERTOIRE: !WORK_DIR!
echo.
echo UTILISATION:
echo   1. Double-cliquez sur activate.bat
echo   2. Lancez vos scripts Python
echo   3. Tapez 'deactivate' pour quitter
echo.
echo Fichiers crees:
echo   - env/ (environnement virtuel)
echo   - activate.bat (script d'activation)
echo   - requirements.txt (dependances)
echo   - .gitignore (exclusions Git)
echo.

pause