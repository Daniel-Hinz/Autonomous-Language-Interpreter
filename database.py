import dataset
import hashlib
import os
import codecs
import string
import random


#######################################################
## Connect to database
db = dataset.connect("mysql://root:@localhost/ali")

## Create a reference to table 'sessions'
users_table = db["users_table"]
companies   = db["companies"]
chart_table = db["chart_table"]
sessions    = db["sessions"]

## creates a company ID
def companyIdGenerator(size=4, uchars=string.digits):
    return ''.join(random.choice(uchars) for _ in range(size))

## if at the very least, just have ALI in the database
if(companies.__len__()== 0):
     companies.insert({
        "company_id": "0001",
        "company_name": "ALI",
        "company_key": "123thjmv79cdfj3ki5tye",
    })


#######################################################
## Finds user through the username inside of database, otherwise return null
def getUser(username):
    try:
        user = list(users_table.find(username=username))
        username = user[0].get("username")
        password = user[0].get("password")
        company = user[0].get("company_name")
        data = {"username": username, "password": password, "company_name": company}
        return data

    except: 
        data = {"username": '', "password": '', "company_name": ''}
        return data


#######################################################
## saves user into database
def saveUser(data):
    assert type(data) is dict
    users_table.insert({
        "username": data["username"],
        "password": data["password"],
        "company_name": data["company_name"]
    })
    return


#######################################################
## Saves company into database
def saveCompany(data):
    assert type(data) is dict

    companies.insert({
        "company_id": data["company_id"],
        "company_name": data["company_name"],
        "company_key": data["company_key"]
    })
    return


#######################################################
## Checks to see if user is an Admin
def isAdmin(username):
    return True if username == "admin" else False


#######################################################
## Function to hash password
def generateCredentials(Userpassword):
    salt = os.urandom(32)
    key  = hashlib.pbkdf2_hmac("sha256",  Userpassword.encode("utf-8"), salt,  100000)

    return '{"salt": "' + str(bytesToString(salt)) + '", "key": "' + str(bytesToString(key)) + '"}'


#######################################################
## Helper function for hashing process
def bytesToString(byte):
    string = str(codecs.encode(byte, "hex"), "utf-8") 
    assert type(string) is str 
    return string


#######################################################
## Helper function for hashing process
def stringToBytes(string):
    byte = codecs.decode(bytes(string, "utf-8"), "hex")  
    assert type(byte) is bytes  
    return byte