from storage import initialize_storage
from config import FUEL_TYPES

from fuel_manager import (
    add_vehicle,
    view_vehicles,
    search_vehicle,
    add_fuel_record,
    view_fuel_history,
    update_fuel_record,
    delete_fuel_record,
    show_fuel_statistics
)

from utils import (
    get_valid_date,
    get_valid_number,
    get_valid_id,
    get_valid_fuel_type
)


def display_menu():
    print("\n========== PERSONAL VEHICLE FUEL TRACKER ==========")
    print("1. Add Vehicle")
    print("2. View Vehicles")
    print("3. Search Vehicle")
    print("4. Add Fuel Record")
    print("5. View Fuel History")
    print("6. Update Fuel Record")
    print("7. Delete Fuel Record")
    print("8. Fuel Statistics")
    print("9. Exit")
    print("===================================================")


def get_fuel_details():
    fuel_date = get_valid_date(
        "Enter fuel purchase date (YYYY-MM-DD): "
    )

    odometer = get_valid_number(
        "Enter odometer reading (km): ",
        minimum=0
    )

    quantity = get_valid_number(
        "Enter fuel quantity in litres or units: ",
        minimum=0.01
    )

    price_per_unit = get_valid_number(
        "Enter price per litre or unit (₹): ",
        minimum=0
    )

    station = input("Enter fuel station name: ").strip()
    notes = input("Enter notes: ").strip()

    return (
        fuel_date,
        odometer,
        quantity,
        price_per_unit,
        station,
        notes
    )


def main():
    initialize_storage()

    while True:
        display_menu()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            name = input("Enter vehicle name: ").strip()

            registration = input(
                "Enter registration number: "
            ).strip().upper()

            fuel_type = get_valid_fuel_type(FUEL_TYPES)

            if not name or not registration:
                print("Vehicle name and registration are required.")
                continue

            add_vehicle(name, registration, fuel_type)

        elif choice == "2":
            view_vehicles()

        elif choice == "3":
            keyword = input(
                "Enter vehicle name or registration: "
            ).strip()

            search_vehicle(keyword)

        elif choice == "4":
            vehicle_id = get_valid_id("Enter vehicle ID: ")

            details = get_fuel_details()

            add_fuel_record(vehicle_id, *details)

        elif choice == "5":
            vehicle_id = get_valid_id("Enter vehicle ID: ")
            view_fuel_history(vehicle_id)

        elif choice == "6":
            record_id = get_valid_id(
                "Enter fuel record ID to update: "
            )

            details = get_fuel_details()

            update_fuel_record(record_id, *details)

        elif choice == "7":
            record_id = get_valid_id(
                "Enter fuel record ID to delete: "
            )

            delete_fuel_record(record_id)

        elif choice == "8":
            show_fuel_statistics()

        elif choice == "9":
            print("Thank you for using Personal Vehicle Fuel Tracker!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
