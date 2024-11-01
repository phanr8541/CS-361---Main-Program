title = ("🏆 Welcome to the Ultimate Sports & Trading Cards Manager 🃏")
print(title)
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

    def add_card(self, card):
        self.cards.append(card)
        print(f"\nAdded {card.name} to the collection.")

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
            else:
                print("\nDeletion cancelled.")
        else:
            print("\nInvalid index. Please try again.")


def display_menu():

    print()
    print("  Please enter the correlating number on each")
    print("  page to proceed in the selected option.")
    print()
    print("1. Add a Card")
    print("2. View Collection")
    print("3. Delete a Card")
    print("4. Quit")


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
            print("Goodbye!")
            break

        else:
            print("\nInvalid option, please try again.")


if __name__ == "__main__":
    main()