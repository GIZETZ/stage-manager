from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Etudiant(Base):
    __tablename__ = "etudiants"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False, unique=True, index=True)
    
    # Relation avec les fiches de stage
    fiches_stages = relationship("FicheStage", back_populates="etudiant", cascade="all, delete-orphan")
    
    # Metadata
    date_creation = Column(DateTime(timezone=True), server_default=func.now())

class FicheStage(Base):
    __tablename__ = "fiches_stages"

    id = Column(Integer, primary_key=True, index=True)
    
    # Clé étrangère vers Etudiant
    etudiant_id = Column(Integer, ForeignKey("etudiants.id"), nullable=False, index=True)
    etudiant = relationship("Etudiant", back_populates="fiches_stages")
    
    # Student info
    contact_etudiant = Column(String, nullable=False)
    niveau_etude = Column(String, nullable=False)
    filiere_classe = Column(String, nullable=False)
    date_fiche = Column(Date, nullable=False)
    
    # Stage info
    en_stage = Column(String, nullable=False)  # "OUI" ou "NON"
    nom_entreprise = Column(String, nullable=True)
    situation_entreprise = Column(String, nullable=True)
    contact_entreprise = Column(String, nullable=True)
    date_debut_stage = Column(Date, nullable=True)
    date_fin_stage = Column(Date, nullable=True)
    
    # Metadata
    date_creation = Column(DateTime(timezone=True), server_default=func.now())
    date_modification = Column(DateTime(timezone=True), onupdate=func.now())
