#!/usr/bin/env python3
"""Migration to make nom_etudiant nullable"""
import sys
import os

# Ensure backend is in path
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

from database import engine
from sqlalchemy import text

print("Migration: Make nom_etudiant nullable...")

with engine.connect() as conn:
    try:
        # Make nom_etudiant nullable
        conn.execute(text("""
            ALTER TABLE fiches_stages
            ALTER COLUMN nom_etudiant DROP NOT NULL
        """))
        print("✓ nom_etudiant column is now nullable")
        conn.commit()
    except Exception as e:
        print(f"✗ Error: {e}")
        conn.rollback()
        sys.exit(1)
