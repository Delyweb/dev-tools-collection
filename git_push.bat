@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ===============================
echo  GIT PUSH AUTOMATIQUE
echo ===============================
echo.

REM Verification que nous sommes dans le bon repertoire
if not exist ".git" (
    echo ERREUR: Ce n'est pas un repository Git
    echo Assurez-vous d'etre dans le repertoire dev-tools-collection
    pause
    exit /b 1
)

echo Repertoire Git detecte: %CD%
echo.

REM Verification du status Git
echo 1. Verification du status Git...
git status --porcelain > temp_status.txt
set /a "changes=0"
for /f %%i in ('type temp_status.txt ^| find /c /v ""') do set "changes=%%i"
del temp_status.txt

if %changes%==0 (
    echo   Aucune modification detectee
    echo   Le repository est deja a jour
    pause
    exit /b 0
)

echo   %changes% modification(s) detectee(s)
echo.

REM Affichage des modifications
echo 2. Modifications detectees:
git status --short
echo.

REM Demande de confirmation
set /p confirm="Voulez-vous commiter et pusher ces modifications? (O/n): "
if /i "!confirm!"=="n" (
    echo Operation annulee
    pause
    exit /b 0
)

REM Demande du message de commit
echo.
echo 3. Message de commit:
echo.
echo Messages suggeres:
echo   1. feat: Add CSS library with professional theme
echo   2. update: Improve Python environment configurator
echo   3. fix: Correct issue in tool
echo   4. docs: Update documentation
echo   5. Personnalise
echo.
set /p msg_choice="Choisir un message (1-5): "

if "!msg_choice!"=="1" (
    set "commit_msg=feat: Add CSS library with professional theme

- Add ThemeCT CSS framework to productivity tools
- Complete component library with modern design
- Responsive layout system and navigation
- Professional color palette and styling
- Documentation with usage examples"

) else if "!msg_choice!"=="2" (
    set "commit_msg=update: Improve Python environment configurator

- Add working directory selection functionality
- Enhance dependency detection for multiple libraries
- Add predefined technology stacks
- Improve user interface with better prompts
- Generate project-specific activation scripts"

) else if "!msg_choice!"=="3" (
    set /p custom_fix="Decrivez le probleme corrige: "
    set "commit_msg=fix: !custom_fix!"

) else if "!msg_choice!"=="4" (
    set /p custom_docs="Decrivez la mise a jour de documentation: "
    set "commit_msg=docs: !custom_docs!"

) else if "!msg_choice!"=="5" (
    echo.
    set /p commit_msg="Entrez votre message de commit: "
    if "!commit_msg!"=="" (
        set "commit_msg=update: General improvements and updates"
    )
) else (
    set "commit_msg=update: General improvements and updates"
)

echo.
echo Message de commit selectionne:
echo "!commit_msg!"
echo.

REM Execution des commandes Git
echo 4. Ajout des fichiers...
git add .
if errorlevel 1 (
    echo ERREUR lors de 'git add'
    pause
    exit /b 1
)
echo   Fichiers ajoutes avec succes

echo.
echo 5. Creation du commit...
git commit -m "!commit_msg!"
if errorlevel 1 (
    echo ERREUR lors du commit
    pause
    exit /b 1
)
echo   Commit cree avec succes

echo.
echo 6. Push vers GitHub...
git push origin main
if errorlevel 1 (
    echo ERREUR lors du push
    echo.
    echo Tentative de pull puis push...
    git pull origin main --allow-unrelated-histories
    if not errorlevel 1 (
        echo Pull reussi, nouveau tentative de push...
        git push origin main
        if errorlevel 1 (
            echo ERREUR: Push definitivement echoue
            pause
            exit /b 1
        )
    ) else (
        echo ERREUR: Pull et push ont echoue
        pause
        exit /b 1
    )
)

echo   Push vers GitHub reussi !

echo.
echo ===============================
echo  SUCCES !
echo ===============================
echo.
echo Vos modifications ont ete envoyees sur GitHub:
echo https://github.com/Delyweb/dev-tools-collection
echo.
echo Resume:
git log --oneline -1
echo.

pause