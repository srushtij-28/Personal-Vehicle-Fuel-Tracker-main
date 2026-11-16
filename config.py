from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

VEHICLES_FILE = DATA_DIR / "vehicles.json"
FUEL_FILE = DATA_DIR / "fuel_records.json"

FUEL_TYPES = [
    "Petrol",
    "Diesel",
    "CNG",
    "Electric"
]
