from flask     import render_template, request, redirect, session, Response
from database  import companies, saveUser, getUser, chart_table,isAdmin, db
from database  import generateCredentials, stringToBytes, companyIdGenerator, saveCompany
from translate import takeHomeTranslate, clearTextTags, clearHomeTags
from sessions  import app

import hashlib
import datetime
import time
import threading
import math
import random
import translate

#################################################################
# Home Page Route
@app.route("/home", methods=["GET", "POST"])
def homePage():
    
    if request.method == 'POST':
        patientName = request.form["name"]
        userNotes = request.form["notes"]
        highlights = request.form["highlights"]
        dateAndTime = str(datetime.datetime.now())
        date = dateAndTime[0:10]
        time = dateAndTime[11:19]
        username = session.get("username")
        
        # Insert user data into the database
        try:
            chart_table.insert({ 
                'username': username,
                'patient': patientName,
                'time' : time,
                'date' : date,
                'notes': userNotes,
                'time_stamp': dateAndTime,
                'highlights': highlights
            })
            
        # Throw 409 error if exception occurs
        except Exception as e:  
            return Response(e, status=409)
        
        # Redirect to the Homepage
        if session.get("username")  == "admin":
            return render_template("home.html", isAdmin = True)

        elif "username" not in session:
            return redirect("/")
        else:
            return render_template("home.html", isAdmin = False)

    # Default Home Page Route   
    else:
        if session.get("username") == "admin":
            return render_template("home.html", isAdmin = True)

        elif "username" not in session:
            return redirect("/")
        else:
            return render_template("home.html", isAdmin = False)


#################################################################
# Translation Route
@app.route("/translate", methods=["GET", "POST"])
def dynamic_page():
    if request.method == "POST":

        languageOne = request.form["languages1"]
        langaugeTwo = request.form["languages2"]

        if languageOne and langaugeTwo:
            session['languageOne'] = languageOne
            session['langaugeTwo'] = langaugeTwo

            l1 = session.get('languageOne')
            l2 = session.get('langaugeTwo')

            translate.main(languageOne, langaugeTwo) 
            return render_template("home.html", isAdmin = True) if session.get("username") == "admin" else render_template("home.html", isAdmin = False)

        else:
            return render_template("home.html", isAdmin = True, values = False) if session.get("username") == "admin" else render_template("home.html", isAdmin = False, values=False)

    else:
        return render_template("home.html", isAdmin == True) if session.get("username") == "admin" else render_template("home.html", isAdmin = False)
    

#################################################################
# Login Page Route
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def loginPage():

    # Handle login form
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = getUser(username)

        # Verify user account
        if not user or not verifyPassword(password, user["password"]):
            return render_template("login.html", failedLogin=True)
        
        # Create session
        if username not in session:
            session["username"] = username 

            # Redirect to home
            if(isAdmin(username)):
                 return render_template("home.html", isAdmin = True)  
            else:
                 return render_template("home.html", isAdmin = False) 

    # Default Login Route 
    else:
        return render_template("login.html", failedLogin=False)


#################################################################
# Signup Page Route
@app.route("/signup", methods=["GET", "POST"])
def signUpPage():
    
    if request.method == "POST":
        companyKey = request.form["companyKey"]
        username = request.form["username"]  
        password = request.form["password"]  
        passwordRepeat = request.form["password_again"]  

        # checking to see if username is already taken
        oldUser = getUser(username)
        oldName = str(oldUser["username"])

        if oldName.upper() == username.upper():
            return render_template("signup.html",
                invalidCode=False,
                notPasswordMatch=False,
                badUsername=True,
            )

        # Verify passwords match
        if (password != passwordRepeat):  
            if "username" not in session:
                session["username"] = username  

                return render_template("signup.html",
                    invalidCode=False,
                    notPasswordMatch=True,
                    badUsername=False,
                ) 

        companyInfo = list(companies.find(company_key=companyKey))

        # Check if company code exists
        try:
            companyName = companyInfo[0].get("company_name")
        except:
            return render_template("signup.html",
                invalidCode=True,
                notPasswordMatch=False,
                badUsername=False,
            ) 

        data = {  
            "username": username,
            "password": generateCredentials(password),
            "company_name": companyName,  
        } 

        # Save the users data
        saveUser(data)
      
        # Redirect to the homepage
        if "username" not in session:
            session["username"] = username              
        return redirect("/")

    # Default Signup Route
    else:
        return render_template("signup.html", invalidCode=False, notPasswordMatch=False, badUsername=False)


#################################################################
# Logout Page Route
@app.route("/logout", methods=["GET"])
def getLogout():
    clearHomeTags()
    session.pop("username", None)
    return redirect("/")  


#################################################################
# Signup Page Route
@app.route("/takehome", methods=["GET", "POST"])
def takehome():
    clearTextTags()
    if request.method == "POST":
        langaugeTwo = request.form["languages2"]
        text        = request.form["t1"]

        if langaugeTwo:
            session["textLanguage"] = langaugeTwo
            l2 = session.get("textLanguage")
            takeHomeTranslate(langaugeTwo, text)
            return render_template("takehome.html", isAdmin = True, l2 = l2) if session.get("username") == "admin" else render_template("takehome.html", isAdmin = False, l2 = l2)    
        else:
            return render_template("takehome.html", isAdmin = True, values = False) if session.get("username") == "admin" else render_template("takehome.html", isAdmin = False, values = False)    
                 
    else:
        return render_template("takehome.html", isAdmin = True) if session.get("username") == "admin" else render_template("takehome.html", isAdmin = False)


#################################################################
# Admin Page Route
@app.route("/admin", methods=["GET", "POST"])
def getAdmin():
    if request.method == 'POST':

        username = request.form["username"]
        password = request.form["password"]
        companyName = request.form["companyName"]
        companyID = request.form["companyID"]
        user = getUser(username) 

        # Verify user account is an admin one
        if username != "admin": 
            return render_template("admin.html", failedLogin = True, isAdmin = True, keyMade = False)
        if not verifyPassword(password, user["password"]):
            return render_template("admin.html", failedLogin = True, isAdmin = True, keyMade = False)

        # Generate key and id 
        key = generateKey(20) 
        if(companyID == ""): 
            companyID = companyIdGenerator()
        
        data = { 
            "company_id": companyID,
            "company_name": companyName,
            "company_key": key,
        }
        
        saveCompany(data) 
        return render_template("admin.html", failedLogin = False, isAdmin = True, keyMade = True, key = key)   
    else:
        return render_template("admin.html", failedLogin = False, isAdmin = True, keyMade = False)


#################################################################
# Chart Page Route
@app.route("/mychart")
def getChart():
    username = session.get("username") 

    itemsInChart = chart_table.find()
    itemsInChart = [ dict(x) for x in list(itemsInChart) if x['username'] == username ] 

    if session.get("username") == "admin": # admin check
        return render_template("chart.html", itemsInChart = itemsInChart, isAdmin = True)
    else:
       return render_template("chart.html", itemsInChart = itemsInChart, isAdmin = False) 


#################################################################
# Veryify password matches a users username
def verifyPassword(Userpassword, Usercredentials):
    
    # Hash and Salt the password variables
    if type(Usercredentials) == str:
        salt = stringToBytes(Usercredentials[10:74])
        key = stringToBytes(Usercredentials[85:149])
    else:
        salt = stringToBytes(Usercredentials["salt"]) 
        key = stringToBytes(Usercredentials["key"])  

    newKey = hashlib.pbkdf2_hmac("sha256", Userpassword.encode("utf-8"), salt, 100000)
    return newKey == key 


#################################################################
# Runs in the backgroud and deletes records that are 24 hours old
def background():
    minutes = 0
 
    while True:
        if minutes > 60:
            try:
                db.query('DELETE FROM chart_table WHERE time_stamp<=DATE_SUB(NOW(), INTERVAL 1 DAY);') #query to find old chart data(24 hours)
                db.commit()
                minutes = 0

            except: pass
        time.sleep(60)
        minutes = minutes + 1


#################################################################
# Generate Company Key
def generateKey(length): #function to generate company key
    result           = ''
    characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

    for i in range(length):
      result += characters[math.floor(random.randint(0, len(characters)-1))]
      
    return result


#################################################################
# Main driver code
if __name__ == "__main__":
    b = threading.Thread(name='background', target=background) #thread for deleting old chart data
    b.daemon = True
    b.start()

    app.run(host="localhost", port=8080, debug=True)









