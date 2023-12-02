import pandas as pd
import os
import time
from datetime import datetime as dt, timedelta

#items = {
#    "username":[],
#    "name": [],
#    "description": [],
#    "price": [],
#    "endtime": []
#}

#itemsdf = pd.DataFrame(items)

def disptimeleft(end):
    
    curr = time.time()
    currdt = dt.fromtimestamp(curr)
    enddt = dt.fromtimestamp(end)
    
    dtime = {"before":[currdt,enddt], 'after':["",""]}
    temp = pd.DataFrame(dtime)
    temp["after"] = temp["before"].dt.round("S")
    
    delta =  temp.loc[1, 'after'] - temp.loc[0, 'after']
    
    timestr = str(delta)
    
    timestr = timestr[-8:]
    
    return timestr

itemsdf = pd.read_csv('items.csv')
solddf = pd.read_csv('sold.csv')
notsolddf = pd.read_csv('notsold.csv')
    
def AddUser(username, password):
    logindata = pd.read_csv('passwords.csv', index_col=[0])
    usernames = logindata["username"].tolist()
    if(username in usernames):
        print("Username already in use")
        return 0
    else:
        
        list = [username, password]
        print(list)
        logindata.loc[len(logindata)] = list
        logindata.to_csv('passwords.csv')

def checksold():

    for i in range(len(itemsdf)):
        currtime = time.time()
        currtime = dt.fromtimestamp(currtime)
        endtime =  dt.fromtimestamp(itemsdf.loc[i, 'endtime'])

        if (currtime > endtime) and (itemsdf.loc[i, 'username'] != itemsdf.loc[i, 'currbid']):
            itemsold(i)
        elif (currtime > endtime) and (itemsdf.loc[i, 'username'] == itemsdf.loc[i, 'currbid']):
            notsold(i)
        

def itemsold(index):
    
    global itemsdf
    
    solditem = []

    solditem = [itemsdf.loc[index, 'username'], itemsdf.loc[index, 'name'], itemsdf.loc[index, 'description'], itemsdf.loc[index, 'price'],itemsdf.loc[index, 'currbid']]
    
    solddf.loc[len(solddf)] = solditem
    
    itemsdf = itemsdf.drop(index)
    
    return ""

def notsold(index):
    
    global itemsdf
    
    notsolditem = []

    notsolditem = [itemsdf.loc[index, 'username'], itemsdf.loc[index, 'name'], itemsdf.loc[index, 'description'], itemsdf.loc[index, 'price'],itemsdf.loc[index, 'currbid']]
    
    notsolddf.loc[len(notsolddf)] = notsolditem
    
    itemsdf = itemsdf.drop(index)
    
    return ""
  
def additem(username):
    os.system('cls')
    itname = input("Please enter the items name: ")
    itdescp = input("Please enter a description for the item: ")
    itprice = int(input("Please enter the starting price you would wish to have for the item: "))
    currbid = username
    currtime = time.time()
    currdt = dt.fromtimestamp(currtime)
    endtime = currdt + timedelta(hours=24)
    endtime = endtime.timestamp()
    
    #timeleft = comptime(currtime, endtime)
    newrow = [username, itname, itdescp, itprice, endtime, currbid]
    

    itemsdf.loc[len(itemsdf)] = newrow
    #print(itemsdf)
    
    return ""

def resetbidtime(index):
    currtime = time.time()
    currdt = dt.fromtimestamp(currtime)
    endtime = currdt + timedelta(hours=24)
    endtime = endtime.timestamp()
    
    itemsdf.loc[index, 'endtime'] = endtime

def Login(username, password):
    logindata = pd.read_csv('passwords.csv', index_col=[0])
    usernames = logindata["username"].tolist()
    passwords = logindata["password"].tolist()
    try:
        
        x = usernames.index(username)
        if password == passwords[x]:
            return True
        else:
            print("Incorrect password")
            return False

    except ValueError:
       print("Incorrect username")
       return False

def searchbid():
    pass

def dispitem(df, index):
    
    disprow =[]
    
    endtime = df.loc[index, 'endtime']
    
    timeleft = disptimeleft(endtime)

    disprow = [df.loc[index, 'username'], df.loc[index, 'name'], df.loc[index, 'description'], df.loc[index, 'price'], timeleft]

    print("Uploaded by user: ", disprow[0], "\n" + disprow[1], "\nCurrent Bid: Rs." + str(disprow[3]), "\n" + disprow[2], "\nTime left until current bid expires: " + str(disprow[4]))

def dispitemsold(df, index):
    
    disprow =[]

    disprow = [df.loc[index, 'username'], df.loc[index, 'name'], df.loc[index, 'description'], df.loc[index, 'sellbid'], df.loc[index, 'currbid']]

    print("Uploaded by user: ", disprow[0], "\n" + disprow[1], "\nSelling Bid: Rs." + str(disprow[3]), "\n" + disprow[2], "\nItem was sold to user: " + str(disprow[4]))

def dispitemnotsold(df, index):
    
    disprow =[]

    disprow = [df.loc[index, 'username'], df.loc[index, 'name'], df.loc[index, 'description'], df.loc[index, 'price'], df.loc[index, 'currbid']]

    print("Uploaded by user: ", disprow[0], "\n" + disprow[1], "\nBid: Rs." + str(disprow[3]), "\n" + disprow[2], "\nItem was not sold")

def placebid(username):
    
    global itemsdf
    
    os.system('cls')
    whichitem = int(input("Enter the item number you would like to place a bid for: or enter -1 to exit: "))
    index = whichitem - 1
    
    if index == -2:
            return ""
        
    print("\n")
    dispitem(itemsdf, index)
    bid = int(input("\nEnter a bid that is higher than the current bid: "))
    
    if bid == -1:
            return ""
    
    while bid <= itemsdf.loc[index, 'price'] :
        bid = int(input("Invlaid bid\nEnter a bid that is higher than the current bid or enter -1 to exit: "))
        
        if bid == -1:
            return ""
        
    itemsdf.loc[index, 'price'] = bid
    itemsdf.loc[index, 'currbid'] = username
    
    resetbidtime(index)
    return ""

    
#dispitem(1)

x = True
while(x):
    os.system('cls')
    print("Welcome to Ebay")
    print("1. Login\n2. Signup\n3. Exit")
    #print(itemsdf)
    x = int(input("Enter your selection: "))
    match x:
        case 1:
            os.system('cls')
            usrinput = input("Please enter your username: ")
            passwd = input("Please enter your password: ")
            HasLoggedin = Login(usrinput, passwd)
            if(HasLoggedin):
                sent = True
                while(sent):
                    os.system('cls')
                    itemsdf.to_csv('items.csv', index = False)
                    solddf.to_csv('sold.csv', index = False)
                    notsolddf.to_csv('notsold.csv', index = False)
                    checksold()
                    print("Welcome", usrinput)
                    print("1. Sell an item\n2. Browse items on sale\n3. Your items\n4. Logout")
                    Input_Login = int(input("Enter your selection: "))
                    match Input_Login:
                        case 1:
                            additem(usrinput)
                            #print(itemsdf)
                        case 2:
                            os.system('cls')
                            
                            print("Items: ")
                            
                            for i in range(len(itemsdf)):
                                print("\n\nItem no." + str(i+1))
                                dispitem(itemsdf, i)
                                
                            nextmenu = int(input("\n\n1. Place a bid on an item\n2. Exit\nEnter your Selection: "))
                            match nextmenu:
                                case 1:
                                    placebid(usrinput)
                                case 2:
                                    pass
                        case 3:
                             os.system('cls')
                             
                             nextmenu2 = int(input("1. Sold Items\n2. Items Successfully bought\n3. Items failed to sell\n4. Items you have up for sale\n5. Exit\nEnter your Selection: "))
                             match nextmenu2:
                                case 1:
                                    os.system('cls')
                                    for i in range(len(solddf)):
                                        if (solddf.loc[i, 'username'] == usrinput):
                                            print("\nItem no." + str(i+1))
                                            dispitemsold(solddf, i)
                                        
                                    yes = input("\nEnter any key to go back: ")
                                case 2:
                                    os.system('cls')
                                    for i in range(len(solddf)):
                                        if (solddf.loc[i, 'currbid'] == usrinput):
                                            print("\nItem no." + str(i+1))
                                            dispitemsold(solddf, i)
                                        
                                    yes = (input("\nEnter any key to go back: "))
                                case 3:
                                    os.system('cls')
                                    for i in range(len(notsolddf)):
                                        if (notsolddf.loc[i, 'username'] == usrinput):
                                            print("\nItem no." + str(i+1))
                                            dispitemnotsold(notsolddf, i)
                                        
                                    yes = input("\nEnter any key to go back: ")
                                case 4:
                                    os.system('cls')
                                    for i in range(len(itemsdf)):
                                        if (itemsdf.loc[i, 'username'] == usrinput):
                                            print("\nItem no." + str(i+1))
                                            dispitem(itemsdf, i)
                                        
                                    yes = input("\nEnter any key to go back: ")
                                case 6:
                                    pass
                        case 4:
                            sent = False

                    os.system('cls')

            else:    
                print("Incorrect password")
                dum1 = input("Enter any key to return to the main menu: ")

        case 2:
            os.system('cls')
            usrinput = input("Please enter your username: ")
            passwd = input("Please enter your password: ")
            AddUser(usrinput,passwd)
            
        case 3:
            x = False
    os.system('cls')        
    
    
    
        