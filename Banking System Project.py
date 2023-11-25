#!/usr/bin/env python
# coding: utf-8

# # Bank Management System Using Python

# In[1]:


# Import libraries
import random  # Library for random number generation
import csv  # Library for CSV file handling

# Define a User class to represent users
class User:
    def __init__(self, account_number, name, address, mobile, email, account_type, balance):
        # Initialize user attributes
        self.account_number = account_number
        self.name = name
        self.address = address
        self.mobile = mobile
        self.email = email
        self.account_type = account_type
        self.balance = balance
        self.transaction_history = []  # Store transaction history for each user

# Define a Bank class to handle banking operations
class Bank:
    def __init__(self):
        # Initialize bank attributes
        self.users = {}  # Dictionary to store users' information using their account numbers as keys
        self.admin_username = "admin"  # Admin username
        self.admin_password = "admin123"  # Admin password
        self.transaction_file = "D:/Python Project/transaction file.csv"  # Path to transaction file

    # Method to generate a unique account number
    def generate_account_number(self):
        while True:
            account_number = str(random.randint(10000, 99999))  # Generate a random account number
            if account_number not in self.users:  # Check if the account number is unique
                return account_number  # Return the unique account number

    # Method to create a new user account
    def create_account(self, user):
        account_number = self.generate_account_number()  # Generate a unique account number
        user.account_number = account_number  # Assign the generated account number to the user
        self.users[account_number] = user  # Add the user to the bank's user dictionary
        print(f"User created successfully. Account Number: {account_number}")  # Display success message

    # Method to deposit funds into a user's account
    def deposit(self, account_number, amount):
        if account_number in self.users:  # Check if the account exists
            # Update user's balance and transaction history
            self.users[account_number].balance += amount
            self.users[account_number].transaction_history.append(f"Deposited ${amount}")
            self.write_transaction_to_csv(account_number, f"Deposited ${amount}")  # Log the transaction

    # Method to withdraw funds from a user's account
    def withdraw(self, account_number, amount):
        if account_number in self.users:  # Check if the account exists
            if self.users[account_number].balance >= amount:  # Check if sufficient balance exists
                # Update user's balance and transaction history
                self.users[account_number].balance -= amount
                self.users[account_number].transaction_history.append(f"Withdrew ${amount}")
                self.write_transaction_to_csv(account_number, f"Withdraw ${amount}")  # Log the transaction
            else:
                print("Insufficient balance.")  # Display error message for insufficient balance

    # Method to transfer funds between two user accounts
    def transfer(self, from_account, to_account, amount):
        if from_account in self.users and to_account in self.users:  # Check if both accounts exist
            if self.users[from_account].balance >= amount:  # Check if sufficient balance in source account
                # Update balances and transaction history for both accounts
                self.users[from_account].balance -= amount
                self.users[to_account].balance += amount
                self.users[from_account].transaction_history.append(f"Transferred ${amount} to {to_account}")
                self.users[to_account].transaction_history.append(f"Received ${amount} from {from_account}")
                # Log the transactions for both accounts
                self.write_transaction_to_csv(from_account, f"Transferred ${amount} to {to_account}")
                self.write_transaction_to_csv(to_account, f"Received ${amount} from {from_account}")
            else:
                print("Insufficient balance.")  # Display error message for insufficient balance

    # Method to check the balance of a user's account
    def check_balance(self, account_number):
        if account_number in self.users:  # Check if the account exists
            return self.users[account_number].balance  # Return the balance of the account
        else:
            return None  # Return None if the account doesn't exist

    # Method to view transaction history for a specific account
    def view_transaction_history(self, account_number):
        if account_number in self.users:  # Check if the account exists
            user = self.users[account_number]  # Get the user object
            print(f"Transaction History for Account Number {account_number}:")
            for transaction in user.transaction_history:  # Iterate through transaction history
                print(transaction)  # Display each transaction

    # Method to view transaction history for all accounts (admin only)
    def admin_view_all_transaction_history(self):
        for account_number, user in self.users.items():  # Iterate through all accounts
            print(f"Transaction History for Account Number {account_number}:")
            for transaction in user.transaction_history:  # Iterate through transaction history of each account
                print(transaction)  # Display each transaction

    # Method to write transactions to a CSV file
    def write_transaction_to_csv(self, account_number, transaction):
        try:
            with open(self.transaction_file, mode='a', newline='') as file:
                writer = csv.writer(file)  # Create a CSV writer object
                writer.writerow([account_number, transaction])  # Write transaction details to the CSV file
        except Exception as e:
            print(f"Error writing to CSV file: {str(e)}")  # Display error message if writing fails

# Main function to run the banking system
def main():
    bank = Bank()  # Create an instance of the Bank class

    while True:
        print("\nBank Management System")
        print("1. Admin Login")
        print("2. User Login")
        print("3. Exit")
        choice = input("Enter your choice: ")  # Get user's choice

        if choice == "1":  # Admin login
            admin_username = input("Admin Username: ")  # Get admin username
            admin_password = input("Admin Password: ")  # Get admin password
            if admin_username == bank.admin_username and admin_password == bank.admin_password:  # Check credentials
                while True:
                    print("\nAdmin Menu")
                    print("1. Add User")
                    print("2. View All Transaction Histories")
                    print("3. Exit")
                    admin_choice = input("Enter your choice: ")  # Get admin's choice

                    if admin_choice == "1":  # Add a new user
                        name = input("Enter Name: ")
                        address = input("Enter Address: ")
                        mobile = input("Enter Mobile Number: ")
                        email = input("Enter Email: ")
                        account_type = input("Enter Account Type (Savings/Current/Deposit): ")
                        balance = float(input("Enter Initial Balance: "))
                        user = User(None, name, address, mobile, email, account_type, balance)  # Create a new user
                        bank.create_account(user)  # Add the user to the bank's records
                    elif admin_choice == "2":  # View all transaction histories
                        bank.admin_view_all_transaction_history()  # Display transaction history for all accounts
                    elif admin_choice == "3":  # Exit admin menu
                        break
                    else:
                        print("Invalid choice. Please try again.")  # Display message for invalid choice

        elif choice == "2":  # User login
            account_number = input("Enter Account Number: ")  # Get user's account number
            if account_number in bank.users:  # Check if the account exists
                while True:
                    print("\nUser Menu")
                    print("1. Deposit")
                    print("2. Withdraw")
                    print("3. Transfer")
                    print("4. Check Balance")
                    print("5. View Transaction History")
                    print("6. Exit")
                    user_choice = input("Enter your choice: ")  # Get user's choice

                    if user_choice == "1":  # Deposit funds
                        amount = float(input("Enter deposit amount: "))
                        bank.deposit(account_number, amount)  # Deposit funds into the user's account
                        print("Amount deposited successfully.")
                    elif user_choice == "2":  # Withdraw funds
                        amount = float(input("Enter withdrawal amount: "))
                        bank.withdraw(account_number, amount)  # Withdraw funds from the user's account
                        print("Amount withdrawn successfully.")
                    elif user_choice == "3":  # Transfer funds to another account
                        to_account = input("Enter recipient's account number: ")
                        amount = float(input("Enter transfer amount: "))
                        bank.transfer(account_number, to_account, amount)  # Transfer funds between accounts
                        print("Amount transferred successfully.")
                    elif user_choice == "4":  # Check account balance
                        balance = bank.check_balance(account_number)  # Get the user's account balance
                        print(f"Your account balance is: {balance}")  # Display the balance
                    elif user_choice == "5":  # View transaction history
                        bank.view_transaction_history(account_number)  # Display transaction history for the user's account
                    elif user_choice == "6":  # Exit user menu
                        break
                    else:
                        print("Invalid choice. Please try again.")  # Display message for invalid choice
            else:
                print("Invalid account number. Please try again.")  # Display message for invalid account number

        elif choice == "3":  # Exit the bank management system
            break
        else:
            print("Invalid choice. Please try again.")  # Display message for invalid choice

if __name__ == "__main__":
    main()  # Run the main function

