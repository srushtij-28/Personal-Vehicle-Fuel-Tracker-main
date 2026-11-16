import json

from config import DATA_DIR, VEHICLES_FILE, FUEL_FILE


def initialize_storage():
    DATA_DIR.mkdir(exist_ok=True)

    for file_path in [VEHICLES_FILE, FUEL_FILE]:
        if not file_path.exists():
            file_path.write_text("[]", encoding="utf-8")


def load_data(file_path):
    initialize_storage()

    try:
        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []


def save_data(file_path, data):
    initialize_storage()

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_vehicles():
    return load_data(VEHICLES_FILE)


def save_vehicles(vehicles):
    save_data(VEHICLES_FILE, vehicles)


def load_fuel_records():
    return load_data(FUEL_FILE)


def save_fuel_records(records):
    save_data(FUEL_FILE, records)
