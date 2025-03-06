from faker import Faker
import json
import random

fake = Faker()

def generate_fake_data(num_entries=1):
    """Generates fake names, emails, and addresses."""
    data = []
    for _ in range(num_entries):
        entry = {
            "name": fake.name(),
            "email": fake.email(),
            "address": fake.address().replace('\n', ', '), 
        }
        data.append(entry)
    return data

def surprise_me():
    """Generates a random name."""
    return fake.name()

def export_to_json(data, filename="fake_data.json"):
    """Exports the generated data to a JSON file."""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Data exported to {filename}")


while True:
    print("\nFake Data Generator")
    print("1. Generate Data")
    print("2. Surprise Me! (Random Name)")
    print("3. Export to JSON")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        try:
            num = int(input("Enter number of entries: "))
            fake_data = generate_fake_data(num)
            print(json.dumps(fake_data, indent=4)) 
        except ValueError:
            print("Invalid input. Please enter a number.")
    elif choice == "2":
        print("Random Name:", surprise_me())
    elif choice == "3":
        if 'fake_data' in locals():
            export_to_json(fake_data)
        else:
            print("Generate data first.")
    elif choice == "4":
        break
    else:
        print("Invalid choice.")