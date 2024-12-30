import mysql.connector as my
con = my.connect(host = "127.0.0.1",user = "root",password ="root",database = "banking_system")
#print(con)
cur = con.cursor() # Request Response

cur.execute("CREATE DATABASE if not exists banking_system")
user = """CREATE TABLE if not exists users(
            user_id int primary key auto_increment,
            name varchar(255) not null,
            account_number int(10) not null unique,
            dob date not null,
            city varchar(255),
            password varchar(255) not null,
            ini_balance int not null,
            mob int(10) not null unique,
            email varchar(255),
            address varchar(255)
            );"""
login = """CREATE TABLE if not exists login(
            account_number int(10) primary key,
            password varchar(255) not null,
            balance int not null,
            status boolean
            );"""
transaction = """CREATE TABLE if not exists transaction(
                transaction_id int primary key auto_increment,
                account_number int(10) not null,
                credit int,
                debit int
                );"""
cur.execute(user)
cur.execute(login)
cur.execute(transaction)

def addUser():
    name = input("Enter Name : ")
    account_number = int(input("Enter account_number : "))
    while account_number < 1000000000 and account_number > 9999999999:
        account_number = int(input("Enter valid account_number : "))
    balance = int(input("Enter starting balance more than 2000 : "))
    while balance < 2000:
        balance = int(input("Enter starting balance MORE THAN 2000 : "))

    ############################################################################################################################
    date = int(input("Enter date(only date) : "))
    while date > 31 or date <= 0:
        print("please enter date between 1 and 31")
        date = int(input("Enter date(only date) : "))
    month = int(input("Enter month(numeric) : "))
    while month >= 13 or month <= 0:
        month = int(input("enter a valid month"))
    if date == 31 and month == 4 or 6 or 9 or 11:
        print("These months only have 30 days")
        date = int(input("Enter date(only date) : "))
        while date >= 31 or date <= 0:
            print("please enter date between 1 and 31")
            date = int(input("Enter date(only date) : "))
        month = int(input("Enter month(numeric) : "))
            
    while month == 2 and date > 29:
        print("Its february you know ")
        while month >= 13 or month <= 0:
            month = int(input("enter a valid month"))
        while date == 31 and month == 4 or 6 or 9 or 11:
            print("These months only have 30 days")
            date = int(input("Enter date(only date) : "))
            while date >= 31 or date <= 0:
                print("please ener date between 1 and 31")
                date = int(input("Enter date(only date) : "))
                month = int(input("Enter month(numeric) : "))

        
    trie = 0
    yob = int(input("Enter yob(as yyyy) : "))
    while yob >= 2007 or yob < 1900:
        yob = int(input("Enter valid yob(as yyyy) : "))
        
        trie = trie + 1
        if trie == 2:
            print("Hey Child , you know you are not mature enough to do banking and stuffs")
            exit()

    while month == 2 and date > 28 and yob%4 != 0:
        print("Its not a leap year you know")
        while month >= 13 or month <= 0:
            month = int(input("enter a valid month"))
        while date == 31 and month == 4 or 6 or 9 or 11:
            print("These months only have 30 days")
            date = int(input("Enter date(only date) : "))
            while date >= 31 or date <= 0:
                print("please ener date between 1 and 31")
                date = int(input("Enter date(only date) : "))
                month = int(input("Enter month(numeric) : "))
    dob = f"{yob}-{month}-{date}"
    
    ############################################################################################################################    
    city = input("Enter city : ")
    mob = int(input("Enter mob : "))
    if mob < 1000000000 and mob > 9999999999:
        mob = int(input("Enter mob : "))
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
    vals = [name,account_number,dob,city,password,balance,mob,email,address]
    
    cur.execute(qnu,vals)
    status = True
    qnl = "insert into users(account_number,password,balance,status) values(%s,%s,%s,%s)"
    valslog = [account_number,password,balance,status]
    cur.execute(qnl,valslog)
        
def cBalance(account_number):
    try:
        qcb = f"select balance from login where account_number = {account_number}"
        cur.execute(qcb)
        result = cursor.fetchone()

        if result:
            balance = result[0]
            print(f"Balance for account {account_number}: {balance}")
        else:
            print(f"Account {account_number} not found.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
def debit(account_number):
    try:
        qcb = "select balance from login where account_number = %s"
        cur.execute(qcb,(account_number))
        result = cur.fetchone()

        if result:
            balance = result[0]
            
            debit = int(input("Enter the amount you want to debit : "))
            nb = balance - debit
            qdtt = "insert into transaction(account_number,debit) values(%s,%s)"
            cur.execute(qdtt,account_number,debit)
            qd = "update login set balance = %s where account_number = %s"
            cur.execute(qd,nb,account_number)
        else:
            print(f"Account {account_number} not found.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
def credit(account_number):
    try:
        qcb = "select balance from login where account_number = %s"
        cur.execute(qcb,(account_number))
        result = cur.fetchone()

        if result:
            balance = result[0]
            
            credit = int(input("Enter the amount you want to credit : "))
            nb = balance + credit
            qctt = "insert into transaction(account_number,credit) values(%s,%s)"
            cur.execute(qctt,account_number,credit)
            qc = "update login set balance = %s where account_number = %s"
            cur.execute(qc,nb,account_number)
        else:
            print(f"Account {account_number} not found.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
def transfer(account_number):
    try:
        qtf = "select balance from login where account_number = %s"
        cur.execute(qtf,(account_number))
        result = cur.fetchone()

        if result:
            balance = result[0]
            tfr = int(input("Enter the amount you want to transfer : "))
            nb = balance - tfr
            qdtt = "insert into transaction(account_number,debit) values(%s,%s)"
            cur.execute(qdtt,account_number,tfr)
            qd = "update login set balance = %s where account_number = %s"
            cur.execute(qd,nb,account_number)
            anacc = int(input("Enter the account number in which you wish to transfer : "))


            try:
                qaa = f"select balance from login where account_number = {nacc}"
                cur.execute(qaa)
                result = cursor.fetchone()

                if result:
                    balance1 = result[0]
                    
                    nb = balance + tfr
                    qctt = "insert into transaction(account_number,credit) values(%s,%s)"
                    cur.execute(qctt,account_number,credit)
                    qc = "update login set balance = %s where account_number = %s"
                    cur.execute(qc,nb,account_number)
                else:
                    print(f"Account {nacc} not found.")

            except mysql.connector.Error as err:
                print(f"Error: {err}")

            
            
        else:
            print(f"Account {account_number} not found.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
def translist(account_number):
    trlist = "select debit,credit from transaction where account_number = {account_number}"
    cur.execute(trlist)
    result = cur.fetchall()
    for i,j in result:
        print(f"debit = {i} , credit = {j}")
def updateP(account_number):
    print("What do you wish to update :/n1.Name/n2.DOB/n3.City/n4.Mobile/n5.Email/n6.Address")
    try:
        
        qcb = f"select {updatek} from login where account_number = %s"
        cur.execute(qcb,(account_number))
        result = cur.fetchone()

        if result:
            oldv = result[0]

            newv = int(input(f"the old {updatek} is {oldv}. New {updatek} is : "))
            
            qup = f"update login set {updatek} = %s where account_number = %s"
            cur.execute(qup,newv,account_number)
        else:
            print(f"Account {account_number} not found.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
def cpass(account_number):
    try:
        qp = "select password from login where account_number = %s"
        cur.execute(qp,(account_number))
        result = cur.fetchone()

        if result:
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
            
            
            qd = "update login set password = %s where account_number = %s"
            cur.execute(qd,nb,account_number)
        else:
            print(f"Account {account_number} not found.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
def activede(account_number):
    try:
        qad = f"select status from login where account_number = {account_number}"
        cur.execute(qad)
        result = cursor.fetchone()

        if result:
            status = result[0]
            if status == False:
                print("Deactive,To activate enter 1")
                sta = int(input())
                if sta == 1:
                    status == True
            if status == True:
                print("Deactive,To activate enter 1")
                sta = int(input())
                if sta == 1:
                    status == False
            
        else:
            print(f"Account {account_number} not found.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

def showDe(account_number):
    try:
        qp = "select name,account_number,dob,city,mob,email,address from users where account_number = %s"
        
        res = cur.execute(qp,(account_number))
        result = cur.fetchone()
        

        if result:
            for name,account_number,dob,city,mob,email,address in res:
                print("All details are as follows :/nName : {name}/nAccount_number : {account_number}/nDOB : {dob}/nCity : {city}/nMobile : {mob}/nEmail : {email}/nAddress : {address}")
                
        else:
            print(f"Account {account_number} not found.")
            
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    try:
        qcb = f"select balance from login where account_number = {account_number}"
        cur.execute(qcb)
        result = cursor.fetchone()

        if result:
            balance = result[0]
            print(f"Balance : {balance}")
        else:
            print(f"Account {account_number} not found.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    

    
            
def validatepassword(account_number,password):
    qvp = f"select password from login where account_number = {account_number}"
    cur.execute(qvr)
    vp = cur.fetchone()
    if vp:
        valid = vp[0]
        if valid == password:
            return True
        else:
            return False
    
        
def logout():
    exit()
def login():
    account_number = int(input("Enter account number : "))
    password = input("Enter your password")
    if validatepassword(account_number,password) == False:
        print("You Have Entered wrong password")
        password = input("Enter your password again : ")
        if validatepassword(account_number,password) == False:
            print("You Have Entered wrong password")
            password = input("Enter your password again : ")
            if validatepassword(account_number,password) == False:
                print("You have entered wrong password 3 times so the code is exiting")
                exit()
        
    transfer_list = []
    
    print(f"Welcome , {user}")
    print("1. Check balance/n2.Debit amount/n3.Credit amount/n4.Transfer amount/n5.Show transaction/n6.Change password/n7.Update profile/n8.Activate\/Deactivate account/n9.LogOut")
    opt = int(input())
    if opt == 1:
        cBalance(account_number)
    elif opt == 2:
        debit(account_number)
    elif opt == 3:
        credit(account_number)
    elif opt == 4:
        transfer(account_number)
    elif opt == 5:
        translist(account_number)
    elif opt == 6:
        cpass(account_number)
    elif opt == 7:
        updateP(account_number)
    elif opt == 8:
        activede(account_number)
    elif opt == 9:
        logout
    else:
        print("ENTER A VALID CHOICE")

print("""WELCOME,
1. LOGIN
1. ADD USER
2. SHOW USER 
4. EXIT
""")
c = input("CHOOSE AN OPTION : ")

if c == "1":
    print("WELCOME TO THE LOGIN PAGE")
    login()
elif c == "2":
    print("WELCOME TO THE REGISTRATION PAGE")
    addUser()
elif c == 3:
    showDe(account_number)
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
