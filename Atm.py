import socket
import random
import sqlite3

con = sqlite3.connect('mydb.db')
cur = con.cursor()

# python interpreter 3.8
class Atm:
    # constructor. responsible for maintaining the session
    def __init__(self):
        data_to_bank=""
        self.my_socket = socket.socket() # creating new socket
        # setting the server address as loopback because the server/client is on my computer and not remote one.
        # connecting the socket to the server (Bank) on port 1729
        self.my_socket.connect(('127.0.0.1', 1729))
        while True:
            try:
                # sending the code the the server
                code=input("Welcome to Noam's Bank!\nLogin = 1 Create new account = 2: ")
                if code=='1':
                    self.my_socket.send(bytes((code).encode()))
                    break
                elif code=='2':
                    # creating new account
                    self.my_socket.send(bytes((code).encode()))
                    while True:
                        # generating a random 6 digit number and checks if its available
                        account_number = random.randint(100000, 999999)
                        result = cur.execute("SELECT account_number FROM Bank WHERE account_number=?",
                                             (account_number,)).fetchone()
                        if result: # if not available, generate again
                            continue
                        break
                    self.my_socket.send(bytes((str(account_number)).encode())) # sending the account number to the server
                    print("Your account number is: %d" % account_number)
                    name = input("Enter the account owner name: ")
                    self.my_socket.send(bytes((name).encode())) # sending the account name to the server
                    while True:
                        # asking for a PIN code. if its not 4 digits long, ask for another one
                        pin = input("Enter PIN code (must be 4 digits only): ")
                        if len(pin) != 4:
                            print("Incorrect PIN!\n")
                        else:
                            try:
                                # checking if the PIN is consisted of digits only
                                check = int(pin)
                                if check < 0:
                                    print("Incorrect PIN!\n")
                                else:
                                    break
                            except:
                                print("Incorrect PIN!\n")
                    self.my_socket.send(bytes((pin).encode())) # sending the pin code to the server
                    while True:
                        # asking for a starting balance: it has to be positive number!
                        balance = input("Enter the amount of money you would like to deposit: ")
                        try:
                            if int(balance) <= 0:
                                print("Error! Must deposit positive amount!")
                            else:
                                break
                        except:
                            print("Incorrect amount!\n")
                    self.my_socket.send(bytes((balance).encode())) # sending the starting balance to the server
                    print("New bank account has been created successfully!")
                else:
                    print("Wrong input! Please try again")
            except:
                print("Wrong input! Please try again")

        # broke the while, and now logging in to any account based on credentials
        while True:
            acc = input("Enter your account number: ")
            pin = input("Enter your PIN: ")

            # sending the credentials to the bank
            self.my_socket.send(bytes((acc).encode()))
            self.my_socket.send(bytes((pin).encode()))
            from_bank = self.my_socket.recv(1024).decode() # receiving answer from the bank
            if from_bank == "True": # if account exists
                # as long as we dont press 4 (exit), keep getting input from user after every action
                while str(data_to_bank) != "4":
                    from_bank = self.my_socket.recv(1024).decode()
                    print(from_bank)
                    data_to_bank = input("")
                    self.my_socket.send(bytes((data_to_bank).encode())) # sending the code of the action to the bank
                    if data_to_bank=='1': # deposit
                        amount=self.check_amount(1)
                        self.my_socket.send(bytes(str(amount).encode())) # sending the amount to the bank
                        if amount!=-1: # if its valid amount, print the respond from the bank (Success message)
                            print(self.my_socket.recv(1024).decode())
                    elif data_to_bank=='2': # withdraw
                        amount = self.check_amount(2)
                        self.my_socket.send(bytes(str(amount).encode())) # sending the amount to the bank
                        if amount != -1: # if its valid amount, print the respond from the bank (Success message)
                            print(self.my_socket.recv(1024).decode())
                    elif data_to_bank=='3': # check balance
                        print(self.my_socket.recv(1024).decode())
                    elif data_to_bank!='4': # any other input (except from 4) is wrong input
                        print("Incorrect code entered! Please try again")
                break #getting here if 4 is pressed, ending the While
            else: # if doesnt exists, check again for credentials
                print("Incorrect credentials! Please try again")
        self.my_socket.close() # ending the session

    # checking the amount the user entered as an input to check if its a positive number
    def check_amount(self, flag):
        try:
            # for deposit
            if flag==1:
                amount = int(input("Enter amount to deposit in your account: "))
            else: # for withdraw
                amount = int(input("Enter amount to withdraw from your account: "))
            if amount <= 0:
                print("Error! Must deposit positive amount!")
            else:
                return amount
        except:
            print("Incorrect amount!\n") # if the amount is not a number
        return -1 # return -1 if the amount is not a positive number


def main():
    atm=Atm()

main()

