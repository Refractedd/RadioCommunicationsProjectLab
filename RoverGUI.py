import tkinter as tk
import tkinter.messagebox
import customtkinter
import serial
from PIL import Image, ImageTk
import numpy as np
from icecream import ic
import time
import re
''' 
Created by:     Benjamin Williams   R11544055
Design For:     Project Lab III: Radio Direction Finding Base Station GUI
                Texas Tech University,
                Electrical and Computer Engineering

Map Border Dimensions: (Lab3Map.png)
Height:   858 px   -   2560 ft  -   781.3 m 
Width:   1232 px   -   3350 ft  -   1020  m
'''

ic.enable()

EX_ADD = ["40", "41", "42", "43", "44", "45"]
EX_RES = ["-999", "-999", "-999", "-999", "-999", "-999"]
buffer = 0

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

class RoverApp(customtkinter.CTk):
    WIDTH = 650
    HEIGHT = 580

    def __init__(self):
        super().__init__()
        self.title("Ben's Customized Rover Interface")
        self.geometry(f"{RoverApp.WIDTH}x{RoverApp.HEIGHT}")

        self.frame_left = customtkinter.CTkFrame(master=self, width=200, corner_radius=10, height=RoverApp.HEIGHT,
                                                 border_color="#5b5b5b", border_width=2)
        self.frame_left.grid(row=0, column=0, ipadx=20, ipady=20, padx=10, pady=10, sticky="nsew")

        self.frame_text = customtkinter.CTkFrame(master=self.frame_left, border_color="#5b5b5b", border_width=2,
                                                 corner_radius=10)
        self.frame_text.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

        self.window = tk.Text(master=self.frame_text, foreground="#FFFFFF", background="#5b5b5b",
                              font=("Roboto Medium", -16), state="disabled", width=65, height=20, borderwidth=2)
        self.window.pack(padx=10, pady=10, fill="both", anchor="center")

        self.terminal = customtkinter.CTkEntry(master=self.frame_left, height=50,
                                               placeholder_text="Terminal> Enter Commands or type -help.",text_font=("Roboto Medium", -16))
        self.terminal.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        self.win_print("Commands: " 
                       "\n-help \t    : display options" 
                       "\n-send [msg] : sends a message to Base Station\n")

        self.terminal.bind("<Return>", self.parseCommand)

        #self.after(1000, self.serial_poll)

    #def serial_poll(self):
    #    if rover.isOpen():
    #        buffer = rover.in_waiting
    #        if buffer > 0:
    #            buffer = rover.in_waiting
    #            s = uartRead()
    #            self.win_print(s)
    #            print(s)

            #txt = f"AT+SEND=50,{len(choice)},{choice}"
            #uart(txt)
    #    self.after(500, self.serial_poll)

    def parseCommand(self, e):
        if self.terminal.get() != "":
            cmd = self.terminal.get()
            if cmd == "-help":
                txt = "Commands: " \
                      "\n-help \t    : display options" \
                      "\n[msg] : sends a message to rover\n"
                self.win_print(txt)
            elif cmd.find("-ping")!=-1:
                for i in range(3):
                    EX_RES[i] = ping(i)
                uartWrite(f"$0,{EX_RES[0]}:1,{EX_RES[1]}:2,{EX_RES[2]}:3")
                #artWrite(f"AT+SEND=50,{len(rssi_text)},{rssi_text}")
            else:
                print(f"{cmd} . {len(cmd)}")
                txt = f"AT+SEND=49,{len(cmd)},{cmd}"
                s = uart(txt)
                self.win_print(txt)
                self.win_print(s)
            self.terminal.delete(0, tk.END)
            self.terminal.insert(tk.END, "")
            return

    def win_print(self, string):
        self.window.config(state="normal")
        self.window.insert(tk.END, string)
        self.window.insert(tk.END, '\n')
        self.window.yview(tk.END)
        self.window.config(state="disabled")
        return

    def on_closing(self, event=0):
        rover.close()
        self.destroy()

    def start(self):
        self.mainloop()

def ping(index):
    uartWrite(f"AT+SEND={EX_ADD[index]},1,R")
    time.sleep(.5)
    reply = uartRead()
    return reply
    # for i in range(3):
    #     timeout = 0
    #     reply = uart(f"AT+SEND={EX_ADD[i]},1,R")
    # while rover.inWaiting() > 4:
    #     print()
    # for i in range(3):
    #     #while not rover.readable():
    #     #    print()#index = cpy.split(',')[0][:-2]
    #     reply = uartRead()
    #     rssi = reply.split(',')[3]
    #     EX_RES[i] = rssi
    #     print(EX_RES[i])



    #text = "$0,{0}:1,{1}:2,{2}:3".format(EX_RES[0], EX_RES[1], EX_RES[2])
    #uart(text)
    #return text

def uart(s):
    print(s)
    msg_out = f"{s}\r\n"
    Data_out = bytes(msg_out, 'utf-8')
    rover.write(Data_out)

    time.sleep(.5)

    data_in = rover.read_until(expected=b'\n')[:-2]
    message = data_in.decode('utf-8')
    print(message)
    return message


def uartWrite(s):
    print(s)
    msg_out = f"{s}\r\n"
    Data_out = bytes(msg_out, 'utf-8')
    rover.write(Data_out)
    #return Data_out

def uartRead():
    time.sleep(.5)
    data_in = rover.read_until(expected=b'\n')[:-2]
    message = data_in.decode('utf-8')
    return message

if __name__ == "__main__":

    #rover = serial.Serial(port='COM16', baudrate=9600)

    #if not rover.isOpen():
    #    rover.open()

    #uart("AT+BAND=915000000")
    #uart("AT+ADDRESS=49")
    #uart("AT+NETWORKID=12")
    #uart("AT+IPR=9600")

    app = RoverApp()
    app.start()

    #uart("AT+SEND=48,1,h")