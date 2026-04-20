import os
from dotenv import load_dotenv

load_dotenv()

# Caminho da raiz do projeto (onde está o .env)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Caminho do dataset, resolvendo relativo ao BASE_DIR
BASE_PATH = os.path.join(BASE_DIR, os.getenv("BASE_PATH"))

# Caminho do dataset, resolvendo relativo ao BASE_DIR
BASE_PATH_OS = os.path.join(BASE_DIR, os.getenv("BASE_PATH_OS"))

# Lista de cenários
SCENARIOS = os.getenv("SCENARIOS").split(",") if os.getenv("SCENARIOS") else []
