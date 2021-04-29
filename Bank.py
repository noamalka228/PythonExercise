import sqlite3
import socket

con = sqlite3.connect('mydb.db')
cur = con.cursor()

# running steps:
# 1. run Database first.
# 2. run Bank
# 3. run Atm
# each run of the Database file deletes the Bank table contents.
# So running it once and then preforming only 2nd and 3rd steps is the optimal action.

# python interpreter 3.8
class Bank:
    # constructor
    def __init__(self, fortune, accounts):
        self.fortune=fortune
        self.accounts=accounts

    # adding an account to the bank, using a valid credentials that was sent by the client
    def add_account(self, account_num, name, pin, balance):
        cur.execute("INSERT INTO Bank (account_number, name, pin, balance) VALUES(?,?,?,?)"
                       ,(account_num, name, pin, balance))
        con.commit()
        print("New bank account has been created successfully!")

    # depositing money to the valid account number that was sent as parameter
    def deposit(self, account_num, amount):
        m="Success! account have deposited %d$." %amount
        result = cur.execute("SELECT * FROM Bank WHERE account_number=?", (account_num, )).fetchone()
        cur.execute("UPDATE Bank SET balance=? WHERE account_number=?", (result[3]+amount, account_num))
        con.commit()
        print(m)
        return m # returning the string and in the main sending it to the client

    # withdrawing money from the valid account number that was sent as parameter
    def withdraw(self, account_num, amount):
        m = "Error Occured!"
        result = cur.execute("SELECT * FROM Bank WHERE account_number=?", (account_num, )).fetchone()
        if amount > result[3]:
            m = ("Cant withdraw more than %d$!" %result[3])
        else:
            cur.execute("UPDATE Bank SET balance=? WHERE account_number=?", (result[3] - amount, account_num))
            con.commit()
            m = "Success! account have withdraw %d$." % amount
        print(m)
        return m # returning the string and in the main sending it to the client

    # checking if the user credentials are valid and exist in the Bank in order to log into their account
    def check_credentials(self, acc, pin_code):
        result = cur.execute("SELECT * FROM Bank WHERE account_number=? AND pin=?", (acc, pin_code)).fetchone()
        if result:
            return True
        return False

    # checking the balance of the account whom account number was sent as parameter
    def check_balance(self, account_num):
        result = cur.execute("SELECT * FROM Bank WHERE account_number=?", (account_num,)).fetchone()
        m = ("You have %d$ in your account" % result[3])
        print(m)
        return m # returning the string and in the main sending it to the client

def main():
    sum=0
    count=0
    action='0'
    msg = '''\nWelcome to the Noam's Bank!
Enter the code of the action you would like to execute:
1 = deposit
2 = withdraw
3 = check balance
4 = exit\n
The code: '''
    server_socket = socket.socket() # creating new socket
    server_socket.bind(('0.0.0.0',1729)) # setting it as the server and connect on port 1729
    server_socket.listen(1) # determing the number of clients connecting to the server
    (client_socket, client_address) = server_socket.accept() # establishing the connection between the client socket and address
    print("Client has entered")

    # printing all existing bank accounts
    print("All of the bank accounts:\n"
          "account_num | name | PIN | balance\n"
          "___________________________________")
    rows = cur.execute("SELECT * FROM Bank").fetchall()
    if rows:
        for row in rows:
            print(row)
            count+=1
            sum+=row[3]
    else:
        print("No bank accounts at the moment...")

    # creating new bank
    my_bank = Bank(sum, count)

    # as long as the sent action by the client is not 4 (exit), keep getting input from the client
    while True and action!='4':
        first_code = int(client_socket.recv(1024).decode()) # 1= log in, 2= create new account
        print("The code is: %d" %first_code)
        while True: # keep getting input from user until action=4
            if first_code==1:
                # receiving log in credentials from the client
                acc = client_socket.recv(1024).decode()
                print(acc)
                pin_code = client_socket.recv(1024).decode()
                print(pin_code)
                credentials = my_bank.check_credentials(acc, pin_code) # checking client credentials
                print(credentials)
                client_socket.send(bytes((str(credentials)).encode('utf-8'))) # letting the client know if credentials are valid
                if credentials == True:
                    # keep getting input from user until action=4
                    while action != '4':
                        client_socket.send(bytes((msg).encode('utf-8')))
                        action = client_socket.recv(1024).decode()
                        if action == '1': # deposit
                            amount = client_socket.recv(1024).decode()
                            if int(amount) > 0:
                                client_socket.send(bytes(my_bank.deposit(acc, int(amount)).encode('utf-8')))
                            else:
                                client_socket.send(bytes((msg).encode('utf-8')))
                        elif action=='2': # withdraw
                            amount = client_socket.recv(1024).decode()
                            if int(amount) > 0:
                                client_socket.send(bytes(my_bank.withdraw(acc, int(amount)).encode('utf-8')))
                            else:
                                client_socket.send(bytes((msg).encode('utf-8')))
                        elif action == '3': # check balance
                            client_socket.send(bytes(my_bank.check_balance(acc).encode('utf-8')))
                        elif action=='4': # exit
                            print("Goodbye!")
                            break
                        else: # not a number between 1-4 so print invalid input and show menu again
                            print("Invalid input!")
                            client_socket.send(bytes((msg).encode('utf-8')))
                    break # breaking the first While to exit the system
            else: # creating new account
                # getting new account valid credentials from the client
                print("Creating new account...")
                acc_num = int(client_socket.recv(1024).decode())
                print(acc_num)
                name = client_socket.recv(1024).decode()
                print(name)
                pin = client_socket.recv(1024).decode()
                print(pin)
                balance = client_socket.recv(1024).decode()
                print(balance)
                my_bank.add_account(acc_num, name, pin, balance) # creating the new account
                first_code = int(client_socket.recv(1024).decode())
                print("The code is: %d" % first_code)
    server_socket.close() # ending the session

if __name__ == '__main__':
    main()
