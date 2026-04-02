@echo off
REM Script de démarrage rapide pour Windows

echo.
echo 🚀 Stage Manager - Demarrage local (Windows)
echo ============================================

REM Vérifier Docker
where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker n'est pas installe
    echo    Install: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo ✅ Docker trouve

REM Vérifier docker-compose
where docker-compose >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ docker-compose n'est pas installe
    pause
    exit /b 1
)

echo ✅ docker-compose trouve

REM Créer fichier .env s'il n'existe pas
if not exist "backend\.env" (
    echo 📝 Creation du fichier .env...
    copy backend\.env.example backend\.env
    echo ✅ .env cree ^(editer les valeurs si necessaire^)
)

REM Lancer docker-compose
echo.
echo 🐳 Lancement des services ^(PostgreSQL + Backend^)...
docker-compose up -d

echo.
echo ✅ Services demarres!
echo.
echo 📍 Acces aux services:
echo    - Frontend: http://localhost:8000/formulaire.html
echo    - Admin: http://localhost:8000/api/admin/dashboard
echo    - API Docs: http://localhost:8000/docs
echo    - Database: localhost:5432 ^(stage_manager^)
echo.
echo 👤 Identifiants admin:
echo    Username: admin
echo    Password: admin123
echo.
echo 🛑 Pour arreter: docker-compose down
echo 📊 Voir les logs: docker-compose logs -f backend
echo.
pause
