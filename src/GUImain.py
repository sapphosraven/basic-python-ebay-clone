
import pandas as pd
import os
import time
from datetime import datetime as dt, timedelta
import tkinter as tk
from tkinter import *
from tkinter import ttk

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
uname = ""
buyingitemindex = 0
    
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
  
def additem(username, itname, itdescp, itprice):
    currbid = username
    currtime = time.time()
    currdt = dt.fromtimestamp(currtime)
    endtime = currdt + timedelta(hours=24)
    endtime = endtime.timestamp()
    
    newrow = [username, itname, itdescp, itprice, endtime, currbid]
    

    itemsdf.loc[len(itemsdf)] = newrow


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

def additemtolistgui(df, index):
    
    disprow =[]
    
    endtime = df.loc[index, 'endtime']
    
    timeleft = disptimeleft(endtime)

    disprow = [df.loc[index, 'username'], df.loc[index, 'name'], df.loc[index, 'description'], df.loc[index, 'price'], timeleft]

    disprow[0] = "Uploaded by user: " + disprow[0]
    disprow[1] = "Item name: " + disprow[1]
    disprow[2] = "Description: " + disprow[2]
    disprow[3] = "Current Bid: Rs." + str(disprow[3])
    disprow[4] = "Time left until current bid expires: " + str(disprow[4])
    
    return disprow

def addsolditemtolistgui(df, index):
    
    disprow =[]

    disprow = [df.loc[index, 'username'], df.loc[index, 'name'], df.loc[index, 'description'], df.loc[index, 'sellbid'], df.loc[index, 'currbid']]

    disprow[0] = "Uploaded by user: " + disprow[0] 
    disprow[1] = "Item name: " + disprow[1]
    disprow[2] = "Description: " + disprow[2]
    disprow[3] = "Selling Bid: Rs." + str(disprow[3])
    disprow[4] = "Item was sold to user: " + str(disprow[4])
    
    return disprow

def addnotsolditemtolistgui(df, index):
    
    disprow =[]

    disprow = [df.loc[index, 'username'], df.loc[index, 'name'], df.loc[index, 'description'], df.loc[index, 'price'], df.loc[index, 'currbid']]

    disprow[0] = "Uploaded by user: " + disprow[0] 
    disprow[1] = "Item name: " + disprow[1]
    disprow[2] = "Description: " + disprow[2]
    disprow[3] = "Bid: Rs." + str(disprow[3])
    disprow[4] = "Item was not sold"
    
    return disprow

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

def clearFrame(frame):
    for widget in frame.winfo_children():
       widget.destroy()
       
    frame.pack_forget()
    
    
    
    
window = Tk()
mframe = Frame(window, bg = "#f7dcc1")
loginframe = Frame(window, bg = "#f7dcc1")
userwelcframe = Frame(window, bg = "#f7dcc1")
loginfailscrframe = Frame(window, bg = "#f7dcc1")
caccountframe = Frame(window, bg = "#f7dcc1")
additemframe = Frame(window, bg = "#f7dcc1")
youritemframe = Frame(window, bg = "#f7dcc1")
solditemsframe = Frame(window, bg = "#f7dcc1")
nsolditemsframe = Frame(window, bg = "#f7dcc1")
boughtitemsframe = Frame(window, bg = "#f7dcc1")
curritemsframe = Frame(window, bg = "#f7dcc1")
browseitemsframe = Frame(window, bg = "#f7dcc1")
bidframe = Frame(window, bg = "#f7dcc1")
bidfailframe = Frame(window, bg = "#f7dcc1")


"""
def bidfailscr():
    
    clearFrame(bidframe)
    
    errormessage = Label(bidfailframe, text = "The bid must be greater than the current bid\nPlease try again.", fg = "red", bg = "#f7dcc1", font = ("Helvetica, 24"))
    continuebutton = Button(bidfailframe, text = "Try again", fg = "black", bg = "white", font = ("Helvetica, 15"), command = placebidgui(buyingitemindex))
    
    errormessage.place(relx = 0.5, rely = 0.45, anchor = CENTER) 
    continuebutton.place(relx = 0.5, rely = 0.55, anchor = CENTER) 
    
    bidfailframe.pack(fill='both', expand= True, side = LEFT)
    window.attributes('-fullscreen', True)
    
"""

def checkbid(bid, temp):
        
        global uname
        global itemsdf
        
        index = int(temp)
        index -= 1
        
        if int(bid) > int(itemsdf.loc[index, 'price']):
           
            itemsdf.loc[index, 'price'] = bid
            itemsdf.loc[index, 'currbid'] = uname
            resetbidtime(index)
            
            successmessage = Label(bidframe, text = "Bid placed successfully, please go back", fg = "light green", bg = "#f7dcc1", font = ("Helvetica, 30"))
            successmessage.place(relx = 0.5, rely = 0.55, anchor = CENTER)
            
        else:
            successmessage = Label(bidframe, text = "Please go back and enter a bid greater than current bid", fg = "red", bg = "#f7dcc1", font = ("Helvetica, 30"))
            successmessage.place(relx = 0.5, rely = 0.55, anchor = CENTER)



def placebidgui(temp):
    
    global itemsdf
    
    clearFrame(browseitemsframe)
    clearFrame(bidfailframe)
    global uname
    
    index = int(temp)
    index -= 1
    
    storestr = ""
    templist = additemtolistgui(itemsdf, index)
    for i in range(5):
        storestr = storestr + templist[i] + "\n"
        
    storestr = "The item you are bidding on is:\n" + storestr
    
    def getbid():
            bid = bidentry.get()
            print(bid)
            checkbid(bid, buyingitemindex)

    headermessage = Label(bidframe, text = "Place your bid:", fg = "purple", bg = "#f7dcc1", font = ("Helvetica, 24"))

    item = Label(bidframe, text = storestr, fg = "purple", bg = "#f7dcc1", font = ("Helvetica, 17") )
    bidprompt = Label(bidframe, text = "Your Bid:", fg = "purple", bg = "#f7dcc1", font = ("Helvetica, 15"))
    bidentry = Entry(bidframe, fg = "green", bg = "white", font = ("Helvetica, 15"))
    placebutton = Button(bidframe, text = "Place Bid", fg = "purple", bg = "white", font = ("Helvetica, 15"), command = getbid)
    backbutton = Button(bidframe, text = "Go Back", fg = "purple", bg = "white", font = ("Helvetica, 15"), command = userwelc)

    headermessage.place(relx = 0.5, rely = 0.2, anchor = CENTER)
    item.place(relx = 0.5, rely = 0.4, anchor = CENTER)
    bidprompt.place(relx = 0.5, rely = 0.6, anchor = CENTER)
    bidentry.place(relx = 0.5, rely = 0.65, anchor = CENTER)
    placebutton.place(relx = 0.5, rely = 0.725, anchor = CENTER)
    backbutton.place(relx = 0.5, rely = 0.8, anchor = CENTER)
    

    bidframe.pack(fill='both', expand= True)
    window.attributes('-fullscreen', True)




def exit_func():
    window.destroy()
    


def nsolditems():
    
    global uname
    clearFrame(youritemframe)

    continuebutton = Button(nsolditemsframe, text = "Go Back", fg = "purple", bg = "white", font = ("Helvetica, 15"), command = youritems)
    listscroll = ttk.Scrollbar(nsolditemsframe, orient = VERTICAL)
    nsolditemslist = Listbox(nsolditemsframe, width = 90, height = 20, bg = "#c6c1f7", fg = "black", font = ("Helvetica, 20"), yscrollcommand = listscroll, relief = SUNKEN, borderwidth = 5)
    
    listscroll.config(command = nsolditemslist.yview)
    listscroll.pack(side = RIGHT, fill = BOTH)
    
    for i in range(len(notsolddf)):
        if (notsolddf.loc[i, 'username'] == uname):
            temporary = addnotsolditemtolistgui(notsolddf, i)
            
            num = "Item no." + str(i + 1)
            temporary.insert(0, num)
            temporary.insert(0, " ")
            for section in temporary:
                nsolditemslist.insert(END, section)
            #solditemslist.insert(END, addsolditemtolistgui(solddf, i))
            #print(addsolditemtolistgui(solddf, i))
    
   
    
    continuebutton.place(relx = 0.9, rely = 0.95, anchor = CENTER) 
    nsolditemslist.place(relx = 0.5, rely = 0.45, anchor = CENTER) 
    #solditemslist.pack(side = TOP, pady = 20)
    
    nsolditemsframe.pack(fill='both', expand= True, side = LEFT)
    window.attributes('-fullscreen', True)




def boughtitems():
    
    global uname
    clearFrame(youritemframe)

    continuebutton = Button(boughtitemsframe, text = "Go Back", fg = "purple", bg = "white", font = ("Helvetica, 15"), command = youritems)
    listscroll = ttk.Scrollbar(boughtitemsframe, orient = VERTICAL)
    boughtitemslist = Listbox(boughtitemsframe, width = 90, height = 20, bg = "#c6c1f7", fg = "black", font = ("Helvetica, 20"), yscrollcommand = listscroll, relief = SUNKEN, borderwidth = 5)
    
    listscroll.config(command = boughtitemslist.yview)
    listscroll.pack(side = RIGHT, fill = BOTH)
    
    for i in range(len(solddf)):
        if (solddf.loc[i, 'currbid'] == uname):
            temporary = addsolditemtolistgui(solddf, i)
            
            num = "Item no." + str(i + 1)
            temporary.insert(0, num)
            temporary.insert(0, " ")
            for section in temporary:
                boughtitemslist.insert(END, section)
            #solditemslist.insert(END, addsolditemtolistgui(solddf, i))
            #print(addsolditemtolistgui(solddf, i))
    
   
    
    continuebutton.place(relx = 0.9, rely = 0.95, anchor = CENTER) 
    boughtitemslist.place(relx = 0.5, rely = 0.45, anchor = CENTER) 
    #solditemslist.pack(side = TOP, pady = 20)
    
    boughtitemsframe.pack(fill='both', expand= True, side = LEFT)
    window.attributes('-fullscreen', True)
     

def browseitems():
    
    
    global uname
    global buyingitemindex
    
    clearFrame(userwelcframe)
    clearFrame(bidfailframe)
    
    def biditemnum():
        
        global buyingitemindex
       
        def getval():
            global buyingitemindex
            buyingitemindex = entry.get()
            print(buyingitemindex)
            placebidgui(buyingitemindex)
        
        prompt = Label(browseitemsframe, text = "Enter the item number of item you would like to buy:", fg = "green", bg = "#f7dcc1", font = ("Helvetica, 15"))
        prompt.place(relx = 0.3875, rely = 0.9, anchor = CENTER)
        entry = Entry(browseitemsframe, fg = "blue", font = ("Helvetica, 15"))
        next = Button(browseitemsframe, text = "Next", fg = "purple", bg = "white", font = ("Helvetica, 15"), command = getval)
        next.place(relx = 0.5, rely = 0.95, anchor = CENTER)
        entry.place(relx = 0.6125, rely = 0.9, anchor = CENTER)
        
        

    continuebutton = Button(browseitemsframe, text = "Go Back", fg = "purple", bg = "white", font = ("Helvetica, 15"), command = userwelc)
    bidbutton = Button(browseitemsframe, text = "Place bid", fg = "purple", bg = "white", font = ("Helvetica, 15"), command = biditemnum)
    listscroll = ttk.Scrollbar(browseitemsframe, orient = VERTICAL)
    itemslist = Listbox(browseitemsframe, width = 90, height = 20, bg = "#c6c1f7", fg = "black", font = ("Helvetica, 20"), yscrollcommand = listscroll, relief = SUNKEN, borderwidth = 5)
    
    listscroll.config(command = itemslist.yview)
    listscroll.pack(side = RIGHT, fill = BOTH)
    
    for i in range(len(itemsdf)):

        temporary = additemtolistgui(itemsdf, i)
            
        num = "Item no." + str(i + 1)
        temporary.insert(0, num)
        temporary.insert(0, " ")
        for section in temporary:
            itemslist.insert(END, section)
        #solditemslist.insert(END, addsolditemtolistgui(solddf, i))
        #print(addsolditemtolistgui(solddf, i))
    
   
    
    continuebutton.place(relx = 0.9, rely = 0.9, anchor = CENTER) 
    bidbutton.place(relx = 0.1, rely = 0.9, anchor = CENTER)
    itemslist.place(relx = 0.5, rely = 0.45, anchor = CENTER) 
    #solditemslist.pack(side = TOP, pady = 20)
    
    browseitemsframe.pack(fill='both', expand= True, side = LEFT)
    window.attributes('-fullscreen', True)




def sellingitems():
    
    global uname
    clearFrame(youritemframe)

    continuebutton = Button(curritemsframe, text = "Go Back", fg = "purple", bg = "white", font = ("Helvetica, 15"), command = youritems)
    listscroll = ttk.Scrollbar(curritemsframe, orient = VERTICAL)
    curritemslist = Listbox(curritemsframe, width = 90, height = 20, bg = "#c6c1f7", fg = "black", font = ("Helvetica, 20"), yscrollcommand = listscroll, relief = SUNKEN, borderwidth = 5)
    
    listscroll.config(command = curritemslist.yview)
    listscroll.pack(side = RIGHT, fill = BOTH)
    
    for i in range(len(itemsdf)):
        if (itemsdf.loc[i, 'username'] == uname):
            temporary = additemtolistgui(itemsdf, i)
            
            num = "Item no." + str(i + 1)
            temporary.insert(0, num)
            temporary.insert(0, " ")
            for section in temporary:
                curritemslist.insert(END, section)
            #solditemslist.insert(END, addsolditemtolistgui(solddf, i))
            #print(addsolditemtolistgui(solddf, i))
    
   
    
    continuebutton.place(relx = 0.9, rely = 0.95, anchor = CENTER) 
    curritemslist.place(relx = 0.5, rely = 0.45, anchor = CENTER) 
    #solditemslist.pack(side = TOP, pady = 20)
    
    curritemsframe.pack(fill='both', expand= True, side = LEFT)
    window.attributes('-fullscreen', True)



    
    
 
def solditems():
    
    global uname
    clearFrame(youritemframe)

    continuebutton = Button(solditemsframe, text = "Go Back", fg = "purple", bg = "white", font = ("Helvetica, 15"), command = youritems)
    listscroll = ttk.Scrollbar(solditemsframe, orient = VERTICAL)
    solditemslist = Listbox(solditemsframe, width = 90, height = 20, bg = "#c6c1f7", fg = "black", font = ("Helvetica, 20"), yscrollcommand = listscroll, relief = SUNKEN, borderwidth = 5)
    
    listscroll.config(command = solditemslist.yview)
    listscroll.pack(side = RIGHT, fill = BOTH)
    
    for i in range(len(solddf)):
        if (solddf.loc[i, 'username'] == uname):
            temporary = addsolditemtolistgui(solddf, i)
            
            num = "Item no." + str(i + 1)
            temporary.insert(0, num)
            temporary.insert(0, " ")
            for section in temporary:
                solditemslist.insert(END, section)
            #solditemslist.insert(END, addsolditemtolistgui(solddf, i))
            #print(addsolditemtolistgui(solddf, i))
    
   
    
    continuebutton.place(relx = 0.9, rely = 0.95, anchor = CENTER) 
    solditemslist.place(relx = 0.5, rely = 0.45, anchor = CENTER) 
    #solditemslist.pack(side = TOP, pady = 20)
    
    solditemsframe.pack(fill='both', expand= True, side = LEFT)
    window.attributes('-fullscreen', True)
     
    
    
    
    
def loginfailscr():
    clearFrame(loginframe)
    
    errormessage = Label(loginfailscrframe, text = "Your username or password is incorrect\nPlease try again.", fg = "red", bg = "#f7dcc1", font = ("Helvetica, 24"))
    continuebutton = Button(loginfailscrframe, text = "Try again", fg = "black", bg = "white", font = ("Helvetica, 15"), command = loginscreen)
    
    errormessage.place(relx = 0.5, rely = 0.45, anchor = CENTER) 
    continuebutton.place(relx = 0.5, rely = 0.55, anchor = CENTER) 
    
    loginfailscrframe.pack(fill='both', expand= True, side = LEFT)
    window.attributes('-fullscreen', True)
  
  
  
def youritems():
    
    global uname
    
    clearFrame(userwelcframe)
    clearFrame(youritemframe)
    clearFrame(solditemsframe)
    clearFrame(boughtitemsframe)
    clearFrame(nsolditemsframe)
    clearFrame(curritemsframe)

    welctext = "What would you like to check?"

    headermessage = Label(youritemframe, text = welctext, fg = "purple", bg = "#f7dcc1", font = ("Helvetica, 24"))

    solditbutton = Button(youritemframe, text = "Sold items", fg = "purple", bg = "white", font = ("Helvetica, 15"), command = solditems)
    boughtitbutton = Button(youritemframe, text = "Items successfully bought", fg = "purple", bg = "white", font = ("Helvetica, 15"), command = boughtitems)
    failitbutton = Button(youritemframe, text = "Items failed to sell", fg = "purple", bg = "white", font = ("Helvetica, 15"), command = nsolditems)
    sellingitbutton = Button(youritemframe, text = "Items you have up for sale", fg = "purple", bg = "white", font = ("Helvetica, 15"), command = sellingitems)
    backbutton = Button(youritemframe, text = "Go Back", fg = "purple", bg = "white", font = ("Helvetica, 15"), command = userwelc)

    headermessage.place(relx = 0.5, rely = 0.2, anchor = CENTER)
    solditbutton.place(relx = 0.5, rely = 0.35, anchor = CENTER)
    boughtitbutton.place(relx = 0.5, rely = 0.45, anchor = CENTER)
    failitbutton.place(relx = 0.5, rely = 0.55, anchor = CENTER)
    sellingitbutton.place(relx = 0.5, rely = 0.65, anchor = CENTER)
    backbutton.place(relx = 0.5, rely = 0.75, anchor = CENTER)
    

    youritemframe.pack(fill='both', expand= True)
    window.attributes('-fullscreen', True)
  
  
    
def userwelc():
    
    global uname
    
    clearFrame(loginframe)
    clearFrame(additemframe)
    clearFrame(youritemframe)
    clearFrame(browseitemsframe)
    clearFrame(bidframe)
    clearFrame(bidfailframe)
    
    itemsdf.to_csv('items.csv', index = False)
    solddf.to_csv('sold.csv', index = False)
    notsolddf.to_csv('notsold.csv', index = False)
    checksold()
    
    welctext = "Welcome back " + str(uname)

    headermessage = Label(userwelcframe, text = welctext, fg = "purple", bg = "#f7dcc1", font = ("Helvetica, 24"))

    sellitbutton = Button(userwelcframe, text = "Sell an item", fg = "purple", bg = "white", font = ("Helvetica, 15"), command = additemgui)
    browseitbutton = Button(userwelcframe, text = "Browse items for sale", fg = "purple", bg = "white", font = ("Helvetica, 15"), command = browseitems)
    youritbutton = Button(userwelcframe, text = "Your Items", fg = "purple", bg = "white", font = ("Helvetica, 15"), command = youritems)
    logoutbutton = Button(userwelcframe, text = "Logout", fg = "purple", bg = "white", font = ("Helvetica, 15"), command = loginscreen)

    headermessage.place(relx = 0.5, rely = 0.2, anchor = CENTER)
    sellitbutton.place(relx = 0.5, rely = 0.4, anchor = CENTER)
    browseitbutton.place(relx = 0.5, rely = 0.5, anchor = CENTER)
    youritbutton.place(relx = 0.5, rely = 0.6, anchor = CENTER)
    logoutbutton.place(relx = 0.5, rely = 0.7, anchor = CENTER)
    

    userwelcframe.pack(fill='both', expand= True)
    window.attributes('-fullscreen', True)



def additemgui():
    
    clearFrame(userwelcframe)

    global uname
    
    def work():
        
        global uname
        
        name = itnameentry.get()
        descp = itdescpentry.get()
        price = itpriceentry.get()
        additem(uname, name, descp, price)
        
        successmessage = Label(additemframe, text = "Item added successfully", fg = "#89e72b", bg = "#f7dcc1", font = ("Helvetica, 20"))
        successmessage.place(relx = 0.5, rely = 0.65, anchor = CENTER)

    headermessage = Label(additemframe, text = "Add an item:", fg = "purple", bg = "#f7dcc1", font = ("Helvetica, 24"))

    itnameprompt = Label(additemframe, text = "Enter the Items name:", fg = "purple", bg = "#f7dcc1", font = ("Helvetica, 15") )
    itnameentry = Entry(additemframe, fg = "#cf6d43", bg = "white", font = ("Helvetica, 15") )
    itdescpprompt = Label(additemframe, text = "Enter a description for the item:", fg = "purple", bg = "#f7dcc1", font = ("Helvetica, 15"))
    itdescpentry = Entry(additemframe, fg = "#cf6d43", bg = "white", font = ("Helvetica, 15"))
    itpriceprompt = Label(additemframe, text = "Enter the price you want as the starting bid:", fg = "purple", bg = "#f7dcc1", font = ("Helvetica, 15"))
    itpriceentry = Entry(additemframe, fg = "#cf6d43", bg = "white", font = ("Helvetica, 15"))
    citembutton = Button(additemframe, text = "Create Item", fg = "purple", bg = "white", font = ("Helvetica, 15"), command = work)
    backbutton = Button(additemframe, text = "Go back", fg = "purple", bg = "white", font = ("Helvetica, 15"), command = userwelc)

    headermessage.place(relx = 0.5, rely = 0.15, anchor = CENTER)
    itnameprompt.place(relx = 0.5, rely = 0.25, anchor = CENTER)
    itnameentry.place(relx = 0.5, rely = 0.3, anchor = CENTER)
    itdescpprompt.place(relx = 0.5, rely = 0.4, anchor = CENTER)
    itdescpentry.place(relx = 0.5, rely = 0.45, anchor = CENTER)
    itpriceprompt.place(relx = 0.5, rely = 0.55, anchor = CENTER)
    itpriceentry.place(relx = 0.5, rely = 0.6, anchor = CENTER)
    citembutton.place(relx = 0.5, rely = 0.725, anchor = CENTER)
    backbutton.place(relx = 0.5, rely = 0.8, anchor = CENTER)
    

    additemframe.pack(fill='both', expand= True)
    window.attributes('-fullscreen', True)





def caccount():
    
    clearFrame(mframe)
    
    global uname
    
    
    def operation():
        
        global uname 
        
        uname = usernameentry.get()
        AddUser(uname, passwordentry.get())
        
        successmessage = Label(caccountframe, text = "Account created successfully, please go back", fg = "light green", bg = "#f7dcc1", font = ("Helvetica, 30"))
        successmessage.place(relx = 0.5, rely = 0.6, anchor = CENTER)

    headermessage = Label(caccountframe, text = "Create a new account:", fg = "purple", bg = "#f7dcc1", font = ("Helvetica, 24"))

    usernameprompt = Label(caccountframe, text = "Enter Username here:", fg = "purple", bg = "#f7dcc1", font = ("Helvetica, 15"))
    usernameentry = Entry(caccountframe, fg = "#94cce4", bg = "white", font = ("Helvetica, 15"))
    passwordprompt = Label(caccountframe, text = "Enter Password here", fg = "purple", bg = "#f7dcc1", font = ("Helvetica, 15"))
    passwordentry = Entry(caccountframe, fg = "#94cce4", bg = "white", font = ("Helvetica, 15"))
    loginbutton = Button(caccountframe, text = "Create Account", fg = "purple", bg = "white", font = ("Helvetica, 15"), command = operation)
    backbutton = Button(caccountframe, text = "Back to Main menu", fg = "purple", bg = "white", font = ("Helvetica, 15"), command = mainscreen)

    headermessage.place(relx = 0.5, rely = 0.2, anchor = CENTER)
    usernameprompt.place(relx = 0.5, rely = 0.3, anchor = CENTER)
    usernameentry.place(relx = 0.5, rely = 0.35, anchor = CENTER)
    passwordprompt.place(relx = 0.5, rely = 0.45, anchor = CENTER)
    passwordentry.place(relx = 0.5, rely = 0.5, anchor = CENTER)
    loginbutton.place(relx = 0.5, rely = 0.725, anchor = CENTER)
    backbutton.place(relx = 0.5, rely = 0.8, anchor = CENTER)
    

    caccountframe.pack(fill='both', expand= True)
    window.attributes('-fullscreen', True)





def loginscreen():
    
    clearFrame(mframe)
    clearFrame(userwelcframe)
    clearFrame(loginfailscrframe)
    global uname
    
    
    def nextmenu():
        
        global uname
        
        uname = usernameentry.get()
        if Login(uname, passwordentry.get()):
            userwelc()
        else:
            loginfailscr()

    headermessage = Label(loginframe, text = "Login:", fg = "purple", bg = "#f7dcc1", font = ("Helvetica, 24"))

    usernameprompt = Label(loginframe, text = "Enter Username here:", fg = "purple", bg = "#f7dcc1", font = ("Helvetica, 15") )
    usernameentry = Entry(loginframe, fg = "green", bg = "white", font = ("Helvetica, 15") )
    passwordprompt = Label(loginframe, text = "Enter Password here:", fg = "purple", bg = "#f7dcc1", font = ("Helvetica, 15"))
    passwordentry = Entry(loginframe, fg = "green", bg = "white", font = ("Helvetica, 15"))
    loginbutton = Button(loginframe, text = "Login", fg = "purple", bg = "white", font = ("Helvetica, 15"), command = nextmenu)
    backbutton = Button(loginframe, text = "Back to Main menu", fg = "purple", bg = "white", font = ("Helvetica, 15"), command = mainscreen)

    headermessage.place(relx = 0.5, rely = 0.2, anchor = CENTER)
    usernameprompt.place(relx = 0.5, rely = 0.3, anchor = CENTER)
    usernameentry.place(relx = 0.5, rely = 0.35, anchor = CENTER)
    passwordprompt.place(relx = 0.5, rely = 0.45, anchor = CENTER)
    passwordentry.place(relx = 0.5, rely = 0.5, anchor = CENTER)
    loginbutton.place(relx = 0.5, rely = 0.725, anchor = CENTER)
    backbutton.place(relx = 0.5, rely = 0.8, anchor = CENTER)
    

    loginframe.pack(fill='both', expand= True)
    window.attributes('-fullscreen', True)





def mainscreen():
    
    clearFrame(loginframe)
    clearFrame(caccountframe)
    #bg = Label(mframe, bg="#f7dcc1")#,fill = tk.BOTH, side = tk.LEFT, expand=True)
    #bg.pack(fill = tk.BOTH, side = tk.LEFT, expand=True)

    welcome = Label(mframe, text = "Welcome to Ebay!", fg = "purple", bg = "#f7dcc1", font = ("Helvetica, 24"))

    loginbutton = Button(mframe, text = "Login", fg = "purple", bg = "white", font = ("Helvetica, 15"), command = loginscreen)
    signupbutton = Button(mframe, text = "Create a new account", fg = "purple", bg = "white", font = ("Helvetica, 15"), command = caccount)
    exitbutton = Button(mframe, text = "Exit", fg = "purple", bg = "white", font = ("Helvetica, 15"), command = exit_func)

    loginbutton.place(relx = 0.5, rely = 0.4, anchor = CENTER)
    signupbutton.place(relx = 0.5, rely = 0.5, anchor = CENTER)
    exitbutton.place(relx = 0.5, rely = 0.6, anchor = CENTER)
    welcome.place(relx = 0.5, rely = 0.2, anchor = CENTER)
    

    mframe.pack(fill='both', expand= True)
    #mframe.place(relx = 0.5, rely = 0.5)
    window.attributes('-fullscreen', True)
    window.mainloop()
    
    
    
    
    
mainscreen()