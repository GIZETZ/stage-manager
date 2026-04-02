# 📋 Stage Manager – Gestion des Fiches PFE

Plateforme complète pour la gestion des fiches de stage PFE 2025-2026 avec:
- ✅ Formulaire web pour les étudiants
- 📊 Dashboard admin sécurisé
- 🗄️ Base de données PostgreSQL (Neon)
- 📥 Export Excel automatique

## Architecture

```
Stage-Manager/
├── backend/                 # FastAPI backend
│   ├── main.py             # Application FastAPI
│   ├── models.py           # Modèles SQLAlchemy
│   ├── schemas.py          # Schémas Pydantic
│   ├── database.py         # Configuration DB
│   ├── config.py           # Configuration globale
│   ├── excel_generator.py  # Génération Excel
│   ├── requirements.txt    # Dépendances Python
│   ├── .env.example        # Variables d'environnement
│   └── .env                # Variables (à créer)
├── frontend/               # Fichiers HTML statiques
│   ├── formulaire.html     # Formulaire public
│   └── admin.html          # Dashboard admin
├── Procfile               # Déploiement Heroku/Railway
└── README.md
```

## Installation locale

### 1. Cloner et installer les dépendances

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configurer la base de données

Créer un fichier `.env` dans `backend/`:

```env
# PostgreSQL via Neon
DATABASE_URL=postgresql://user:password@region.neon.tech/dbname?sslmode=require

# Admin credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=votre_mot_de_passe_securise

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### 3. Lancer le serveur

```bash
cd backend
uvicorn main:app --reload
```

L'application sera accessible à:
- **Formulaire**: http://localhost:8000
- **Admin**: http://localhost:8000/api/admin/dashboard

## 🗄️ Configuration Neon DB (PostgreSQL)

1. Aller sur [neon.tech](https://neon.tech)
2. Créer un projet gratuit
3. Copier la connection string: `postgresql://user:password@host/dbname?sslmode=require`
4. La mettre dans `.env` → `DATABASE_URL`

## 🚀 Déploiement sur Railway

### 1. Créer un compte Railway

Aller sur [railway.app](https://railway.app)

### 2. Connecter le repository GitHub

- Cliquer "New Project"
- "Deploy from GitHub" → Sélectionner le repo

### 3. Ajouter les variables d'environnement

Dans Railway Dashboard → "Variables":

```
DATABASE_URL=postgresql://user:password@region.neon.tech/dbname?sslmode=require
ADMIN_USERNAME=admin
ADMIN_PASSWORD=motde_passe_securise
ALLOWED_ORIGINS=https://your-app.railway.app
```

### 4. Deployer

Railway détectera automatiquement `Procfile` et déploiera!

## 🌍 Déploiement sur Render

### 1. Créer un compte Render

Aller sur [render.com](https://render.com)

### 2. Créer un Web Service

- "New +" → "Web Service"
- Connecter votre repository GitHub
- Choisir "Python 3"

### 3. Configuration Render

**Build Command:**
```
pip install -r backend/requirements.txt
```

**Start Command:**
```
cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Environment Variables:**
```
DATABASE_URL=postgresql://user:password@region.neon.tech/dbname?sslmode=require
ADMIN_USERNAME=admin
ADMIN_PASSWORD=motde_passe_securise
ALLOWED_ORIGINS=https://your-app.render.com
```

## 📝 Utilisation

### Formulaire public

Les étudiants accèdent à `/formulaire.html` pour:
1. Remplir leur identité
2. Indiquer leur situation de stage
3. Valider et soumettre

**Les données sont:**
- Enregistrées en base de données
- Actualisées dans l'Excel automatiquement

### Admin Dashboard

Accès: `/api/admin/dashboard`

**Identifiants par défaut:**
- Username: `admin`
- Password: `admin123` (à changer!)

**Fonctionnalités:**
- 📊 Statistiques en temps réel
- 📋 Tableau complet des fiches
- 📥 Télécharger l'Excel mis à jour

## 🔐 Sécurité

### En production:

1. **Changer le mot de passe admin** dans `.env`
2. **Utiliser HTTPS** (le fournisseur d'hébergement s'en charge)
3. **Valider les inputs** (déjà fait côté back)
4. **Utiliser JWT** pour l'authentification (si besoin avancé)

## 📊 Schéma Excel

L'Excel généré contient:
| ID | Nom | Contact | Niveau | Filière | En Stage | Entreprise | Commune | Début | Fin | Créé |
|----|----|---------|--------|---------|----------|-----------|---------|-------|-----|------|

## 🐛 Troubleshooting

### "Error: Connection refused"
- Vérifier que la DB est accessible
- Vérifiez `DATABASE_URL` dans `.env`
- Vérifiez que Neon DB est active

### "Authentication failed"
- Vérifier les identifiants admin
- Vérifier que le token existe et est valide

### Excel ne se génère pas
- Vérifier les permissions dans le répertoire
- Vérifier que `EXCEL_FILE_PATH` est correct

## 📞 Support

Pour des questions ou problèmes:
1. Vérifier les logs: `railway logs` ou `render logs`
2. Vérifier `.env` et la configuration DB
3. Vérifier que les ports ne sont pas occupés

## 📜 Licence

Projet interne – PFE 2025-2026

---

**Fait avec ❤️ pour la gestion des stages**
