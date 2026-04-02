# 🚀 Guide de Déploiement Rapide

## Étape 1: Préparation (5 minutes)

### A. Créer un compte Neon DB

1. Aller sur https://neon.tech
2. Sign Up → Créer un projet gratuit
3. Copier la **connection string** (ressemble à):
   ```
   postgresql://neondb_owner:password@ep-region-123456.region.neon.tech/neondb?sslmode=require
   ```

### B. Créer un repository GitHub

1. Créer un nouveau repo sur GitHub
2. Clone le contenu du projet Stage-Manager
3. Push sur GitHub

## Étape 2: Déployer sur Railway (Recommandé - Plus simple)

### 1. Sign Up sur Railway

- Aller sur https://railway.app
- Sign up avec GitHub (plus rapide)

### 2. Créer un nouveau projet

- Dashboard → "New Project"
- "Deploy from GitHub repo"
- Sélectionner votre repo `Stage-Manager`

### 3. Configurer les variables

Railway → Project → "Variables"

Ajouter:
```
DATABASE_URL=postgresql://neondb_owner:password@ep-region.neon.tech/neondb?sslmode=require
ADMIN_USERNAME=admin
ADMIN_PASSWORD=ChangezCeMotDePasse123!
ALLOWED_ORIGINS=https://stage-manager-xyz.railway.app
EXCEL_FILE_PATH=/tmp/fiches_stages.xlsx
```

**Remplacer:**
- `DATABASE_URL` par votre Neon URL
- `stage-manager-xyz` par le vrai nom du domaine

### 4. Deploy!

Railway détecte automatiquement `Procfile` → Déploie en 2-3 minutes

**Accès:**
- Formulaire: `https://your-app.railway.app/formulaire.html`
- Admin: `https://your-app.railway.app/api/admin/dashboard`

---

## Étape 3 (Alternative): Déployer sur Render

### 1. Sign Up sur Render

- https://render.com
- Sign up avec GitHub

### 2. Créer un Web Service

Dashboard → "New +" → "Web Service"
- Connecter GitHub repo
- Environment: **Python 3**

### 3. Configuration

**Build Command:**
```bash
pip install -r backend/requirements.txt
```

**Start Command:**
```bash
cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Environment Variables:**

Mêmes que Railway (voir Section 2.3)

### 4. Deploy!

Render build et déploie automatiquement

**Accès:**
- Formulaire: `https://your-app.onrender.com/formulaire.html`
- Admin: `https://your-app.onrender.com/api/admin/dashboard`

---

## ⚡ Test local avant déploiement

### 1. Installer les dépendances

```bash
pip install -r backend/requirements.txt
```

### 2. Créer `.env` local

Dans `backend/.env`:
```env
DATABASE_URL=postgresql://stage_user:stage_password@localhost:5432/stage_manager
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
ALLOWED_ORIGINS=http://localhost:8000
EXCEL_FILE_PATH=./fiches_stages.xlsx
```

### 3. Lancer avec Docker (recommandé)

```bash
docker-compose up -d
```

Puis accédez à http://localhost:8000/formulaire.html

### 4. Ou sans Docker (PostgreSQL doit être installé localement)

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## ✅ Vérification après déploiement

1. **Accédez au formulaire** → Remplissez une fiche test
2. **Accédez à l'admin** → Connectez-vous avec les identifiants
3. **Vérifiez les stats** → Doit afficher 1 fiche
4. **Téléchargez l'Excel** → Doit contenir vos données

---

## 🔒 Changer le mot de passe admin

**En production (après déploiement):**

1. Railway/Render Dashboard
2. Aller dans "Variables"
3. Modifier `ADMIN_PASSWORD`
4. Le service redémarre automatiquement

---

## 🐛 Dépannage rapide

### "Connection refused" sur DB
- Vérifier que Neon DB est active
- Copier exactement l'URL de Neon
- Ajouter `?sslmode=require` à la fin

### Page 404 "Not found"
- Vérifier l'URL: `https://your-app.railway.app/formulaire.html`
- Pas `http://`, utiliser `https://`

### Perte d'Excel après redémarrage
- Sur Railway/Render, `/tmp` est limité
- Ajouter un stockage persistant ou garder la DB

### Admin Dashboard vide
- Vérifier que les étudiants ont submitté des fiches
- Actualiser la page (F5)

---

## 📊 Domaine personnalisé (optionnel)

### Railway
- Settings → "Custom Domain"
- Ajouter votre domaine (ex: `stages.votreécole.ci`)
- Suivre les instructions DNS

### Render
- Même processus dans Settings

---

## 📞 Support rapide

Si ça ne marche pas:

1. **Logs Railway:** Railway Dashboard → Deployment → "Logs"
2. **Logs Render:** Render Dashboard → "Logs"
3. **Vérifier `.env`:** Tous les paramètres requis?
4. **Tester localement:** Avec `docker-compose up`

---

**Bravo! 🎉 Votre plateforme est en ligne!**

Temps estimé: 15 minutes de déploiement
