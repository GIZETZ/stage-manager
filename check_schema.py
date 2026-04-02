import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))
from db import engine, Session
from sqlalchemy import inspect, text

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
