# 🏗️ Architecture Système

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLIENTS PUBLICS                              │
├─────────────────────────────────────────────────────────────────────┤
│  📱 Navigateur Web (Étudiants)        👨‍💼 Admin (Délégué)         │
│   └─ /formulaire.html                 └─ /api/admin/dashboard       │
└────────────┬────────────────────────────────────────┬───────────────┘
             │                                        │
             │ HTTP/HTTPS                             │
             ▼                                        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND (Serveur)                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Route: /api/soumettre-fiche  (POST) ────┐                         │
│  Route: /api/admin/login      (POST) ─┐   │                        │
│  Route: /api/admin/fiches     (GET)  │ │   │                        │
│  Route: /api/admin/stats      (GET)  │ │   │                        │
│  Route: /api/admin/download-excel    │ │   │                        │
│                                       │ │   │                        │
└───────────────────────────────────────┼─┼───┼──────────────────────┘
                                        │ │   │
              ┌─────────────────────────┘ │   │
              │      ┌──────────────────┘   │
              │      │  ┌────────────────────┘
              ▼      ▼  ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    EXCEL GENERATOR                                   │
├──────────────────────────────────────────────────────────────────────┤
│  ✅ Généré automatiquement après chaque soumission                   │
│  ✅ Stocké localement ou sur système de fichiers                    │
│  ✅ Téléchargeable par l'admin                                      │
└──────────────────────────────────────────────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    POSTGRESQL (Neon DB)                             │
├──────────────────────────────────────────────────────────────────────┤
│  Table: fiches_stages                                               │
│  ├─ ID (Primary Key)                                               │
│  ├─ Données Étudiant (nom, contact, niveau, filière)              │
│  ├─ Données Stage (OUI/NON, entreprise, commune, dates)           │
│  └─ Métadonnées (date_création, date_modification)                │
│                                                                      │
│  Indexes: nom_etudiant, en_stage, date_fiche                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

# 📡 Flux de données

## Soumission Formulaire Étudiant

```
1️⃣  Étudiant remplit le formulaire
    ↓
2️⃣  Frontend valide les données (JavaScript)
    ↓
3️⃣  Envoi POST → /api/soumettre-fiche
    ↓
4️⃣  Backend valide & enregistre en DB
    ↓
5️⃣  Excel généré automatiquement
    ↓
6️⃣  Page de confirmation affichée
```

## Accès Admin Dashboard

```
1️⃣  Admin accède /api/admin/dashboard
    ↓
2️⃣  Formulaire de login
    ↓
3️⃣  POST /api/admin/login (username + password)
    ↓
4️⃣  Token généré, stocké en localStorage
    ↓
5️⃣  GET /api/admin/stats + /api/admin/fiches (avec token)
    ↓
6️⃣  Dashboard affiche stats et tableau
    ↓
7️⃣  Admin peut télécharger Excel
```

---

# 🔄 Cycle de vie des données

```
FORMULAIRE (Frontend, HTML/JS)
    │
    ├─ Validation locale (requis, format)
    │
    ▼
API BACKEND (FastAPI)
    │
    ├─ Validation Pydantic
    │
    ├─ Vérification duplicata
    │
    ├─ INSERT/UPDATE en DB
    │
    ├─ Génération Excel
    │
    └─ Retour JSON réussi
        │
        ▼
    DATABASE (PostgreSQL)
        │
        ├─ Enregistrement persistant
        │
        ├─ Indexes pour recherche rapide
        │
        └─ Métadonnées d'audit
            │
            ▼
        ADMIN DASHBOARD
            │
            ├─ Lecture stats
            │
            ├─ Affichage tableau
            │
            └─ Export Excel (pour rapports)
```

---

# 🛡️ Couches de sécurité

```
┌─ HTTPS/TLS (Chiffrement en transit)
│
├─ CORS (Contrôle des origines)
│
├─ Validation des entrées (Pydantic)
│
├─ Authentification Admin (username + password)
│
├─ Token de session (localStorage)
│
├─ Base de données (Neon DB, chiffrée)
│
└─ Logs d'audit (date_création, date_modification)
```

---

# 📊 Capacité & Performance

| Métrique | Valeur |
|----------|--------|
| Fiches supportées | Illimitées (PostgreSQL) |
| Taille Excel | ~1 MB par 1000 fiches |
| Temps de réponse | < 500 ms |
| Utilisateurs simultanés | 100+ (Railway Standard) |
| Uptime | 99.9% (Railway/Render) |

---

# 🚀 Technologies utilisées

| Couche | Technologie |
|--------|------------|
| Frontend | HTML5 + CSS3 + JavaScript (Vanilla) |
| Backend | FastAPI (Python 3.11) |
| Database | PostgreSQL (Neon) |
| Hosting | Railway ou Render |
| Excel | openpyxl (Python) |
| ORM | SQLAlchemy |

---

# ✅ Checklist de déploiement

- [ ] Repository GitHub créé
- [ ] Neon DB account + connection string
- [ ] Railway/Render account
- [ ] Variables d'environnement configurées
- [ ] Domaine personnalisé (optionnel)
- [ ] HTTPS automatique (inclus)
- [ ] Mot de passe admin changé
- [ ] Test du formulaire
- [ ] Test de l'admin dashboard
- [ ] Test du téléchargement Excel
- [ ] Sauvegarde DB configurée
- [ ] Documentation mise à jour

