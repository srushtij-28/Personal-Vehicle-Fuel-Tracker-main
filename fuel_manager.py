from datetime import date

from storage import (
    load_vehicles,
    save_vehicles,
    load_fuel_records,
    save_fuel_records
)


def find_vehicle(vehicle_id):
    vehicles = load_vehicles()

    for vehicle in vehicles:
        if vehicle["id"] == vehicle_id:
            return vehicle

    return None


def add_vehicle(name, registration, fuel_type):
    vehicles = load_vehicles()

    for vehicle in vehicles:
        if vehicle["registration"].lower() == registration.lower():
            print("\nThis registration number already exists.")
            return

    vehicle_id = max(
        [vehicle["id"] for vehicle in vehicles],
        default=0
    ) + 1

    vehicle = {
        "id": vehicle_id,
        "name": name,
        "registration": registration.upper(),
        "fuel_type": fuel_type,
        "created_date": date.today().isoformat()
    }

    vehicles.append(vehicle)
    save_vehicles(vehicles)

    print("\nVehicle added successfully!")
    print(f"Vehicle ID: {vehicle_id}")


def view_vehicles():
    vehicles = load_vehicles()

    if not vehicles:
        print("\nNo vehicles registered.")
        return

    print("\n" + "-" * 75)
    print(
        f"{'ID':<6} {'Vehicle':<22} "
        f"{'Registration':<20} {'Fuel Type':<15}"
    )
    print("-" * 75)

    for vehicle in vehicles:
        print(
            f"{vehicle['id']:<6} "
            f"{vehicle['name'][:21]:<22} "
            f"{vehicle['registration']:<20} "
            f"{vehicle['fuel_type']:<15}"
        )

    print("-" * 75)


def get_vehicle_records(vehicle_id):
    records = load_fuel_records()

    matching = [
        record for record in records
        if record["vehicle_id"] == vehicle_id
    ]

    return sorted(
        matching,
        key=lambda record: (record["date"], record["id"])
    )


def calculate_mileage(vehicle_id, record_id):
    records = get_vehicle_records(vehicle_id)

    previous_record = None
    current_record = None

    for index, record in enumerate(records):
        if record["id"] == record_id:
            current_record = record

            if index > 0:
                previous_record = records[index - 1]

            break

    if not current_record or not previous_record:
        return None

    distance = (
        current_record["odometer"]
        - previous_record["odometer"]
    )

    if distance <= 0 or current_record["quantity"] <= 0:
        return None

    return round(distance / current_record["quantity"], 2)


def add_fuel_record(vehicle_id, fuel_date, odometer,
                    quantity, price_per_unit, station, notes):

    vehicle = find_vehicle(vehicle_id)

    if not vehicle:
        print("\nVehicle ID not found.")
        return

    records = load_fuel_records()

    vehicle_records = get_vehicle_records(vehicle_id)

    if vehicle_records:
        latest = vehicle_records[-1]

        if odometer <= latest["odometer"]:
            print(
                "\nOdometer reading must be greater than "
                "the previous reading."
            )
            return

        if fuel_date < latest["date"]:
            print("Fuel date cannot be before the previous record.")
            return

    record_id = max(
        [record["id"] for record in records],
        default=0
    ) + 1

    record = {
        "id": record_id,
        "vehicle_id": vehicle_id,
        "date": fuel_date,
        "odometer": odometer,
        "quantity": quantity,
        "price_per_unit": price_per_unit,
        "total_cost": round(quantity * price_per_unit, 2),
        "station": station,
        "notes": notes
    }

    records.append(record)
    save_fuel_records(records)

    print("\nFuel record added successfully!")
    print(f"Total Cost: ₹{record['total_cost']:.2f}")

    mileage = calculate_mileage(vehicle_id, record_id)

    if mileage is not None:
        print(f"Estimated Mileage: {mileage} km per unit")
    else:
        print("Mileage will be available after another valid reading.")


def view_fuel_history(vehicle_id):
    vehicle = find_vehicle(vehicle_id)

    if not vehicle:
        print("\nVehicle ID not found.")
        return

    records = get_vehicle_records(vehicle_id)

    if not records:
        print("\nNo fuel records found for this vehicle.")
        return

    print(f"\nFuel History: {vehicle['name']}")
    print("-" * 105)

    print(
        f"{'ID':<5} {'Date':<13} {'Odometer':<13} "
        f"{'Quantity':<12} {'Price/Unit':<13} {'Total Cost':<13} {'Mileage':<12}"
    )

    print("-" * 105)

    for record in records:
        mileage = calculate_mileage(vehicle_id, record["id"])
        mileage_text = f"{mileage} km/unit" if mileage else "N/A"

        print(
            f"{record['id']:<5} "
            f"{record['date']:<13} "
            f"{record['odometer']:<13.1f} "
            f"{record['quantity']:<12.2f} "
            f"₹{record['price_per_unit']:<12.2f} "
            f"₹{record['total_cost']:<12.2f} "
            f"{mileage_text:<12}"
        )

    print("-" * 105)


def search_vehicle(keyword):
    vehicles = load_vehicles()
    keyword = keyword.lower()

    results = [
        vehicle for vehicle in vehicles
        if keyword in vehicle["name"].lower()
        or keyword in vehicle["registration"].lower()
    ]

    if not results:
        print("\nNo matching vehicles found.")
        return

    print("\nSearch Results:")

    for vehicle in results:
        print(
            f"\nID: {vehicle['id']}"
            f"\nVehicle: {vehicle['name']}"
            f"\nRegistration: {vehicle['registration']}"
            f"\nFuel Type: {vehicle['fuel_type']}"
        )


def update_fuel_record(record_id, fuel_date, odometer,
                       quantity, price_per_unit, station, notes):

    records = load_fuel_records()

    record = next(
        (item for item in records if item["id"] == record_id),
        None
    )

    if not record:
        print("\nFuel record ID not found.")
        return

    vehicle_records = sorted(
        [
            item for item in records
            if item["vehicle_id"] == record["vehicle_id"]
            and item["id"] != record_id
        ],
        key=lambda item: (item["date"], item["id"])
    )

    previous_records = [
        item for item in vehicle_records
        if (item["date"], item["id"]) < (fuel_date, record_id)
    ]

    next_records = [
        item for item in vehicle_records
        if (item["date"], item["id"]) > (fuel_date, record_id)
    ]

    if previous_records and odometer <= previous_records[-1]["odometer"]:
        print("Odometer must be greater than the previous reading.")
        return

    if next_records and odometer >= next_records[0]["odometer"]:
        print("Odometer must be less than the next reading.")
        return

    record["date"] = fuel_date
    record["odometer"] = odometer
    record["quantity"] = quantity
    record["price_per_unit"] = price_per_unit
    record["total_cost"] = round(quantity * price_per_unit, 2)
    record["station"] = station
    record["notes"] = notes

    save_fuel_records(records)

    print("\nFuel record updated successfully!")


def delete_fuel_record(record_id):
    records = load_fuel_records()

    updated_records = [
        record for record in records
        if record["id"] != record_id
    ]

    if len(updated_records) == len(records):
        print("\nFuel record ID not found.")
        return

    save_fuel_records(updated_records)

    print("\nFuel record deleted successfully!")


def show_fuel_statistics():
    vehicles = load_vehicles()
    records = load_fuel_records()

    if not vehicles:
        print("\nNo vehicles registered.")
        return

    print("\n========== FUEL STATISTICS ==========")

    for vehicle in vehicles:
        vehicle_records = get_vehicle_records(vehicle["id"])

        total_cost = sum(
            record["total_cost"] for record in vehicle_records
        )

        total_quantity = sum(
            record["quantity"] for record in vehicle_records
        )

        mileage_values = [
            calculate_mileage(vehicle["id"], record["id"])
            for record in vehicle_records
        ]

        valid_mileages = [
            value for value in mileage_values
            if value is not None
        ]

        average_mileage = (
            sum(valid_mileages) / len(valid_mileages)
            if valid_mileages else None
        )

        print(f"\nVehicle: {vehicle['name']}")
        print(f"Registration: {vehicle['registration']}")
        print(f"Fuel Records: {len(vehicle_records)}")
        print(f"Total Fuel: {total_quantity:.2f} units")
        print(f"Total Fuel Cost: ₹{total_cost:.2f}")

        if average_mileage is not None:
            print(f"Average Mileage: {average_mileage:.2f} km/unit")
        else:
            print("Average Mileage: Not available yet.")

    print("\nOverall Fuel Records:", len(records))
    print("=====================================")
