import sqlite3
from hashlib import sha256

ADMIN_PASSWORD = "123456"

connect = input("Please key in your password?\n")

while connect != ADMIN_PASSWORD:
    connect = input("Please key in your password?\n")
    if connect == "q":
        break

def create_password(pass_key, service, admin_pass):
    return sha256(admin_pass.encode('utf-8') + service.lower().encode('utf-8') + pass_key.encode('utf-8')).hexdigest()[
           :15]  # the 15 is for tha amount of characters in the password

def get_hex_key(admin_pass, service):
    return sha256(admin_pass.encode('utf-8') + service.lower().encode('utf-8')).hexdigest()

conn = sqlite3.connect('pass_manager.db')

def get_password(admin_pass, service):
    secret_key = get_hex_key(admin_pass, service)
    cursor = conn.execute("SELECT * FROM KEYS WHERE PASS_KEY=" + '"' + secret_key + '"')

    pass_key = ""
    for row in cursor:
        pass_key = row[0]

    return create_password(pass_key, service, admin_pass)

def add_password(service, admin_pass):
    secret_key = get_hex_key(admin_pass, service)
    command = 'INSERT INTO KEYS (PASS_KEY) VALUES (%s);' %('"' + secret_key + '"')
    conn.execute(command)
    conn.commit()

    return create_password(secret_key, service, admin_pass)

if connect == ADMIN_PASSWORD:
    try:
        conn.execute('''CREATE TABLE KEYS
            (PASS_KEY TEXT PRIMARY KEY NOT NULL);''')
        print("Your safe has been created!\nWhat would you like to store in it today?")
    except:
        print("You have a safe, what would you like to store in it today?")

    while True:
        print('*' * 15)
        print("COMMANDS:")
        print("q = quit program")
        print("sp = store password")
        print("gp = get password")
        print('*' * 15)

        if input == "q":
            break
        if input == "sp":
            service = input("What is the name of the service?\n")
            print("\n" + service.capitalize() + " password created:\n" + add_password(service, ADMIN_PASSWORD))
        if input == "gp":
            service = input("What is the name of the service?\n")
            print("\n" + service.capitalize() + " password:\n" + get_password(ADMIN_PASSWORD, service))
