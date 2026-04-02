"""
Script d'initialisation des étudiants
À exécuter une seule fois pour créer les 27 étudiants dans la base de données
"""

from database import engine, SessionLocal
from models import Base, Etudiant

# Liste des 27 étudiants
ETUDIANTS = [
    "AMANI KOUASSI STEVEN",
    "ASSALE N'DAH JEAN",
    "BLE GAYE MARC DAVID",
    "COULIBALY NAHOUO ALBERT",
    "DEMBELE MADOUSSOU EUNICE",
    "EZIN ASSOUHAN DERIC STEPHANE",
    "FOFANA ISSOUF",
    "GOLITI BI MARC ANI KEVIN",
    "KAMATE FLAGNAN",
    "KANI EHOUMAN MATTHIAS",
    "KANTE YOUSSOUF AZIZ",
    "KOFFI ASSABA LINDA SEPHORA",
    "KONAN KONAN N'DRI ROMUALD",
    "KONE GNOUWETCHA ANGE",
    "KOUADIO AKOUA MATHANIA",
    "KOUAKOUSSUI YANN EZECHIEL AYMARD",
    "KOUAME SOURALEH JATHE",
    "LOBA EMMANUELLA VALENCIA",
    "M'BO MELVIN MARC EMMANUEL",
    "OFFO ANGE EMMANUEL",
    "OULE DESIRE-MARIE",
    "SORO FANNY AICHA",
    "SORO FOUNGNIGUE IVAN",
    "TOKAPIEU OUANGUI EZECHIEL",
    "YEBOUE KOUASSI EMMANUEL",
    "YEO YOMOYAHA",
    "ZIAO KOLO"
]

def init_etudiants():
    """Initialise la base de données avec les 27 étudiants"""
    
    # Créer les tables
    Base.metadata.create_all(bind=engine)
    
    # Obtenir une session
    db = SessionLocal()
    
    try:
        # Vérifier si les étudiants existent déjà
        count = db.query(Etudiant).count()
        if count > 0:
            print(f"✓ {count} étudiants existent déjà dans la base de données")
            return
        
        # Ajouter les 27 étudiants
        for nom in ETUDIANTS:
            etudiant = Etudiant(nom=nom)
            db.add(etudiant)
        
        db.commit()
        print(f"✓ {len(ETUDIANTS)} étudiants ajoutés à la base de données")
        
        # Afficher les IDs assignés
        etudiants = db.query(Etudiant).all()
        print("\nÉtudiants créés :")
        for e in etudiants:
            print(f"  ID {e.id}: {e.nom}")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Erreur lors de l'initialisation: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_etudiants()
