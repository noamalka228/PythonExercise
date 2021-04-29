from numpy import *
import functools
def exercise1_a():
    sum = 0
    number = input("Enter a number (stop to end)\n")
    while number.lower() != "stop": # checks upper and lower case letters: for example convert STOP to stop
        sum = sum + int(number) # casting the char to int
        number = input("Enter a number (stop to end)\n") # keep getting input from user
    print(sum)

def exercise1_b():
    sum=0
    my_list = input("Enter a list of numbers (press enter to end): ").split(',') # getting list input from user using ',' to split items
    for i in my_list: # using foreach to check all items in the list
        sum = sum+int(i) # casting each item to int
    print(sum)

def exercise2(matrix):
    # check horizontal lines for player1
    if((matrix[0][0]==matrix[0][1]==matrix[0][2]==1) or (matrix[1][0]==matrix[1][1]==matrix[1][2]==1)
        or (matrix[2][0]==matrix[2][1]==matrix[2][2]==1)):
        print("player 1 wins")
    # check vertical lines for player1
    elif ((matrix[0][0] == matrix[1][0] == matrix[2][0] == 1) or (matrix[0][1] == matrix[1][1] == matrix[2][1] == 1)
        or (matrix[0][2] == matrix[1][2] == matrix[2][2] == 1)):
        print("player 1 wins")
    # check crosses for player1
    elif ((matrix[0][0] == matrix[1][1] == matrix[2][2] == 1) or (matrix[0][2] == matrix[1][1] == matrix[2][0] == 1)):
        print("player 1 wins")

    # check horizontal lines for player2
    elif ((matrix[0][0] == matrix[0][1] == matrix[0][2] == 2) or (matrix[1][0] == matrix[1][1] == matrix[1][2] == 2)
       or (matrix[2][0] == matrix[2][1] == matrix[2][2] == 2)):
        print("player 2 wins")
    # check vertical lines for player2
    elif ((matrix[0][0] == matrix[1][0] == matrix[2][0] == 2) or (matrix[0][1] == matrix[1][1] == matrix[2][1] == 2)
        or (matrix[0][2] == matrix[1][2] == matrix[2][2] == 2)):
        print("player 2 wins")
    # check crosses for player2
    elif ((matrix[0][0] == matrix[1][1] == matrix[2][2] == 2) or (matrix[0][2] == matrix[1][1] == matrix[2][0] == 2)):
        print("player 2 wins")
    # if non of the checks is true, the game represents a draw
    else:
        print("it's a draw")

def exercise3():
    i=0
    count = 1
    new_string = ""
    original_string = input("Enter a string: ")
    # checking all the string except from the last letter, unless it is the same as the one before it
    while i < len(original_string)-1:
        if original_string[i] == original_string[i + 1]: # increasing the counter when there are 2 duplicate letters
            count=count+1
        else: # when we reach a letter that is not equal to the one before, adding the sequence to the new string
            new_string += original_string[i]
            new_string += str(count)
            count = 1 # reset the counter
        i=i+1
    # adding the last sequence or letter to the new string
    new_string += original_string[i]
    new_string += str(count)
    print("The shorter string is: "+new_string)

def exercise4():
    i=0
    sum=0
    id=input("Enter id number: ")
    while i < len(id)-1: # adding to the sum all the digits except for the last number
        if i%2==0: # if i is even, add it to the sum
            sum+=int(id[i])
        else: # if i is odd, multiply the digit by 2
            if 2*int(id[i])<10:
                sum+=2*int(id[i])
            else: # if the answer after multiplying by 2 is bigger than 10, sum the digits
                j=2*int(id[i])
                sum+=j%10+j//10
        i=i+1
    k=sum+(10-sum%10) # round the sum up
    print(int(id[i])==k-sum) # check if the last digit is valid

# the function that can be replaced. i chose to square each item in the list
def squared(num):
    return pow(num, 2)

# the map function receives a function and a list as parameters and executing the function on each item in the list
def map(func, list):
    return [func(item) for item in list] # returning the new list after we executed the function on its items


def main():
    #exercise1_a()
    #exercise1_b()
    #mat = array([[2, 2, 0],
                 #[2, 1, 0],
                 #[2, 1, 0]])

    #exercise2(mat)
    my_string='aaa'
    #exercise3()
    #exercise4()

    #exercise5
    list=[10,20,30]
    print("The original list: ")
    print(list)
    list=map(squared,list) # to run another function on the list, define a new function and send it to the map function
    print("The list after the map function: ")
    print(list)


if __name__ == '__main__':
    main()




