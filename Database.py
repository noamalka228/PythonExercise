import sqlite3

con = sqlite3.connect('mydb.db')
cur = con.cursor()

# python interpreter 3.8
def main():
    try:
        # clears the table
        cur.execute("""DROP TABLE Bank""")
    except:
        pass
    try:
        # creates the table, giving its name and sets its columns and their type
        cur.execute(""" CREATE TABLE IF NOT EXISTS Bank (account_number integer, name text, pin text,
        balance integer);""")
        print("New Bank was created successfully!")
    except:
        print("Error occured!")

if __name__ == '__main__':
    main()
