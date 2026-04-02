from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
import os
from pathlib import Path
import sqlalchemy as sa

from database import engine, get_db, Base
from models import FicheStage, Etudiant
from schemas import FicheStageCreate, FicheStageResponse, AdminLogin, AdminResponse, EtudiantResponse
from config import ADMIN_USERNAME, ADMIN_PASSWORD, EXCEL_FILE_PATH, ALLOWED_ORIGINS
from excel_generator import generate_excel

# Créer les tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Stage Manager API",
    description="Gestion des fiches de stage PFE 2025-2026",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session admin
admin_session = {}

# ──────────────────────────────────
# ROUTES PUBLIQUES - FORMULAIRE
# ──────────────────────────────────

# Chemin absolu vers le dossier frontend
BACKEND_DIR = Path(__file__).parent
FRONTEND_DIR = BACKEND_DIR.parent / "frontend"

@app.get("/", response_class=HTMLResponse)
def get_form():
    """Retourne le formulaire HTML"""
    formulaire_path = FRONTEND_DIR / "formulaire.html"
    return formulaire_path.read_text(encoding="utf-8")

@app.get("/formulaire.html", response_class=HTMLResponse)
def get_form_direct():
    """Route directe pour /formulaire.html"""
    formulaire_path = FRONTEND_DIR / "formulaire.html"
    return formulaire_path.read_text(encoding="utf-8")

@app.get("/admin.html", response_class=HTMLResponse)
def get_admin():
    """Route directe pour /admin.html"""
    admin_path = FRONTEND_DIR / "admin.html"
    return admin_path.read_text(encoding="utf-8")

@app.get("/api/etudiants", response_model=list[EtudiantResponse])
def get_etudiants(db: Session = Depends(get_db)):
    """Récupère la liste de tous les étudiants"""
    etudiants = db.query(Etudiant).order_by(Etudiant.nom).all()
    return [EtudiantResponse.from_orm(e) for e in etudiants]

@app.post("/api/soumettre-fiche", response_model=FicheStageResponse)
def create_or_update_fiche_stage(
    fiche: FicheStageCreate,
    db: Session = Depends(get_db)
):
    """
    Crée ou met à jour une fiche de stage pour un étudiant
    L'étudiant_id garantit l'unicité
    """
    try:
        # Vérifier que l'étudiant existe
        etudiant = db.query(Etudiant).filter(Etudiant.id == fiche.etudiant_id).first()
        if not etudiant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Étudiant avec l'ID {fiche.etudiant_id} non trouvé"
            )
        
        # Chercher une fiche existante pour cet étudiant
        existing_fiche = db.query(FicheStage).filter(
            FicheStage.etudiant_id == fiche.etudiant_id
        ).first()
        
        if existing_fiche:
            # Mettre à jour la fiche existante
            for key, value in fiche.dict().items():
                setattr(existing_fiche, key, value)
            existing_fiche.date_modification = datetime.now()
            db.commit()
            db.refresh(existing_fiche)
            record = existing_fiche
        else:
            # Créer une nouvelle fiche
            db_fiche = FicheStage(**fiche.dict())
            db.add(db_fiche)
            db.commit()
            db.refresh(db_fiche)
            record = db_fiche
        
        # Regénérer le fichier Excel avec les relations
        all_fiches = db.query(FicheStage).options(
            sa.orm.joinedload(FicheStage.etudiant)
        ).order_by(FicheStage.date_creation.desc()).all()
        generate_excel(all_fiches, EXCEL_FILE_PATH)
        
        return FicheStageResponse.from_orm(record)
    
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création: {str(e)}"
        )

# ──────────────────────────────────
# ROUTES ADMIN
# ──────────────────────────────────

@app.post("/api/admin/login", response_model=AdminResponse)
def admin_login(credentials: AdminLogin):
    """Authentification admin"""
    if credentials.username == ADMIN_USERNAME and credentials.password == ADMIN_PASSWORD:
        token = f"{credentials.username}_{datetime.now().timestamp()}"
        admin_session[token] = {
            "username": credentials.username,
            "logged_in_at": datetime.now()
        }
        return AdminResponse(
            access=True,
            message=f"Bienvenue {credentials.username}!",
            token=token
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides"
        )

def verify_admin_token(token: str) -> bool:
    """Vérifie si le token admin est valide"""
    return token in admin_session

@app.get("/api/admin/verify-token")
def verify_token(token: str):
    """Vérifie si un token est valide"""
    return {
        "valid": verify_admin_token(token),
        "message": "Token valide" if verify_admin_token(token) else "Token invalide ou expiré"
    }

@app.get("/api/admin/dashboard", response_class=HTMLResponse)
def get_admin_dashboard():
    """Retourne la page admin"""
    with open("../frontend/admin.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/admin/fiches")
def get_all_fiches(token: str, db: Session = Depends(get_db)):
    """Récupère toutes les fiches (admin only)"""
    if not verify_admin_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré"
        )
    
    fiches = db.query(FicheStage).options(
        sa.orm.joinedload(FicheStage.etudiant)
    ).order_by(FicheStage.date_creation.desc()).all()
    
    # Formater les fiches avec le nom de l'étudiant
    result = []
    for f in fiches:
        fiche_dict = FicheStageResponse.from_orm(f).dict()
        fiche_dict['nom_etudiant'] = f.etudiant.nom if f.etudiant else "Inconnu"
        result.append(fiche_dict)
    
    return result

@app.get("/api/admin/stats")
def get_stats(token: str, db: Session = Depends(get_db)):
    """Retourne les statistiques"""
    if not verify_admin_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré"
        )
    
    total = db.query(FicheStage).count()
    en_stage = db.query(FicheStage).filter(FicheStage.en_stage == "OUI").count()
    pas_stage = db.query(FicheStage).filter(FicheStage.en_stage == "NON").count()
    
    # Nombre d'entreprises uniques
    entreprises_uniques = db.query(FicheStage.nom_entreprise).distinct().filter(
        FicheStage.nom_entreprise.isnot(None)
    ).count()
    
    return {
        "total_fiches": total,
        "en_stage": en_stage,
        "pas_stage": pas_stage,
        "entreprises_uniques": entreprises_uniques,
        "taux_placement": f"{(en_stage/total*100):.1f}%" if total > 0 else "0%"
    }

@app.get("/api/admin/download-excel")
def download_excel(token: str, db: Session = Depends(get_db)):
    """Télécharge le fichier Excel"""
    if not verify_admin_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré"
        )
    
    try:
        # Récupérer toutes les fiches et régénérer le fichier Excel
        all_fiches = db.query(FicheStage).order_by(FicheStage.date_creation.desc()).all()
        generate_excel(all_fiches, EXCEL_FILE_PATH)
        
        if not os.path.exists(EXCEL_FILE_PATH):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Impossible de générer le fichier Excel"
            )
        
        return FileResponse(
            path=EXCEL_FILE_PATH,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            filename=f"fiches_stages_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la génération du fichier: {str(e)}"
        )

@app.post("/api/admin/logout")
def admin_logout(token: str):
    """Déconnexion admin"""
    if token in admin_session:
        del admin_session[token]
    return {"message": "Déconnexion réussie"}

# ──────────────────────────────────
# HEALTH CHECK
# ──────────────────────────────────

@app.get("/api/health")
def health_check():
    """Vérification de santé de l'API"""
    return {
        "status": "OK",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
