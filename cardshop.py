import os

title = ("🏆 Welcome to the Ultimate Sports & Trading Cards Manager 🃏")
print(title)
print("     Keep track of your cards in a personal collection!")
print("+------------------------------------------------------------+")
class Card:
    def __init__(self, name, set_name, year, value):
        self.name = name
        self.set_name = set_name
        self.year = year
        self.value = value

    def __str__(self):
        return f"{self.name} - {self.year} {self.set_name} - ${self.value:.2f}"

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

    def save_to_file(self):
        with open('card_collection.txt', 'w') as file:
            for card in self.cards:
                file.write(f"{card.name} | Year: {card.year} | Set: {card.set_name} | "
                           f"Value: ${card.value:.2f}\n")
        print("Collection saved to 'card_collection.txt'.")

    def load_from_file(self):
        if os.path.exists('card_collection.txt'):
            with open('card_collection.txt', 'r') as file:
                for line in file:
                    # Strip any whitespace and split by ' | '
                    parts = line.strip().split(' | ')
                    if len(parts) == 4:
                        # Parse individual fields correctly
                        name_part = parts[0]
                        year_part = parts[1].replace("Year: ", "")
                        set_part = parts[2].replace("Set: ", "")
                        value_part = parts[3].replace("Value: $", "")

                        try:
                            year = year_part.strip()
                            value = float(value_part.strip())
                            card = Card(name_part.strip(), set_part.strip(), year, value)
                            self.cards.append(card)
                        except ValueError:
                            print("Error loading card data; skipping entry.")
            print("Loaded existing collection from 'card_collection.txt'.")
        else:
            print("No existing collection found. Starting a new collection.")


def display_menu():

    print()
    print("  Please enter the correlating number")
    print("  to proceed in the selected option.")
    print()
    print("1. Add a Card")
    print("2. View Collection")
    print("3. Delete a Card")
    print("4. About")
    print("5. Quit")

def show_about():
    print("\n+------------------- About -------------------+")
    print("  Welcome to the Ultimate Sports & Trading")
    print("  Cards Manager! This program helps you")
    print("  keep track of your valuable trading card")
    print("  collection by allowing you to add, view,")
    print("  and delete cards from your personal list.")
    print()
    print("  Features:")
    print("  - Add new cards to your collection with")
    print("    detailed information such as name, set,")
    print("    year, and value.")
    print("  - View all your cards in a user-friendly")
    print("    format to easily track your collection.")
    print("  - Delete cards from your collection with")
    print("    a confirmation prompt to prevent accidental")
    print("    deletions.")
    print("  - Automatic saving and loading of your")
    print("    collection data to/from 'card_collection.txt'.")
    print()
    print("  This program is ideal for collectors,")
    print("  enthusiasts, or anyone looking to manage")
    print("  their trading card collection effectively.")
    print()
    print("  Credits:")
    print("  Developed by Richard Phan")
    print("  Inspired by the love for trading card collecting!")
    print()
    print("  For feedback or suggestions, please contact:")
    print("  phanri@oregonstate.edu")
    print("+--------------------------------------------+")


def main():
    collection = Collection()

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
            collection.view_cards()

        elif choice == "3":
            collection.view_cards()
            try:
                index = int(input("\nEnter the card number to delete: ")) - 1
                collection.delete_card(index)
            except ValueError:
                print("\nPlease enter a valid number.")

        elif choice == "4":
            show_about()

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("\nInvalid option, please try again.")


if __name__ == "__main__":
    main()