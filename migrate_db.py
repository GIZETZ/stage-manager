#!/usr/bin/env python3
"""Migration script to update fiches_stages table schema"""
import sys
import os

# Ensure backend is in path
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

from database import engine
from sqlalchemy import inspect, text

inspector = inspect(engine)

print("=" * 60)
print("MIGRATION: Update fiches_stages schema")
print("=" * 60)

# Check current schema
if 'fiches_stages' in inspector.get_table_names():
    print("\n✓ Table fiches_stages existe")
    cols = {col['name']: col['type'] for col in inspector.get_columns('fiches_stages')}
    print(f"\nColonnes actuelles ({len(cols)}):")
    for name, dtype in cols.items():
        print(f"  - {name}: {dtype}")
    
    # Check if migrations are needed
    needs_etudiant_id = 'etudiant_id' not in cols
    has_nom_etudiant = 'nom_etudiant' in cols
    
    if needs_etudiant_id:
        print("\n⚠ Besoin d'ajouter: colonne etudiant_id")
    if has_nom_etudiant:
        print("⚠ À supprimer: colonne nom_etudiant (après migration)")
else:
    print("✗ Table fiches_stages n'existe pas!")
    sys.exit(1)

# Check etudiants table
if 'etudiants' in inspector.get_table_names():
    print("\n✓ Table etudiants existe")
    cols = {col['name']: col['type'] for col in inspector.get_columns('etudiants')}
    print(f"Colonnes ({len(cols)}):")
    for name, dtype in cols.items():
        print(f"  - {name}: {dtype}")
else:
    print("✗ Table etudiants n'existe pas!")
    sys.exit(1)

# Execute migration if needed
if needs_etudiant_id:
    print("\n" + "=" * 60)
    print("Exécution de la migration...")
    print("=" * 60)
    
    with engine.connect() as conn:
        try:
            # Add etudiant_id column
            print("\n1. Ajout colonne etudiant_id...")
            conn.execute(text("""
                ALTER TABLE fiches_stages
                ADD COLUMN etudiant_id INTEGER
            """))
            print("   ✓ Colonne ajoutée")
            
            # Add foreign key constraint
            print("\n2. Ajout contrainte foreignkey...")
            conn.execute(text("""
                ALTER TABLE fiches_stages
                ADD CONSTRAINT fk_etudiant_id
                FOREIGN KEY (etudiant_id) REFERENCES etudiants(id)
            """))
            print("   ✓ Contrainte ajoutée")
            
            # Create index
            print("\n3. Création index sur etudiant_id...")
            conn.execute(text("""
                CREATE INDEX idx_fiches_stages_etudiant_id
                ON fiches_stages(etudiant_id)
            """))
            print("   ✓ Index créé")
            
            conn.commit()
            print("\n✓ Migration terminée avec succès!")
            
        except Exception as e:
            print(f"\n✗ Erreur: {e}")
            conn.rollback()
            sys.exit(1)
else:
    print("\n✓ Schéma déjà à jour!")
