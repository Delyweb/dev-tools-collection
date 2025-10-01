@echo off
chcp 65001 >nul

echo.
echo ================================
echo  CONFIGURATEUR D'ENVIRONNEMENT
echo ================================
echo.

echo Verification Python...
python --version
if errorlevel 1 (
    echo ERREUR: Python non trouve
    pause
    exit /b 1
)
echo.

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

echo Mise a jour pip...
env\Scripts\pip install --upgrade pip
echo.

echo Detection des dependances dans Azure.py...
findstr /i "import azure" Azure.py >nul
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

findstr /i "import pandas" Azure.py >nul
if not errorlevel 1 (
    echo Dependance pandas detectee
    set /p install_pandas="Installer pandas? (O/n): "
    if /i not "!install_pandas!"=="n" (
        echo Installation pandas...
        env\Scripts\pip install pandas
    )
)

echo.
echo Generation requirements.txt...
env\Scripts\pip freeze > requirements.txt
echo.

:activate_creation
echo Creation script d'activation...
(
echo @echo off
echo chcp 65001 ^>nul
echo echo Activation environnement: 03-Azure
echo call env\Scripts\activate
echo echo Environnement Python active !
echo echo Tapez 'deactivate' pour quitter
echo cmd /k
) > activate.bat

echo Creation .gitignore...
if not exist .gitignore (
    (
    echo env/
    echo __pycache__/
    echo *.pyc
    echo .env
    echo logs/
    ) > .gitignore
)

echo.
echo ================================
echo  CONFIGURATION TERMINEE !
echo ================================
echo.
echo UTILISATION:
echo   1. Double-cliquez sur activate.bat
echo   2. Tapez: python Azure.py
echo   3. Pour quitter: deactivate
echo.
echo Fichiers crees:
echo   - env/ (environnement virtuel)
echo   - activate.bat (script d'activation)
echo   - requirements.txt (dependances)
echo   - .gitignore (exclusions Git)
echo.

pause