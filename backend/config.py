import os
from pathlib import Path
from dotenv import load_dotenv
import tempfile

load_dotenv()

# Chemin racine du projet
PROJECT_ROOT = Path(__file__).parent.parent

# Database
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost/stage_manager"
)

# Admin credentials
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

# Excel file paths
# Template en lecture seule (source) - à la racine du projet
EXCEL_TEMPLATE_PATH = str(PROJECT_ROOT / "fiches_stages.xlsx")
# Fichier de sortie (destination) - dans /tmp pour éviter les problèmes de permissions
EXCEL_FILE_PATH = os.path.join(tempfile.gettempdir(), "fiches_stages.xlsx")

# CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
