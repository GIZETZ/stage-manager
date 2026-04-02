#!/bin/bash
# Script de démarrage rapide local pour développement

echo "🚀 Stage Manager - Démarrage local"
echo "===================================="

# Vérifier Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé"
    echo "   Install: https://www.docker.com/products/docker-desktop"
    exit 1
fi

echo "✅ Docker trouvé"

# Vérifier docker-compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose n'est pas installé"
    exit 1
fi

echo "✅ docker-compose trouvé"

# Créer fichier .env s'il n'existe pas
if [ ! -f backend/.env ]; then
    echo "📝 Création du fichier .env..."
    cp backend/.env.example backend/.env
    echo "✅ .env créé (éditer les valeurs si nécessaire)"
fi

# Lancer docker-compose
echo "🐳 Lançage des services (PostgreSQL + Backend)..."
docker-compose up -d

echo ""
echo "✅ Services démarrés!"
echo ""
echo "📍 Accès aux services:"
echo "   - Frontend: http://localhost:8000/formulaire.html"
echo "   - Admin: http://localhost:8000/api/admin/dashboard"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - Database: localhost:5432 (stage_manager)"
echo ""
echo "👤 Identifiants admin:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "🛑 Pour arrêter: docker-compose down"
echo "📊 Voir les logs: docker-compose logs -f backend"
