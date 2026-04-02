#!/usr/bin/env python3
import sys
import os

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

from backend.db import engine
from sqlalchemy import inspect

inspector = inspect(engine)
print("Colonnes de fiches_stages:")
if 'fiches_stages' in inspector.get_table_names():
    for col in inspector.get_columns('fiches_stages'):
        print(f"  - {col['name']}: {col['type']}")
else:
    print("  Table fiches_stages n'existe pas!")

print("\nColonnes de etudiants:")
if 'etudiants' in inspector.get_table_names():
    for col in inspector.get_columns('etudiants'):
        print(f"  - {col['name']}: {col['type']}")
else:
    print("  Table etudiants n'existe pas!")
