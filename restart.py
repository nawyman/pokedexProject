"""
Author: Nick Wyman
Class: ISCS210 Python Programming
fileName: restartFunction.py
Description: Importable restart function

Algorithm:
Input:
Asking User if they'd like to run again using input() function
Processing:
Run the program again if the user inputs y
Else quit the program
Output:
If user doesn't restart the program, print("Have a Nice Day!") 
"""
def restart(function):
    goAgain  = input("Would you like to run the program again? y or n > ")
    if goAgain == "y":
        function()
    else:
        print("\nHave a Nice Day!")
        
