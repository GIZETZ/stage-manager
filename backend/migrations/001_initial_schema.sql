-- Migration 001: Initial schema
-- Run this script in Neon DB if auto-migration doesn't work

CREATE TABLE IF NOT EXISTS fiches_stages (
    id SERIAL PRIMARY KEY,
    
    -- Student info
    nom_etudiant VARCHAR NOT NULL,
    contact_etudiant VARCHAR NOT NULL,
    niveau_etude VARCHAR NOT NULL,
    filiere_classe VARCHAR NOT NULL,
    date_fiche DATE NOT NULL,
    
    -- Stage info
    en_stage VARCHAR NOT NULL,  -- 'OUI' ou 'NON'
    nom_entreprise VARCHAR,
    situation_entreprise VARCHAR,
    contact_entreprise VARCHAR,
    date_debut_stage DATE,
    date_fin_stage DATE,
    
    -- Metadata
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP
);

-- Index pour recherches rapides
CREATE INDEX IF NOT EXISTS idx_nom_etudiant ON fiches_stages(nom_etudiant);
CREATE INDEX IF NOT EXISTS idx_en_stage ON fiches_stages(en_stage);
CREATE INDEX IF NOT EXISTS idx_date_fiche ON fiches_stages(date_fiche);
