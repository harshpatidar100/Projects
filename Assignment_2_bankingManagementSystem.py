import mysql.connector as my

from datetime import datetime




con = my.connect(host = "127.0.0.1",user = "root",password ="root",database = "banking_system")

cur = con.cursor() # Request Response

cur.execute("CREATE DATABASE if not exists banking_system")
user = """CREATE TABLE if not exists users(
            user_id int primary key auto_increment,
            name varchar(255) not null,
            account_number varchar(10) not null unique,
            dob date not null,
            city varchar(255),
            password varchar(255) not null,
            ini_balance varchar(255) not null,
            mob varchar(10) not null unique,
            email varchar(255),
            address varchar(255)
            );"""
login = """CREATE TABLE if not exists login(
            account_number varchar(10) primary key,
            password varchar(255) not null,
            balance varchar(255) not null,
            status boolean
            );"""
transaction = """CREATE TABLE if not exists transaction(
                transaction_id int primary key auto_increment,
                account_number varchar(10) not null,
                credit int,
                debit int
                );"""
cur.execute(user)
cur.execute(login)
cur.execute(transaction)


def getUserDate(): 
    while True: 
        try: 
            date_str = input("Enter date (YYYY-MM-DD): ") 
            date_obj = datetime.strptime(date_str, "%Y-%m-%d") 
            return date_obj.strftime("%Y-%m-%d") # Return formatted string 
        except ValueError: 
            print("Invalid date format. Please use YYYY-MM-DD.")


def addUser():
    name = input("Enter Name : ")
    account_number = input("Enter account_number : ")
    while len(account_number) != 10:
        account_number = input("Enter valid account_number : ")
    balance = input("Enter starting balance more than 2000 : ")
    while int(balance) < 2000:
        balance = input("Enter starting balance MORE THAN 2000 : ")

    


    
    dob = getUserDate()
    
    city = input("Enter city : ")
    mob = input("Enter mob : ")
    if len(mob) != 10:
        mob = input("Enter mob : ")
    email = input("Enter email : ")
    address = input("Enter address : ")
    password = input("Enter password : ")
    while password == None:
        print("password cannot be empty.")
        password = input("enter password again :")
    pa = input("Enter password again : ")
    while password != pa:
        print("both the passwords are not same")
        password = input("Enter password : ")
        pa = input("Enter password again : ")
    qnu = "insert into users(name,account_number,dob,city,password,ini_balance,mob,email,address) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    vals = (name,account_number,dob,city,password,balance,mob,email,address)
    
    cur.execute(qnu,vals)
    status = True
    qnl = "insert into login(account_number,password,balance,status) values(%s,%s,%s,%s)"
    valslog = (account_number,password,balance,status)
    cur.execute(qnl,valslog)
    con.commit()
        
def chkBalance(account_number):
    try:
        qcb = f"select balance from login where account_number = {account_number}"
        cur.execute(qcb)
        result = cur.fetchone()

        
        balance = result[0]
        print(f"Balance for account {account_number}: {balance}")
        

    except mysql.connector.Error as err:
        print(f"Error: {err}")
def debit(account_number):
    try:
        qcb = f"select balance from login where account_number = {account_number}"
        cur.execute(qcb)
        result = cur.fetchone()

        
        balance = result[0]
            
        debit = int(input("Enter the amount you want to debit : "))
        nb = int(balance) - debit
        qdtt = "insert into transaction(account_number,debit) values(%s,%s)"
        cur.execute(qdtt,(account_number,debit))
        qd = "update login set balance = %s where account_number = %s"
        cur.execute(qd,(nb,account_number))
        con.commit()
        

    except mysql.connector.Error as err:
        print(f"Error: {err}")


        
def credit(account_number):
    try:
        qcb = f"select balance from login where account_number = {account_number}"
        cur.execute(qcb)
        result = cur.fetchone()

        
        balance = result[0]
            
        credit = int(input("Enter the amount you want to credit : "))
        nb = int(balance) + credit
        qctt = "insert into transaction(account_number,credit) values(%s,%s)"
        cur.execute(qctt,(account_number,credit))
        qc = "update login set balance = %s where account_number = %s"
        cur.execute(qc,(nb,account_number))
        con.commit()
        

    except mysql.connector.Error as err:
        print(f"Error: {err}")
def transfer(account_number):
    try:
        qtf = f"select balance from login where account_number = {account_number}"
        cur.execute(qtf)
        result = cur.fetchone()

    
        balance = result[0]
        tfr = int(input("Enter the amount you want to transfer : "))
        nb1 = int(balance) - tfr
        qdtt = "insert into transaction(account_number,debit) values(%s,%s)"
        cur.execute(qdtt,(account_number,tfr))
        qd = f"update login set balance = {nb1} where account_number = {account_number}"
        cur.execute(qd)
        nacc = int(input("Enter the account number in which you wish to transfer : "))


        try:
            qaa = f"select balance from login where account_number = {nacc}"
            cur.execute(qaa)
            result = cur.fetchone()

            
            balance1 = result[0]
            
            nb2 = int(balance) + tfr
            qctt = "insert into transaction(account_number,credit) values(%s,%s)"
            cur.execute(qctt,(nacc,tfr))
            qc = f"update login set balance = {nb2} where account_number = {nacc}"
            cur.execute(qc)
            con.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        
            
        

    except mysql.connector.Error as err:
        print(f"Error: {err}")


        
def transList(account_number):
    trlist = f"select debit,credit from transaction where account_number = {account_number}"
    cur.execute(trlist)
    result = cur.fetchall()
    
    for i,j in result:
        print(f"debit = {i} , credit = {j}")


        
def updateProfile(account_number):
    selk = input("What do you wish to update :\n1.Name\n2.DOB\n3.City\n4.Mobile\n5.Email\n6.Address\n7.Cancel\n")
    while selk != 7:
        if selk == "1":
            updatek = "name"
            break
        elif selk == "2":
            updatek = "dob"
            break
        elif selk == "3":
            updatek = "city"
            break
        elif selk == "4":
            updatek = "mob"
            break
        elif selk == "5":
            updatek = "email"
            break
        elif selk == "6":
            updatek = "address"
            break
        elif selk == "7":
            return 0
        else:
            print("ENTER A VALID CHOICE")
    
    try:
        
        qcb = f"select {updatek} from users where account_number = {account_number}"
        cur.execute(qcb)
        result = cur.fetchone()

        
        oldv = result[0]


        if selk == "2":
            print(f"the old Date of Birth is {oldv}")
            newv = getUserDate()
            while oldv == newv:
                i = input("Both the old DOB and New DOB are same if you dont wish to change enter 1 or else enter anything else : ")
                if i == 1:
                    break
                else:
                    newv = getUserDate()

        else:
            newv = input(f"the old {updatek} is {oldv}. New {updatek} is : ")
            
            while oldv == newv:
                i = input(f"Both the old {updatek} that is {oldv} and New {updatek} are same if you dont wish to change enter 1 or else enter anything else : ")
                if i == 1:
                    break
                else:
                    newv = input(f"the old {updatek} is {oldv}. New {updatek} is : ")
            
            
        qup = f"update users set {updatek} = %s where account_number = {account_number}"

            
        cur.execute(qup,(newv,))
        con.commit()
        

    except mysql.connector.Error as err:
        print(f"Error: {err}")


    
def checkPass(account_number):
    try:
        qp = f"select password from login where account_number = {account_number}"
        cur.execute(qp)
        result = cur.fetchone()

        
        passwordd = result[0]

        password = input("Enter new password : ")
        while password == None:
            print("password cannot be empty.")
            password = input("enter password again :")
        while password == passwordd:
            print("old and new passwords cannot be same")
            password = input("Enter password : ")
            
        pa = input("Enter new password again : ")
        while password != pa:
            print("both the passwords are not same")
            password = input("Enter password : ")
            pa = input("Enter password again : ")
        
        
        qd = f"update login set password = {pa} where account_number = {account_number}"
        cur.execute(qd)
        con.commit()
        

    except mysql.connector.Error as err:
        print(f"Error: {err}")


def chkstatus(account_number):
    try:
        qst = f"select status from login where account_number = {account_number}"
        cur.execute(qst)
        result = cur.fetchone()
        status = result[0]
        if status == False:
            return False
        else:
            return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")

        
def activeDeactivate(account_number):
    try:
        status = chkstatus(account_number)
        if status == False:
            print("Deactive,To activate enter 1")
            sta = int(input())
            if sta == 1:
                qs = f"update login set status = TRUE where account_number = {account_number}"
                cur.execute(qs)
                con.commit()
                print("YOUR ACCOUNT HAS BEEN ACTIVATED")
        else:
            print("Active,To deactivate enter 1")
            sta = int(input())
            if sta == 1:
                qs = f"update login set status = FALSE where account_number = {account_number}"
                cur.execute(qs)
                con.commit()
                print("YOUR ACCOUNT HAS BEEN DEACTIVATED")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

def showDetails():

    account_number = input("Enter account number : ")
    if accountNum(account_number) == False:
        return False
    
    password = input("Enter your password : ")
    if validatepassword(account_number,password) == False:
        print("You Have Entered wrong password")
        password = input("Enter your password again : ")
        if validatepassword(account_number,password) == False:
            print("You Have Entered wrong password")
            password = input("Enter your password again : ")
            if validatepassword(account_number,password) == False:
                print("You have entered wrong password 3 times so the code is exiting")
                exit()

    
    try:
        qp = "select name,account_number,dob,city,mob,email,address from users where account_number = %s"
        
        cur.execute(qp,(account_number,))
        result = cur.fetchone()
        

        if result:
            list1 = list(result)
            name,account_number,dob,city,mob,email,address = list1
            print(f"All details are as follows :\nName : {name}\nAccount_number : {account_number}\nDOB : {dob}\nCity : {city}\nMobile : {mob}\nEmail : {email}\nAddress : {address}")
                
        else:
            print(f"Account {account_number} not found.")
            
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    try:
        qcb = f"select balance from login where account_number = {account_number}"
        cur.execute(qcb)
        result = cur.fetchone()

        
        balance = result[0]
        print(f"Balance : {balance}")
        

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    

    
            
def validatePassword(account_number,password):
    try:
        qvp = f"select password from login where account_number = {account_number}"
        cur.execute(qvp)
        vp = cur.fetchone()
        if vp:
            valid = vp[0]
            if valid == password:
                return True
            else:
                return False
    except mysql.connector.Error as err:
        print(f"Error: {err}")

        
def accountNum(account_number):
    try:
        qac = f"select account_number from login where account_number = {account_number}"
        cur.execute(qac)
        result = cur.fetchone()

        if result:
            return True
        else:
            print(f"{account_number} does not exists")
            return False
            

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        

        
def username(account_number):
    try:
        qu = f"select name from users where account_number = {account_number}"
        cur.execute(qu)
        result = cur.fetchone()

        
        username = result[0]
        return username
        

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
        

def login():
    account_number = input("Enter account number : ")
    if accountNum(account_number) == False:
        return False
    
    password = input("Enter your password : ")
    if validatePassword(account_number,password) == False:
        print("You Have Entered wrong password")
        password = input("Enter your password again : ")
        if validatePassword(account_number,password) == False:
            print("You Have Entered wrong password")
            password = input("Enter your password again : ")
            if validatePassword(account_number,password) == False:
                print("You have entered wrong password 3 times so the code is exiting")
                exit()
        
    
    userna = username(account_number)
    print(f"Welcome , {userna}")


    while True:    
        print("1. Check balance\n2.Debit amount\n3.Credit amount\n4.Transfer amount\n5.Show transaction\n6.Change password\n7.Update profile\n8.Activate\\Deactivate account\n9.LogOut")
        opt = int(input())
        status = chkstatus(account_number)
        if status == True:
            
            if opt == 1:
                chkBalance(account_number)
            elif opt == 2:
                debit(account_number)
            elif opt == 3:
                credit(account_number)
            elif opt == 4:
                transfer(account_number)
            elif opt == 5:
                transList(account_number)
            elif opt == 6:
                checkPass(account_number)
            elif opt == 7:
                updateProfile(account_number)
            elif opt == 8:
                activeDeactivate(account_number)
            elif opt == 9:
                return False
            else:
                print("ENTER A VALID CHOICE")
        else:
            if opt == 8:
                activeDeactivate(account_number)
            elif opt == 9:
                return False
            elif opt == 1 or 2 or 3 or 4 or 5 or 6 or 7:
                print("YOUR ACCOUNT IS NOT ACTIVE!\nPLEASE ACTIVATE YOUR ACCOUNT TO GAIN ACCESS TO SERVICES. ")
            else:
                print("ENTER A VALID CHOICE")
            


c = ""

while c != "4":

    print("""WELCOME,
    1. LOGIN
    2. ADD USER
    3. SHOW USER 
    4. EXIT
    """)
            
    c = input("CHOOSE AN OPTION : ")


    if c == "1":
        print("WELCOME TO THE LOGIN PAGE")
        if login() == False:
            continue
        
    elif c == "2":
        print("WELCOME TO THE REGISTRATION PAGE")
        addUser()

        
    elif c == "3":
        
        showDetails()

        
    elif c == "4":
        exit()

        
    else:
        print("ENTER A VALID CHOICE")



#######################################################################################################################
"""
BANKING SYSTEM
        1. ADD USER
              Create used with following fields:
                  a. name 
                  b. account number(random unique 10 digit)
                  c. dob
                  d. city 
                  e. password (proper validated password) 
                  f. initial balance(minimum 2000)
                  g. contact number 
                  h. Email ID 
                  i. Address
            (Perform all validation rule on fields such as: Name, Contact number, Email ID, Account Number, Password)
        2. SHOW USER (Display users information in proper format)
        3. LOGIN
            a. acc nu b. password
                i) show balance
                ii) show transaction
                iii) credit amount
                iv) Debit amount
                v) Transfer amount
                vi) Active/Deactive account
                vii) change password
                viii) update profile
                ix) Logout
        4. EXIT


        DataBase:
            DB NAME : banking_system
            Tables:
                    1) users
                    2) login
                    3) transaction
"""
