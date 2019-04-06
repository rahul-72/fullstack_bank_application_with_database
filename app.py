from flask import Flask, render_template, request, session
import json,time,os,sys,time     
from random import randint    #importing useful libraries....
import MySQLdb as sql
"""******************************************************************************"""

"""Creating app object and app.secret_key="toencryptyoursessiondata" is for session."""
app=Flask(__name__)
app.secret_key = "toencryptyoursessiondata"
 



""" ************************************************************************************ """
# creating functions for database
#creating 3 global functions so that we can use them in functions like debit, credit etc.
db=None
cursor=None
data=None
"""After the execution of db_execute_fetch function the value of data will be:

data= ('rahul123',
 'rahul',
 'charan',
 33000,
 '11100011100',
 'rahul456',
 'charan7rahul@gmail.com',
 2147483647)  
 
 means data will be in tuple form.
 """
def db_connection():
    global db,cursor
    db=sql.connect(host='localhost', port=3306, user='root', password='', database='xyz')
    cursor=db.cursor()
    

def db_execute_fetch(cmd):     
    """database ---->>>>> program"""
    global data
    cursor.execute(cmd)
    data=cursor.fetchone()

def db_execute_insert(cmd):       
    """database <<<<<<<-------- program"""
    cursor.execute(cmd)
    db.commit()

    

def db_close():
    global db,cursor,data
    cursor.close()
    db.close() 
    db=None
    cursor=None
    data=None

"""*****************************************************************************"""

"""In flask, first of all this route will initiate."""
@app.route('/')
def index():
    if 'username' in session:
        """If user exits then I am opening his file."""
        username=session['username']

        cmd=f"select * from bank where username='{username}'"
        db_connection()
        db_execute_fetch(cmd)


        name=data[1] + ' '+data[2]
        name=name.title()
        db_close()
        return render_template("login.html", title="Login", name=name)
        """render_template will take login.html file from the template folder."""

    else:    
        return render_template('index.html', title='XYZ Bank')

"""    *******************************************************************************"""   



@app.route('/login/', methods=["POST"])
# flask is coming to this route after clicking login buttom.
def login():
    """1st we will get username and password from
    request module and then we will check them in
    our database."""
    username=request.form["username"].strip().lower()
    password=request.form["password"]

    cmd=f"select * from bank where username='{username}'"
    db_connection()
    db_execute_fetch(cmd)
    if data:
        if password == data[5]:
            session['username']=username 
            """This is how we use session"""
            name=data[1] + ' ' +data[2]
            name=name.title()
            db_close()
            return render_template("login.html", title="Login", name=name, username=True)
        else:
            error="Invalid Password"
            return render_template("index.html", title="XYZ Bank", error=error)
    else:
        error="Username does not exits"
        return render_template("index.html", title="XYZ Bank", error=error)                      
            

""" **********************************************************************"""
                       
@app.route('/debit/')
def debit():
    return render_template('debit.html', title='Debit')


@app.route('/debit_amount/', methods=['POST'])
def debit_amount():
    amount=request.form['amount']
    amount=int(amount)

    username=session['username']

    cmd=f"select * from bank where username='{username}'"
    db_connection()
    db_execute_fetch(cmd)

    name=data[1] + ' '+data[2]
    name=name.title()
    username=session['username']

    if data[3] > amount:
        msg= f'Amount Rs {amount} are debited from your account'
        new_amount =data[3] -  amount
        cmd1=f"update bank set balance='{new_amount}' where username='{username}' "
        db_execute_insert(cmd1)
        db_close()
        return render_template('login.html', title='Login',name=name, msg=msg)
    else:
        msg='You does not have sufficient amount.'
        return render_template('login.html',title='Login', name=name, msg=msg)



"""       ***********************************************************************"""




@app.route('/credit/')
def credit():
    return render_template('credit.html', title='Credit')

@app.route('/credit_amount/', methods=['post'])
def credit_amount():
    amount=request.form['amount']
    amount=int(amount)

    username=session['username']

    cmd=f"select * from bank where username='{username}'"
    db_connection()
    db_execute_fetch(cmd)
    name=data[1] + ' '+data[2]
    name=name.title()
    new_amount=data[3]+amount
    cmd1=f"update bank set balance='{new_amount}' where username='{username}' "
    db_execute_insert(cmd1)
    db_close()
    msg=f'Amount Rs{amount} are credited to your account.'
    return render_template('login.html', title='Login',name=name, msg=msg)


"""**************************************************************************"""




@app.route('/balance_account/')
def balance_account():

    username=session['username']

    cmd=f"select * from bank where username='{username}'"
    db_connection()
    db_execute_fetch(cmd)
    balance=data[3]
    account_number=data[4]
    db_close()
    return render_template('balance_account.html', title='Balance_Account', balance=balance, account_number=account_number)


"""*****************************************************************************"""

@app.route('/profile/')
def profile():

    username=session['username']

    cmd=f"select * from bank where username='{username}'"
    db_connection()
    db_execute_fetch(cmd)
    name=data[1] + ' '+data[2]
    name=name.title()
    data_send=data
    db_close()
    return render_template('profile.html', title='Profile', data=data_send, name=name)


"""***********************************************************************************""" 


@app.route('/logout/')
def logout():
    session.clear()
    return render_template('index.html', title='XYZ Bank')



"""*************************************************************************************"""



@app.route('/signup/')
def signup():
    return render_template('signup.html', title='Signup')


@app.route('/mk_signup/', methods=['get','post'])
def mk_signup():

    if request.method == "POST" : 
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        username=request.form['username']
        phone_number=int(request.form['phone_number'])
        verify_password=request.form['verify_password']

        cmd=f"select * from bank where username='{username}'"
        db_connection()
        db_execute_fetch(cmd)
        
        if not data: 
            """The bank data of a particular user is in this form---->>>>>

{"first_name": "rahul", "last_name":"charan", "balance": 35000,
"account_number": "1001", "username":"rahul123", 
"password": "rahul456", "email":"charan7rahul@gmail.com"}  """
            if len(password)>=8:
            #checking whether password of length 8 or more or not.

                if password==verify_password:
                    #verifing password.

                    while True:
                        q,w,e,r,t,y,u,i,o,p,l=map(str,[randint(0,9) for i in range(11)])
                        """Assigning 11 random number to update
                        account-number in dictionary."""
                        a=q+w+e+r+t+y+u+i+o+p+l

                        cmd1="select * from bank where account_number='{a}'"
                        #Here I am not database' functions which I created above.
                        cursor.execute(cmd1)
                        data1=cursor.fetchall()
                        if data1:  
                            """checking whether a randomly generated account number is already
                            in bank dictionary or not."""
                            continue                   
                        else:
                            break



                    if len(str(phone_number))==10:
                        
                        """cheaking whether phone number is of 10 digits or not."""
                        cmd2=f"insert into bank values('{username}','{first_name}','{last_name}',0,'{a}','{password}','{email}','{phone_number}')"
                        db_execute_insert(cmd2)
                        db_close()
                        error = "Account Sucessfully Created Please Login"
                        return render_template("index.html",title="XYZ Bank",error=error)
                    else:
                        error="Only Enter 10 Digit Phone Number"
                        return render_template("index.html",title="XYZ Bank",error=error)

                else:
                    error="Password Verification is Failed."
                    return render_template('signup.html', title='signup', error=error)        

            else:
                error="Enter Password of Length 8 or more"
                return render_template('signup.html', title='Signup', error=error)
        else : 
            error = "User Already Exists... Login into your account"
            db_close()
            return render_template("index.html",title="XYZ Bank",error=error)

    else : 
         error = "GET Method Not Allowed Please Click Signup to create account"
         return render_template("index.html",title="XYZ Bank",error=error)



"""**************************************************************************************"""




if __name__=="__main__":
    app.run('localhost',5000,debug=True)
    """running it on localhost. One can run it on other host also."""