import zmq
import os
import csv

# Initialize ZeroMQ context and sockets for wishlist and user microservices
context = zmq.Context()
wishlist_socket = context.socket(zmq.REQ)
wishlist_socket.connect("tcp://localhost:5555")  # Wishlist microservice

user_socket = context.socket(zmq.REQ)
user_socket.connect("tcp://localhost:5556")  # User microservice

grading_socket = context.socket(zmq.REQ)
grading_socket.connect("tcp://localhost:5560")  # Connect to the card grading microservice

title = ("🏆 Welcome to the Ultimate Sports & Trading Cards Manager 🃏")
print(title)
print("     Keep track of your cards in a personal collection!")
print("+------------------------------------------------------------+")

# Card and Collection classes remain unchanged from the current code
class Card:
    def __init__(self, name, set_name, year, value, grade=None):
        self.name = name
        self.set_name = set_name
        self.year = year
        self.value = value
        self.grade = grade  # New attribute

    def __str__(self):
        grade_display = f" - Grade: {self.grade}" if self.grade else ""
        return f"{self.name} - {self.year} {self.set_name} - ${self.value:.2f}{grade_display}"

class Collection:
    def __init__(self):
        self.cards = []
        self.load_from_file()

    def add_card(self, card):
        self.cards.append(card)
        print(f"\nAdded {card.name} to the collection.")
        self.save_to_file()

    def view_cards(self):
        if not self.cards:
            print("\nThe collection is empty.")
        else:
            print("\nYour Trading Card Collection:")
            for i, card in enumerate(self.cards, 1):
                print(f"\n{i}. {card}")

    def delete_card(self, index):
        if 0 <= index < len(self.cards):
            card_to_delete = self.cards[index]
            confirm = input(f"\nAre you sure you want to delete '{card_to_delete.name}'? "
                            f"\n*Removing item will result in lost card data* (y/n): ").lower()

            if confirm == 'y':
                self.cards.pop(index)
                print(f"\nRemoved {card_to_delete.name} from the collection.")
                self.save_to_file()
            else:
                print("\nDeletion cancelled.")
        else:
            print("\nInvalid input. Please try again.")

    def add_card_to_wishlist(self, card):
        """Sends a request to add a card to the wishlist microservice."""
        wishlist_socket.send_json({
            'command': 'add',
            'name': card.name,
            'set_name': card.set_name,
            'year': card.year,
            'value': card.value
        })
        message = wishlist_socket.recv_string()
        print(message)

    def display_wishlist(self):
        """Requests and displays the wishlist."""
        wishlist_socket.send_json({'command': 'display'})
        message = wishlist_socket.recv_string()
        print(message)

    def save_to_file(self):
        with open('card_collection.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Year', 'Set', 'Value', 'Grade'])  # Add grade to header
            for card in self.cards:
                writer.writerow([card.name, card.year, card.set_name, card.value, card.grade])
        print("Collection saved to 'card_collection.csv'.")

    def load_from_file(self):
        if os.path.exists('card_collection.csv'):
            with open('card_collection.csv', 'r', newline='') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) >= 4:
                        try:
                            name = row[0].strip()
                            year = row[1].strip()
                            set_name = row[2].strip()
                            value = float(row[3].strip())
                            grade = row[4].strip() if len(row) > 4 and row[4].strip() else None
                            card = Card(name, set_name, year, value, grade)
                            self.cards.append(card)
                        except ValueError:
                            print("Error loading card data; skipping entry.")
            print("Loaded existing collection from 'card_collection.csv'.")
        else:
            print("No existing collection found. Starting a new collection.")

# New Login Feature
def login():
    """Login or create a new user profile."""
    print("\n+------------------- Login -------------------+")
    print("1. Log in")
    print("2. Create a new profile")
    print("+--------------------------------------------+")

    while True:
        choice = input("Enter your choice (1 or 2): ")

        if choice == "1":
            username = input("Enter your username: ").strip()
            user_socket.send_json({"command": "check_user", "username": username})
            response = user_socket.recv_string()
            if "exists" in response:
                print(f"Welcome back, {username}!")
                return username
            else:
                print(response)  # "User 'username' not found."

        elif choice == "2":
            username = input("Enter a new username: ").strip()
            user_socket.send_json({"command": "add_user", "username": username})
            response = user_socket.recv_string()
            print(response)  # "User 'username' created successfully."
            if "created" in response:
                return username

        else:
            print("Invalid choice. Please enter 1 or 2.")

def display_menu():
    print()
    print("  Please enter the correlating number")
    print("  to proceed in the selected option.")
    print()
    print("1. Add a Card Manually")
    print("2. Add Cards from a CSV File")
    print("3. View Collection")
    print("4. Delete a Card")
    print("5. Add Card to Wishlist")
    print("6. Display Current Wishlist")
    print("7. Grade a Card")  # New option
    print("8. About")
    print("9. Quit")

def show_about():
    print("\n+------------------- About -------------------+")
    print("  Welcome to the Ultimate Sports & Trading")
    print("  Cards Manager! This program helps you")
    print("  keep track of your valuable trading card")
    print("  collection by allowing you to add, view,")
    print("  and delete cards from your personal list.")
    print("  Developed by Richard Phan")
    print("+--------------------------------------------+")

def main():
    # Perform login first
    username = login()

    collection = Collection()
    print(f"\nHello, {username}! Let's manage your collection.")

    while True:
        display_menu()
        choice = input("\nEnter your choice: ")

        if choice == "1":
            name = input("Card Name: ")
            set_name = input("Set Name: ")
            year = input("Year: ")
            value = float(input("Price Acquired: $"))

            card = Card(name, set_name, year, value)
            collection.add_card(card)

        elif choice == "2":
            file_path = input("Enter the path to the CSV file: ")
            collection.add_cards_from_file(file_path)

        elif choice == "3":
            collection.view_cards()

        elif choice == "4":
            collection.view_cards()
            try:
                index = int(input("\nEnter the card number to delete: ")) - 1
                collection.delete_card(index)
            except ValueError:
                print("\nPlease enter a valid number.")

        elif choice == "5":
            name = input("Card Name: ")
            set_name = input("Set Name: ")
            year = input("Year: ")
            value = float(input("Value: $"))
            card = Card(name, set_name, year, value)
            collection.add_card_to_wishlist(card)

        elif choice == "6":
            collection.display_wishlist()


        elif choice == "7":
            collection.view_cards()  # Show the current collection for reference
            try:
                index = int(input("\nEnter the card number to grade: ")) - 1
                if 0 <= index < len(collection.cards):
                    selected_card = collection.cards[index]
                    print(f"Selected card: {selected_card}")
                    condition = float(input("Enter the card condition (1 to 10): "))

                    # Send request to grading microservice
                    grading_socket.send_json({
                        "card_name": selected_card.name,
                        "condition": condition
                    })
                    print("\nGrading in progress...")

                    response = grading_socket.recv_string()
                    print("\n" + response)

                    # Update and save the grade
                    grade = response.split(":")[-1].strip()  # Extract grade from response
                    selected_card.grade = grade
                    collection.save_to_file()
                else:
                    print("\nInvalid card number.")
            except ValueError:
                print("\nInvalid input. Please enter a number.")

        elif choice == "8":
            show_about()

        elif choice == "9":
            print("Goodbye!")
            break

        else:
            print("\nInvalid option, please try again.")

if __name__ == "__main__":
    main()
