# Simple Banking System (Python)
# https://github.com/imprvhub/bankingsystem-jbrains
# Graduate Project Completed By Iván Luna, August 15, 2023
# For Hyperskill (Jet Brains Academy). Course: SQL With Python

import random
import sqlite3

db = sqlite3.connect('card.s3db')
sql = db.cursor()
sql.execute('''CREATE TABLE IF NOT EXISTS card
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT,
            pin TEXT,
            balance INTEGER DEFAULT 0)''')
db.commit()


def generator_card():
    card_number = str(random.randint(4000000000000000, 4000009999999999))
    if not check_luhn(card_number) or check_account(card_number):
        generator_card()
    print("Your card number:")
    print(card_number)
    pin_code = ''.join(str(random.randint(0, 9)) for _ in range(4))
    default_balance = 0
    sql.execute(f'INSERT INTO card (number, pin, balance) VALUES ({card_number}, {pin_code}, {default_balance})')
    db.commit()
    print("Your card PIN:")
    print(pin_code)
    main_menu()


def login():
    card_number = input("Enter your card number:")
    pin_code = input("Enter your PIN:")
    if check_account(card_number):
        if check_pin(card_number, pin_code):
            print("You have successfully logged in!")
            login_menu(card_number)
        pass
    print("Wrong card number or PIN!")
    main_menu()


def income(card_number):
    money = int(input('Enter income:'))
    sql.execute(f"UPDATE card SET balance=balance+{money} WHERE number={card_number}")
    db.commit()
    print('Income was added!')
    login_menu(card_number)


def transfer(card_number):
    print('Transfer')
    to_card = input('Enter card number:')
    if card_number == to_card:
        print("You can't transfer money to the same account!")
        login_menu(card_number)
    elif not check_luhn(to_card):
        print("Probably you made mistake in the card number. Please try again!")
        login_menu(card_number)
    elif not check_account(to_card):
        print("Such a card does not exist.")
        login_menu(card_number)
    transfer_money(card_number, to_card)


def transfer_money(from_card, to_card):
    money = int(input('Enter how much money you want to transfer:'))
    sql.execute(f'SELECT balance FROM card WHERE number = {from_card}')
    money_from_card = [int(i[0]) for i in sql.fetchall()]
    if money > money_from_card[0]:
        print('Not enough money!')
        login_menu(from_card)
    sql.execute(f"UPDATE card SET balance=balance+{money} WHERE number={to_card}")
    sql.execute(f"UPDATE card SET balance=balance-{money} WHERE number={from_card}")
    db.commit()
    print('Success!')
    login_menu(from_card)


def check_account(card_number):
    # sql.execute('SELECT number FROM card')
    list_cards = [x[0] for x in sql.execute("SELECT number FROM card")]
    if card_number in list_cards:
        return True
    return False


def check_pin(card_number, pin_code):
    sql.execute(f'SELECT pin FROM card WHERE number ={card_number}')
    pin = ''.join(sql.fetchone())
    if pin == pin_code:
        print(pin_code)
        return True
    return False


def check_luhn(card_number):
    last_digital = card_number[-1]
    card_number = card_number[:-1]
    sum_odd = 0
    for x in range(0, 15, 2):
        k = int(card_number[x]) * 2
        if k > 9:
            sum_odd += (k // 10 + k % 10)
        else:
            sum_odd += k
    sum_even = 0
    for y in range(1, 14, 2):
        sum_even += int(card_number[y])
    if last_digital == str((sum_odd + sum_even) % 10) == "0":
        return True
    elif last_digital == str(10 - (sum_odd + sum_even) % 10):
        return True
    return False


def close_account(card_number):
    sql.execute(f'DELETE FROM card WHERE number={card_number}')
    db.commit()
    main_menu()


def check_balance(card_number):
    sql.execute(f'SELECT balance FROM card WHERE number={card_number}')
    money = sql.fetchone()
    print(f'Balance: {money}')
    login_menu(card_number)


def login_menu(card_number):
    print("1. Balance \n2. Add income \n3. Do transfer \n4. Close account \n5. Log out \n0. Exit")
    action = input()
    if action == '1':
        check_balance(card_number)
    elif action == '2':
        income(card_number)
    elif action == '3':
        transfer(card_number)
    elif action == '4':
        close_account(card_number)
    elif action == '5':
        main_menu()
    sql.close()
    exit()


def main_menu():
    print('1. Create an account \n2. Log into account \n0. Exit')
    action = input()
    if action == "1":
        generator_card()
    elif action == "2":
        login()
    else:
        sql.close()
        exit()


main_menu()
