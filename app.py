from flask import Flask, render_template, request, session
import json,time,os,sys,time     
from random import randint    #importing useful libraries....

"""******************************************************************************"""

"""Creating app object and app.secret_key="toencryptyoursessiondata" is for session."""
app=Flask(__name__)
app.secret_key = "toencryptyoursessiondata"



current_path=os.getcwd()  
"""Always use current path so that this application 
    can run on other laptops also."""

bank_data=os.path.join(current_path,"static/data/bank")
bank_log_data=os.path.join(current_path,"static/data/bank_log")
"""Setting the path for the bank data and bank_log data."""


"""The bank data of a particular user is in this form---->>>>>

{"first_name": "rahul", "last_name":"charan", "balance": 35000,
 "account_number": "1001", "username":"rahul123", 
 "password": "rahul456", "email":"charan7rahul@gmail.com"}  """

""" ************************************************************************************ """


"""In flask, first of all this route will initiate."""
@app.route('/')
def index():
    if 'username' in session:
        """If user exits then I am opening his file."""
        username=session['username']
        file_name=os.path.join(bank_data, username)
        f=open(file_name)
        data=json.load(f)
        f.close()
        """loading and dumping his log file."""
        f=open(os.path.join(bank_log_data,username))
        log=json.load(f)
        f.close()
        log.append(time.ctime())

        f=open(os.path.join(bank_log_data,username),'r+')
        json.dump(log,f)
        f.close()

        name=data['first_name'] + ' '+data['last_name']
        name=name.title()
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
    for user in os.listdir(bank_data):
        """By this for loop I will get a list which contains
        name of files."""
        if username==user:
            f=open(os.path.join(bank_data,username))
            data=json.load(f)
            f.close()
            if password== data['password']:
                f=open(os.path.join(bank_log_data,username))
                log=json.load(f)
                f.close()
                log.append(time.ctime())

                f=open(os.path.join(bank_log_data,username),'r+')
                json.dump(log,f)
                f.close()
                
                session['username']=username 
                """This is how we use session"""
                name=data['first_name'] + ' ' +data['last_name']
                name=name.title()
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
    username=session["username"]
    f=open(os.path.join(bank_data,username))
    data=json.load(f)
    f.close()
    name=data['first_name'] + ' '+data['last_name']
    name=name.title()

    if data['balance'] > amount:
        msg= f'Amount Rs {amount} are debited from your account'
        data['balance'] -=amount
        json.dump(data, open(os.path.join(bank_data,username),'w'))
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
    username=session["username"]
    f=open(os.path.join(bank_data,username))
    data=json.load(f)
    f.close()
    name=data['first_name'] + ' '+data['last_name']
    name=name.title()

    data['balance']+=amount
    f=open(os.path.join(bank_data,username),'w')
    json.dump(data,f)
    f.close()
    msg=f'Amount Rs{amount} are credited to your account.'
    return render_template('login.html', title='Login',name=name, msg=msg)


"""**************************************************************************"""




@app.route('/balance_account/')
def balance_account():

    username=session["username"]
    f=open(os.path.join(bank_data,username))
    data=json.load(f)
    f.close()
    balance=data['balance']
    account_number=data['account_number']
    return render_template('balance_account.html', title='Balance_Account', balance=balance, account_number=account_number)


"""*****************************************************************************"""

@app.route('/profile/')
def profile():
    username=session["username"]
    f=open(os.path.join(bank_data,username))
    data=json.load(f)
    f.close()
    name=data['first_name'] + ' '+data['last_name']
    name=name.title()
    
    return render_template('profile.html', title='Profile', data=data, name=name)


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
        
        if username not in bank_data : 
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
                        for i in os.listdir(bank_data):
                            f=open(os.path.join(bank_data,i))
                            data=json.load(f)
                            f.close()
                            if data['account_number']==a:  
                                """checking whether a randomly generated account number is already
                                in bank dictionary or not."""
                                break                   
                            continue
                        else:
                            break



                    if len(str(phone_number))==10:
                        """cheaking whether phone number is of 10 digits or not."""
                        data = { 
                            'email':email,
                            'first_name':first_name,
                            'last_name':last_name,
                            'password':password,
                            'username':username,
                            'balance':0,
                            'account_number':a,
                            'phone_number':phone_number
                        }
                        """creating dictionary and dumping it ."""
                        f=open(os.path.join(bank_data,username),'w')
                        json.dump(data,f)
                        f.close()

                        log_list=[]
                        f=open(os.path.join(bank_log_data,username),'w')
                        json.dump(log_list,f)
                        f.close()

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
            return render_template("index.html",title="XYZ Bank",error=error)

    else : 
         error = "GET Method Not Allowed Please Click Signup to create account"
         return render_template("index.html",title="XYZ Bank",error=error)



"""**************************************************************************************"""




if __name__=="__main__":
    app.run('localhost',5000,debug=True)
    """running it on localhost. One can run it on other host also."""