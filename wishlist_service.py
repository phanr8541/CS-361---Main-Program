import zmq
import csv
import os
import time



class WishlistService:
    def __init__(self, file_name="wishlist.csv"):
        self.file_name = file_name
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:5555")
        self.initialize_wishlist()

    def initialize_wishlist(self):
        if not os.path.exists(self.file_name):
            with open(self.file_name, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Name', 'Set', 'Year', 'Value'])  # Header for wishlist

    def add_card_to_wishlist(self, card_data):
        print("Processing request to add card to wishlist...")
        time.sleep(2)  # Add a 2-second delay to simulate processing times

        with open(self.file_name, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(card_data)

        print(f"Added card to wishlist: {card_data}")

    def listen(self):
        print("Wishlist service is listening for requests...")
        while True:
            message = self.socket.recv_json()
            card_data = [message['name'], message['set_name'], message['year'], message['value']]
            self.add_card_to_wishlist(card_data)
            self.socket.send_string("Card added to wishlist successfully!")


if __name__ == "__main__":
    service = WishlistService()
    service.listen()
