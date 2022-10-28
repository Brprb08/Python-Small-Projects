from curses.ascii import isdigit
import random
import time

# Global Constant
MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

# Set up a dictionary so that there are a random amount of symbols
# A is the best value
symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if(symbol != symbol_to_check):
                break
        # if break doesnt hit this else will run
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)
    
    return winnings, winning_lines


def get_slot_machine_spin(rows,cols,symbols):
    all_symbols = []
    #Loop through dictionary
    # .items gives the key and value of the dictionary
    for symbol, symbol_count in symbols.items():
        # _ is an empty variable so there is not an unused variable
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    # columns = [[], [], []]
    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:] # : means to copy list to current_symbols
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)
    
    return columns

def print_slot_machine(columns):
    for row in range(len(columns[0])):
        # Enumerate gives the index as well as the value of columns
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end = " | ")
            else:
                print(column[row], end="")
            #time.sleep(.25)

        print()

# Collects user input
def deposit():
    while True:
        amount = input("How much would you like to deposit? $")

        # Check to make sure amount is a number
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Amount must be greater than 0.\n")
        else:
            print("Please enter a number.\n")
    
    return amount

def get_number_of_lines():
    while True:
        lines = input("Enter the number of lines to bet on (1-" + str(MAX_LINES) + ")? ")

        # Check to make sure lines is a number
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Enter a valid number of lines.\n")
        else:
            print("Please enter a number of lines.\n")
    
    return lines

def get_bet():
    while True:
        amount = input("What would you like to bet on each line? $")

        # Check to make sure amount is a number
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Amount must be between ${MIN_BET} - ${MAX_BET}.\n")
        else:
            print("Please enter a number.\n")
    
    return amount

def spin(balance):
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
            print(f"You do not have enough to bet that amount, your current balance is ${balance}.")
        else:
            break

    print(f"You are betting ${bet} on {lines} lines. Total bet is equal to ${total_bet}.")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won ${winnings}.")
    # the * is an unpack which will print the list with spaces between
    (f"You won on lines: ", *winning_lines)
    return winnings - total_bet


def main():
    balance = deposit()
    while True:
        print(f"Current balance is ${balance}.")
        answer = input("Press enter to play (q to quit).")
        if(answer == "q"):
            break 
        if balance == 0:
            print("You are out of money.")
            re_deposit = input("Would you like to deposit more (only y for yes, anything else means no): ")
            if(re_deposit != "y"):
                break
            else:
                balance = deposit()
        balance += spin(balance)
    
    print(f"You left with ${balance}.")

    
for i in range(100):
    main()

