from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class FicheStageCreate(BaseModel):
    etudiant_id: int
    contact_etudiant: str
    niveau_etude: str
    filiere_classe: str
    date_fiche: date
    en_stage: str
    nom_entreprise: Optional[str] = None
    situation_entreprise: Optional[str] = None
    contact_entreprise: Optional[str] = None
    date_debut_stage: Optional[date] = None
    date_fin_stage: Optional[date] = None

class FicheStageResponse(BaseModel):
    id: int
    etudiant_id: int
    contact_etudiant: str
    niveau_etude: str
    filiere_classe: str
    date_fiche: date
    en_stage: str
    nom_entreprise: Optional[str] = None
    situation_entreprise: Optional[str] = None
    contact_entreprise: Optional[str] = None
    date_debut_stage: Optional[date] = None
    date_fin_stage: Optional[date] = None
    date_creation: datetime
    date_modification: Optional[datetime] = None

    class Config:
        from_attributes = True

class EtudiantResponse(BaseModel):
    id: int
    nom: str
    date_creation: datetime

    class Config:
        from_attributes = True

class AdminLogin(BaseModel):
    username: str
    password: str

class AdminResponse(BaseModel):
    access: bool
    message: str
    token: Optional[str] = None
