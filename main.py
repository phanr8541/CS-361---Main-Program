def main():
    # initialize card list
    cardList = []

    choice = 0
    while choice !=4:
        print("*** Sports & Trading Card Manager ***")
        print("1) Add a card")
        print("2) Lookup a card")
        print("3) Display cards collection")
        print("4) Quit")
        choice = int(input())

        if choice == 1:
            print("Adding a card...")
            nCard = input("Enter the name of the card >>>")
            nBrand = input("Enter the brand that created the card >>>")
            nYear = input("Enter the year of the card >>>")
            nCost = input("Enter the price the card was acquired >>>")
            cardList.append([nCard, nBrand, nYear, nCost])

        elif choice == 2:
            print("Looking up a card...")
            keyword = input("Enter Search Term: ")
            for card in cardList:
                if keyword in card:
                    print(card)

        elif choice == 3:
            print("Displaying all cards...")
            for i in range(len(cardList)):
                print(cardList[i])

        elif choice == 4:
            print("Quitting Program")

    print("Program Terminated!")

if __name__=="__main__":
    main()