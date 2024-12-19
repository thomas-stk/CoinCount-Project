import pandas as pd
import matplotlib.pyplot as plt
import os 
import sys 

coins_details = {("2", 20, 12.00, 120.00), ("1", 20, 8.75, 175.00), ("0.50", 10, 8.00, 160.00), ("0.20", 10, 5.00, 250.00), ("0.10", 5, 6.50, 325.00), ("0.05", 5, 2.35, 235.00), ("0.02", 1, 7.12, 356.00), ("0.01", 1, 3.56, 356.00)}
coin_types = {"2", "1", "0.50", "0.20", "0.10", "0.05", "0.02", "0.01"}

# Volunteer Name
def volunteer():
    while True:
        Name = str(input("\nPlease enter your name: "))
        if Name.isalpha() == True:
            print(f"Name: {Name.capitalize()}")
            break
        elif Name.isalpha() == False:
            print("Please enter a valid name.")
            
        else: 
            print("Invalid Name. Please try again.")
    return Name

# Type of coin being counted
def coin_type():
    global User_coin
    while True:
        print("\nCoin types: '£2', '£1', '50p or £0.50', '20p or £0.20', '10p or £0.10', '5p or £0.05', '2p or £0.02', '1p or £0.01'")
        User_coin = input("\nPlease enter a coin type from the list above: £")
        if User_coin in coin_types:
            print(f"\nCoin selected: £{User_coin}")
            # Confirming selected
            while True:
                confirm_coin = str(input("\nWould you like to confirm this coin type (y/n): "))
                if confirm_coin.lower() == "y":
                    print(f"Coin type confirmed.")
                    return User_coin
                    
                elif confirm_coin.lower() == "n":
                    break 
                else:
                    print("\nInvalid input, please enter 'y' or 'n'")               
        else:
            print("\nInvalid Coin type. Please try again.")
    
# Weight of their current bag
def coin_weight():
    global input_weight
    weight_needed = 0
    coins_needed = 0

    while True:
        try:
            # Checking if user has entered a valid weihgt
            input_weight = float(input("\nPlease enter the weight of your bag (grams): "))
            if input_weight >= 0:
                print(f"Current bag weight (g): {input_weight:.2f}")
                for i in coins_details:
                    if i[0] == User_coin:
                        coin_index = i
                total_weight = coin_index[3]
                global bag_value
                bag_value = coin_index[1]

                # If bag weight is equal to the total weight
                if total_weight == input_weight:
                    print(f"\nCoins counted correctly: {input_weight:.2f}g")
                    break
                    
                # If bag weight is more or less than the total weight
                else:
                    weight_needed = total_weight - input_weight 
                    one_coinweight = coin_index[2]
                    coins_needed = weight_needed / one_coinweight
                    coins_needed = int(coins_needed)

                    # Checks coins needed is an integer
                    if coins_needed == coins_needed:
                        global inaccuracy 
                        inaccuracy += 1
                    # How many coins user needs to add/remove to be correct
                        try:
                            if coins_needed > 0:
                                print(f"\nPlease add {coins_needed} coins, then re-weigh bag.")
                                
                            elif coins_needed < 0:
                                print(f"\nPlease remove {coins_needed * -1} coins, then re-weigh bag.")   
                                
                            else:
                                print("\nError. Please re-weigh your bag.")
                        except ValueError:
                            print("\nError. Please re-weigh your bag.")
                    else:
                        print("\nWrong coin. Please re-weigh your bag.")
                        

            # Input weight is less than 0
            elif input_weight < 0: 
                print("Invalid weight. Please try again.")
            else: 
                print("Please enter a valid weight.")
        except ValueError:
            print("\nError. Please enter a number for your weight.")

# Main program for coin count
def main_program():
    global inaccuracy
    inaccuracy = 0
    name = volunteer()
    users_coin = coin_type()
    weight_coin = coin_weight()
    # Checks if the file already exists
    file = "Volunteer table.csv"
    # Creates the csv file if it does not exist
    if not os.path.exists(file):
        # Column names for the csv
        columns = ['Name','Coin Type','Inaccuracy','Bag Value']
        # Creating an empty dataframe with the columns
        df = pd.DataFrame(columns=columns)
        # Writing the column names into a csv file
        df.to_csv("Volunteer table.csv", index=False)
    

    newLine = f"\n{name},{users_coin},{inaccuracy},{bag_value}"
    # Writes down the information entered by the user down into the csv file
    with open("Volunteer table.csv", 'a') as f:
        f.writelines([newLine])
    # Option to count more bags
    while True:
        count_more = input("\nWould you like to count another bag? (y/n): ")
        if count_more.lower() == "y":
            print(f"Option confirmed.")
            return main_program()
        elif count_more.lower() == "n":
            return Main_menu()
        else:
            print("\nInvalid input, please enter 'y' or 'n'")  


# Function to find the total bags counted by an individual
def individual_total():
    df = pd.read_csv("Volunteer table.csv")
    grouped = df.groupby("Name").agg({
        "Name": ["count"]
    })
    
    print(grouped.reset_index())
    # Asking if user wants to stay in this page or go back to menu
    while True:
        return_menu = str(input("\nWould you like to return to menu or see everyone's total (m/t): ")) 
        if return_menu.lower() == "m":
            return Main_menu()
        elif return_menu.lower() == "t":
            return everyone_total()
        else:
            print("Invalid input. Please enter 'm' or 't'.")

# Function for total bags counted by everyone
def everyone_total():
    df = pd.read_csv("Volunteer table.csv")
    bag = 0
    for i in df["Name"]:
        bag += 1
    print(f"\nTotal Bags Counted: {bag}")
    while True:
        return_menu = str(input("\nWould you like to return to menu or see individual total (m/i): "))
        if return_menu.lower() == "m":
            return Main_menu()
        elif return_menu.lower() == "i":
            return individual_total()
        else:
            print("Invalid input. Please enter 'm' or 'i'.")
            


# Function to view the total bags counted for the menu
def Total_bags():
    while True: 
        bags_counted = str(input("\nWould you like to see the total amount of bags counted by all volunteers (T) OR total counted by an individual (I): "))
        if bags_counted.upper() == "I":
            return individual_total()
        elif bags_counted.upper() == "T":
            return everyone_total()
        else:
            print("Invalid input, please enter a 'T' or an 'I'.")


# Function to showcase user's accuracy
def user_accuracy():
    df = pd.read_csv("Volunteer table.csv")
    accuracy = df.groupby("Name").agg(Count=('Inaccuracy', 'count'), Sum=('Inaccuracy', 'sum'))
    accuracy['Average Accuracy'] = (accuracy['Count'] - accuracy['Sum']) / accuracy['Count'] * 100
    print(accuracy)
    # Option to view barchart for user accuracy
    while True:
        show_graph = str(input("\nWould you like to view an accuracy bar graph (y/n): "))
        if show_graph.lower() == "y":
            print("\nGraph loading...\n")
            y = accuracy["Average Accuracy"]
            x = accuracy.index
            
            plt.bar(x, y, color="#085FFE", width=0.6)
            plt.xlabel("Volunteer Names")
            plt.ylabel("Accuracy in (%)")
            plt.title("Volunteer Accuracy Bar graph")
            plt.tight_layout()
            plt.show()
            return Main_menu()
        elif show_graph.lower() == "n":
            print("\nReturning to main menu...\n")
            return Main_menu()
        else:
            print("Invalid Input. Please enter a 'y' or 'n'.")

            

# Main menu for user to pick which task/activity they are doing.
def Main_menu():
    print("Menu:\n",
          "-------------"
          "\n 1. Weigh Coin Bag\n",
          "2. View Total Bags Counted\n",
          "3. View User's Accuracy\n",
          "4. Close program\n"  
          )
    # Validating user's choice in the menu
    while True:
        try:
            user_choice = int(input("Please enter a number between 1 - 4: "))
            if user_choice == 1:
                return main_program()
            elif user_choice == 2:
                return Total_bags()
            elif user_choice == 3:
                return user_accuracy()
            elif user_choice == 4:
                print("---------")
                print("Closing program....")
                sys.exit(0)
            else: 
                print("\nInvalid number please enter a number between 1 - 4.\n")
        except ValueError:
            print("\nError. Please enter a number. (1 - 4)\n")

Main_menu()

     


        

 
    



