import math
from multiprocessing.connection import wait
import random
from tkinter import *
import tkinter as tk

from PIL import Image, ImageTk

window = tk.Tk()

def encrypt(user):
    mult = 30
    addit = 1008567

    encoded =""

    if(len(user) % 2 != 0):
        user = user +" "

    for i in range(0, len(user), 2):
        tempEnc = ord(user[i])
        value = ord(user[i+1])
        
        print(tempEnc, value)
        tempEnc = (tempEnc << 0x8) +value
        tempEnc = tempEnc * mult + addit

        encoded += hex(tempEnc)[2:]
    return encoded

def decrypt(user):
    mult = 30
    addit = 1008567
    decoded = ""

    for i in range(0, len(user), 6):
        tempDec = int("0x"+user[i:i+6], 0)
        
        tempDec = int((tempDec -addit) / mult)

        hexer = hex(tempDec)[2:]

        decoded += bytearray.fromhex(hexer).decode()

def send():
    msg = e.get()
    send = "Home Base -> "+msg
    txt.insert(tk.END, "\n" + send)
    txt.yview(END)
    e.delete(0,END)
    encryptMsg = encrypt(msg)
    print(encryptMsg)

def clicked(ok):
    send = "Home Base -> "+e.get()
    txt.insert(tk.END, "\n" + send)
    txt.yview(END)
    e.delete(0,END)
    # print("I am here")

def point():
# 45 pixels = 108.33 meters
# 1 pixel ~= 2.407 meters
# 2.0769 pixels ~= 5 meters
# 4.15 pixels ~= 100 meters
# memCirc = [1054, 400]
# bounds x =-25 -  3
#       y = -7 -  9
    # if(x !=0):
    #     if(y!=0):

            point = Image.open("reference.png")
            background = Image.open("remadeBackground.png")
            
            # xCoor = 0.0
            # yCoor = 0.0
            if(e.get() == ""):
                send = "COMMAND -> Enter x,y coordinates first"
                txt.insert(tk.END, "\n" + send)
                txt.yview(END)
                return

            coords = e.get()
            e.delete(0,END)
            xCoor = int(coords[:coords.rfind(',')])
            yCoor = int(coords[coords.rfind(',')+1:])

            if(xCoor > 3):
                send = "COMMAND -> X value out of scope"
                txt.insert(tk.END, "\n" + send)
                txt.yview(END)
                return
            if(xCoor < -25):
                send = "COMMAND -> X value out of scope"
                txt.insert(tk.END, "\n" + send)
                txt.yview(END)
                return
            if(yCoor > 9):
                send = "COMMAND -> Y value out of scope"
                txt.insert(tk.END, "\n" + send)
                txt.yview(END)
                return
            if(yCoor < -7):
                send = "COMMAND -> Y value out of scope"
                txt.insert(tk.END, "\n" + send)
                txt.yview(END)
                return

            xCoor = float(xCoor)*4.15 + 1044
            yCoor = float(yCoor)*(-4.15) + 390 

            background.paste(point, (int(xCoor), int(yCoor)), point)

            background.save('remadeBackground.png','PNG')

            newImg = Image.open('remadeBackground.png')

            tkimage = ImageTk.PhotoImage(newImg)

            panel1 = Label(window, image = tkimage)
            panel1.grid(row=2, column=8, sticky="E")
            # print(x,y)

def notebook():
            point = Image.open("notebook.png")
            background = Image.open("remadeBackground.png")
            
            # xCoor = 0.0
            # yCoor = 0.0
            if(e.get() == ""):
                send = "COMMAND -> Enter x,y coordinates first"
                txt.insert(tk.END, "\n" + send)
                txt.yview(END)
                return

            coords = e.get()
            e.delete(0,END)
            xCoor = int(coords[:coords.rfind(',')])
            yCoor = int(coords[coords.rfind(',')+1:])

            if(xCoor > 3):
                send = "COMMAND -> X value out of scope"
                txt.insert(tk.END, "\n" + send)
                txt.yview(END)
                return
            if(xCoor < -25):
                send = "COMMAND -> X value out of scope"
                txt.insert(tk.END, "\n" + send)
                txt.yview(END)
                return
            if(yCoor > 9):
                send = "COMMAND -> Y value out of scope"
                txt.insert(tk.END, "\n" + send)
                txt.yview(END)
                return
            if(yCoor < -7):
                send = "COMMAND -> Y value out of scope"
                txt.insert(tk.END, "\n" + send)
                txt.yview(END)
                return

            xCoor = float(xCoor)*4.15 + 1044
            yCoor = float(yCoor)*(-4.15) + 390 

            background.paste(point, (int(xCoor), int(yCoor)), point)

            background.save('remadeBackground.png','PNG')

            newImg = Image.open('remadeBackground.png')

            tkimage = ImageTk.PhotoImage(newImg)

            panel1 = Label(window, image = tkimage)
            panel1.grid(row = 2, column = 8, sticky = E)


def getorigin(eventorigin):
    # if untilClk == 1:
    #     untilClk = 0
    global x,y
    # x = 0
    # y = 0
    # if (eventorigin.x > 100):
    if (eventorigin.y > -.753*eventorigin.x +718):
        x=eventorigin.x
        y=eventorigin.y
    print(eventorigin.x,eventorigin.y)
    print(x,y)

def player():
    
        guy = Image.open("littleGuy.png")
        guyBack = Image.open('remadeBackground.png')

        degree = random.randint(0,360)
        theta = degree * math.pi / 180
        tof = (round(random.uniform(0.000000001, 0.000001000), 9))

        # tof = 0.000000700  #time of flight, 100 nanoseconds

        # theta = 225 * math.pi / 180  #angle of arival in radians

        r = tof / 2 * 300000000 #time going out * speed of light
        xCoord = round(math.cos(theta) * r)      #finding x coord, rounded to zero out/make int
        yCoord = round(math.sin(theta) * r)      #finding y coord, rounded to zero out/make int

        xCoord = xCoord*4.15 + 1044
        yCoord = yCoord*(-4.15) + 390 

        while(yCoord < -.753*xCoord +718 or yCoord > 750 or xCoord > 1120):
            tof = (round(random.uniform(0.000000001, 0.000001000), 9))
            r = tof / 2 * 300000000 #time going out * speed of light
           
            xCoord = round(math.cos(theta) * r)      #finding x coord, rounded to zero out/make int
            yCoord = round(math.sin(theta) * r)      #finding y coord, rounded to zero out/make int

            xCoord = xCoord*4.15 + 1044
            yCoord = yCoord*(-4.15) + 390 

        print("xCoord is ", xCoord)   
        print("yCoord is ", yCoord)

        guyBack.paste(guy, (int(xCoord), int(yCoord)), guy)
        guyBack.save('playerBack.png','PNG')

        together = Image.open('playerBack.png')

        tkTime = ImageTk.PhotoImage(together)


        panel1 = Label(window, image = tkTime)
        panel1.grid(row = 2, column = 8, sticky = E)
        
        window.after(300,player)
    # point = Image.open("reference.png")
    # background = Image.open("remadeBackground.png")
    
    # background.paste(point, (x-10, y-10), point)

    # background.save('remadeBackground.png','PNG')

    # newImg = Image.open('remadeBackground.png')

    # tkimage = ImageTk.PhotoImage(newImg)

    # panel1 = Label(window, image = tkimage)
    # panel1.grid(row = 2, column = 8, sticky = E)
    # else:
        # return

memCirc = [1054, 400]
# 45 pixels = 108.33 meters
# 1 pixel ~= 2.407 meters
# 41.5 pixels ~= 100 meters



lable1 = Label(window, pady=10, width=20, height=1).grid(
    row=1)
 
txt = Text(window, width=60)
txt.grid(row=2, column=0, columnspan=2)
 
scrollbar = Scrollbar(txt)
scrollbar.place(relheight=1, relx=0.974)
 
e = Entry(window, width=55)
e.grid(row=3, column=0)
 
send = Button(window, text="Send",
              command=send).grid(row=3, column=1)

point = Button(window, text="Set a reference point", 
                command=point).grid(row=0, column=0)

notebook = Button(window, text="Place a Notebook", 
                command=notebook).grid(row=0, column=1)


img = Image.open("compas.png")
background = Image.open("Campus snippet.png")


background2 = ImageTk.PhotoImage(img)
w = background2.width()
h = background2.height()
w = (int)(w*.25)
h = (int)(h*.25)
print(w)
print(h)
# img = img.resize((background2.width()*.25,background2.height()*.25))
img = img.resize((w,h))

# img = ImageTk.PhotoImage(resize_img)

background.paste(img, (0,0), img)

# point = Image.open("reference.png")

# background.paste(point, (485,200), point)

background.save('remadeBackground.png','PNG')

newImg = Image.open('remadeBackground.png')

tkimage = ImageTk.PhotoImage(newImg)

# canvas = tk.Canvas()
# canvas.create_image(0, 0, window, image = tkimage)
# canvas.grid(row = 2, column=8, sticky = E)
panel1 = Label(window, image = tkimage)
panel1.grid(row = 2, column = 8, sticky = E)

window.bind("<Button 1>", getorigin)
window.bind("<Return>", clicked)

player()
 
window.mainloop()


# for i in range(100):

    
