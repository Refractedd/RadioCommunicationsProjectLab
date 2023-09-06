import tkinter as tk
import tkinter.messagebox
import customtkinter
import serial
from PIL import Image, ImageTk
from icecream import ic
import time
import random
import os
import numpy as np

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
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")


def metersToUnits(x, y):
    x_units = round(x * (146/402))
    y_units = round(y * (264/220))
    return x_units, y_units


def UnitsToMeters(x, y):
    x_meters = round(x / (146/402))
    y_meters = round(y / (264/220))
    return x_meters, y_meters

def distanceToUnits(rssi):
    return rssi*(1587661/1010025)

class MapItem(object):

    def __init__(self, obj, xnum, ynum, cnt):
        self.widget = obj
        self.x_pos = int(xnum)
        self.y_pos = int(ynum)
        self.count = int(cnt)

    def get_pos(self):
        return self.x_pos, self.y_pos

    def set_xy(self, xnum, ynum):
        self.x_pos = xnum
        self.y_pos = ynum


class Relay(MapItem):

    def __init__(self, obj, xnum, ynum, name, cnt, tof):
        super(Relay, self).__init__(obj, xnum, ynum, cnt)
        self.name = name
        self.ToF_value = tof

    def get_ToF(self):
        return self.ToF_value

    def set_ToF(self, val):
        self.ToF_value = val


class Notebook(MapItem):

    def __init__(self, obj, xnum, ynum, name, cnt):
        super(Notebook, self).__init__(obj, xnum, ynum, cnt)
        self.name = name
        self.codeword = "null"

    def get_codeword(self):
        return self.codeword

    def set_codeword(self, word):
        self.codeword = word




class App(customtkinter.CTk):
    WIDTH = 1280
    HEIGHT = 855

    def __init__(self):
        super().__init__()
        self.title("Ben's Customized Base-Station Interface")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")

        self.grid_columnconfigure(0, minsize=200, weight=0)
        self.grid_columnconfigure(1, minsize=1000, weight=1)

        self.grid_rowconfigure(0, minsize=700)
        self.grid_rowconfigure(1, weight=0)

        self.frame_left = customtkinter.CTkFrame(master=self, width=200, corner_radius=10, height=App.HEIGHT,
                                                 border_color="#5b5b5b", border_width=2)
        self.frame_left.grid(row=0, column=0, ipadx=20, ipady=20, padx=10, pady=10, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self, width=513, corner_radius=10, height=App.HEIGHT,
                                                  border_color="#5b5b5b", border_width=2)
        self.frame_right.grid(row=0, column=1, padx=10, pady=10, sticky="nsw")

        self.frame_output = customtkinter.CTkFrame(master=self, width=App.WIDTH - 100, corner_radius=10,
                                                   border_color="#5b5b5b", border_width=2)
        self.frame_output.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky="nw")

        self.Relay_win = customtkinter.CTk()
        self.Relay_win.title("Relay Manager")
        self.Relay_win.geometry("300x300")
        self.Relay_win.protocol("WM_DELETE_WINDOW", self.Relay_win.destroy)

        self.Relay_Frame = customtkinter.CTkFrame(master=self.Relay_win, corner_radius=10, width=500, height=500,
                                                  border_color="#5b5b5b", border_width=2)
        self.Relay_Frame.grid_configure(row=0, column=0, rowspan=6, columnspan=3, padx=20, pady=20, sticky="we")

        self.Relay_Title = customtkinter.CTkLabel(master=self.Relay_Frame, text="Relay Manager",
                                                  text_font=("Roboto Medium", -16), padx=20)
        self.Relay_Title.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        map_image = Image.open("Lab3Map2.png").resize((513, 669))
        rover_image = Image.open("Rover_1.png").resize((50, 50))
        notebook_image = Image.open("notebook.png").resize((50, 50))
        relay_image = Image.open("blueMarker.png").resize((50, 50))
        marker_image = Image.open("redMarker.png").resize((50, 50))

        self.bg_image = ImageTk.PhotoImage(map_image)
        self.rover_image = ImageTk.PhotoImage(rover_image)
        self.nb_image = ImageTk.PhotoImage(notebook_image)
        self.node_image = ImageTk.PhotoImage(relay_image)
        self.marker_image = ImageTk.PhotoImage(marker_image)

        self.Map = tkinter.Canvas(master=self.frame_right, width=513, height=669)
        self.Map.grid(row=0, column=2, padx=20, pady=10)
        self.Map.create_image(0, 0, image=self.bg_image, anchor="nw")
        self.Map.grid_configure(row=0, column=0, rowspan=669, columnspan=513, sticky='nsw')

        self.x_var = float(50)
        self.y_var = float(50)

        self.pop = customtkinter.CTkFrame(master=self.frame_right, corner_radius=10, border_color="#5b5b5b",
                                          border_width=2)
        self.marker_var = customtkinter.StringVar(value="Relay")
        self.pop_entry = customtkinter.CTkComboBox(master=self.pop, values=["Relay", "Notebook", "Marker", "Rover"],
                                                   text_font=("Roboto Medium", -14), command=self.PlaceMarker,
                                                   variable=self.marker_var)
        self.pop_entry.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.Relay_Title = customtkinter.CTkLabel(master=self.frame_left, text="Base Station Applications",
                                                  text_font=("Roboto Medium", -17, "underline", "bold"))
        self.Relay_Title.grid(row=1, column=0, padx=20, ipadx=10, pady=10, sticky="nswe")

        self.RelayButton = customtkinter.CTkButton(master=self.frame_left, text="Relays",
                                                   text_font=("Roboto Medium", -14), command=self.Relay_win.mainloop)
        self.RelayButton.grid(row=4, column=0, padx=40, pady=20, sticky="n")

        self.switch_2 = customtkinter.CTkSwitch(master=self.frame_left, text="Dark Mode", command=self.change_mode,
                                                text_font=("Roboto Medium", -14))
        self.switch_2.grid(row=8, column=0, pady=20, padx=20, sticky="sw")
        self.switch_2.select()

        self.info = customtkinter.CTkLabel(master=self.frame_output, width=App.WIDTH - 70,
                                           text="Terminal> Hover over buttons for descriptions.",
                                           text_font=("Roboto Medium", -16), padx=20)
        self.info.grid(row=0, column=0, padx=20, pady=20, sticky='nsw')

        self.frame_text = customtkinter.CTkFrame(master=self.frame_left, border_color="#5b5b5b", border_width=2,
                                                 corner_radius=10)
        self.frame_text.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

        self.window = tk.Text(master=self.frame_text, foreground="#FFFFFF", background="#5b5b5b",
                              font=("Roboto Medium", -16), state="disabled", width=65, height=20, borderwidth=2)
        self.window.pack(padx=10, pady=10, fill="both", anchor="center")

        self.terminal = customtkinter.CTkEntry(master=self.frame_left, height=50,
                                               placeholder_text="Terminal> Enter Commands or type -help.",
                                               text_font=("Roboto Medium", -16))
        self.terminal.grid(row=6, column=0, padx=20, pady=20, sticky="ew")

        self.win_print("Commands: \n-help \t    : display options"
                       "\n-send [msg] : sends a message to rover\n")

        self.rover = self.Map.create_image(269, 354, image=self.rover_image)
        #self.Map.move(self.rover, 350, 350)

        self.relays = np.zeros(3, dtype=object)
        self.relayLabels = np.zeros(3, dtype=object)
        r1 = self.Map.create_image(295, 147, image=self.node_image)
        r2 = self.Map.create_image(295, 396, image=self.node_image)
        r3 = self.Map.create_image(418, 271, image=self.node_image)
        #r4 = self.Map.create_image(152, 312, image=self.node_image)
        #r5 = self.Map.create_image(341, 36, image=self.node_image)
        #r6 = self.Map.create_image(274, 277, image=self.node_image)

        self.relays = [(Relay(r1, 295, 147, "Relay 1", 0, distanceToUnits(232))), #meters 232 -> units 290.87
                       (Relay(r2, 295, 396, "Relay 2", 1, distanceToUnits(262))),
                       (Relay(r3, 418, 271, "Relay 3", 2, distanceToUnits(217)))]
                       #(Relay(r4, 152, 312, "Relay 4", 3, 100)),
                       #(Relay(r5, 341, 36,  "Relay 5", 4, 150)),
                       #(Relay(r6, 274, 277, "Relay 7", 5, 200))]

        self.ovals = np.zeros(3, dtype=object)

        index = 0
        for relay in self.relays:
            text = relay.name + f" ( {relay.x_pos}, {relay.y_pos} ) RSSI: {relay.get_ToF()}"
            self.relayLabels[index] = customtkinter.CTkLabel(master=self.Relay_Frame, text=text,
                                                             text_font=("Roboto Medium", -16), padx=20)
            self.relayLabels[index].grid(row=index + 1, column=0, sticky='w')
            index += 1

        self.notebooks = [None, None, None]
        self.Map.create_text(295, 147, text=f"{1}", font=("Roboto Medium", -20))
        self.Map.create_text(295, 396, text=f"{2}", font=("Roboto Medium", -20))
        self.Map.create_text(418, 271, text=f"{3}", font=("Roboto Medium", -20))
        #self.Map.create_text(152, 312, text=f"{4}", font=("Roboto Medium", -20))
        #self.Map.create_text(341, 36, text=f"{5}", font=("Roboto Medium", -20))
        #self.Map.create_text(274, 277, text=f"{6}", font=("Roboto Medium", -20))
        self.next_relay = 3

        self.RelayButton.bind("<Enter>", self.ToF_hover)
        self.RelayButton.bind("<Leave>", self.button_hover_leave)
        self.Map.bind("<Motion>", self.Map_hover)
        self.Map.bind("<Button-1>", self.clickCanvas)
        self.Map.bind("<Leave>", self.button_hover_leave)
        self.pop.bind("<Leave>", self.hide_popup)
        self.terminal.bind("<Return>", self.parseCommand)

        self.after(1000, self.serial_poll)

    def locate2(self):
        Rssi = []
        for relay in self.relays:
            Rssi.append(relay.get_ToF())



    def locate(self):
        # right(418, 271) top(295, 147) bottom(295, 396)
        # right(123, 124) top(0  , 0  ) bottom(0  , 249)
        y1, x1 = self.relays[0].x_pos - 295, self.relays[0].y_pos - 147
        y2, x2 = self.relays[1].x_pos - 295, self.relays[1].y_pos - 147
        y3, x3 = self.relays[2].x_pos - 295, self.relays[2].y_pos - 147
        r1 = self.relays[0].get_ToF()
        r2 = self.relays[1].get_ToF()
        r3 = self.relays[2].get_ToF()
        #ic((x1, y1), r1, (x2, y2), r2, (x3, y3), r3)
        x = ((r1 ** 2) - (r2 ** 2) + (x2 ** 2)) / (2 * x2)
        y = ((r1 ** 2) - (r3 ** 2) + (x3 ** 2) + (y3 ** 2) - 2 * (x3 * x)) / (2 * y3)
        temp = y
        y = x
        x = temp
        x += 295
        y += 147

        self.Map.delete(self.rover)
        self.rover = self.Map.create_image(x, y, image=self.rover_image)
        # dist = Absolute{( RSSI + 55.5) / -0.1357}

    def serial_poll(self):

        for relay in self.relays:
            #tof = round(np.abs((random.randint(-100, -30) + 55.5) / -0.1357))
            #relay.set_ToF(tof)
            text = relay.name + f" ( {relay.x_pos}, {relay.y_pos} ) RSSI: {relay.get_ToF()}"
            if self.relayLabels[relay.count] != 0:
                self.relayLabels[relay.count].config(text=text)
            self.Map.delete(self.ovals[relay.count])
            self.ovals[relay.count] = self.Map.create_oval(relay.x_pos - relay.get_ToF(), relay.y_pos - relay.get_ToF(), relay.x_pos + relay.get_ToF(), relay.y_pos + relay.get_ToF(), width=2)
        self.locate()

        try:
            if serial.isOpen():
                inlen = serial.in_waiting
                if inlen > 0:
                    ic(inlen)
                    data = serial.read_until(expected=b'\n')[:-2]
                    message = data.decode('utf-8')
                    message.removeprefix('The Rover Says: ')
                    if message[0] == "$":
                        message = message.removeprefix("$")
                        split = message.split(':')
                        for s in split:
                            RSSI_s = s.split(',')
                            RSSI = int(RSSI_s[1])
                            distance = round(np.abs((RSSI + 55.5) / -0.1357))
                            ic(distance)
                            self.relays[int(RSSI_s[0])].set_ToF(distance)
                        self.locate2()
                    self.win_print(message)
        except AttributeError:
            print("No serial device open")
        finally:
            self.after(1000, self.serial_poll)

    def parseCommand(self, e):
        if self.terminal.get() != "":
            cmd = self.terminal.get()
            if cmd == "-help":
                txt = "Commands: " \
                      "\n-help \t    : display options" \
                      "\n-send [msg] : sends a message to rover\n"
            elif cmd.find("-send") != -1:
                msg = cmd.removeprefix("-send ")
                ic(msg)
                txt = "Base Station -> Rover> " + msg
                serial.write(msg.encode('utf-8'))
            else:
                txt = "Base Station> " + cmd
            self.win_print(txt)
            self.terminal.delete(0, tk.END)
            self.terminal.insert(tk.END, "")
            return

    def win_print(self, string):
        self.window.config(state="normal")
        self.window.insert(tk.END, string + "\n")
        self.window.yview(tk.END)
        self.window.config(state="disabled")

        return

    def clickCanvas(self, event):
        self.y_var, self.x_var = self.frame_right.grid_location(x=event.x, y=event.y)
        self.pop.grid(row=self.x_var, column=self.y_var, padx=10, pady=10)
        self.pop.lift(aboveThis=self.Map)
        print(f"Click Coordinatess: ({self.x_var}, {self.y_var})")

    def hide_popup(self, e):
        self.pop.grid_forget()

    def PlaceMarker(self, choice):

        if choice == "Relay":
            x = self.x_var + self.node_image.width() / 2
            y = self.y_var + self.node_image.height() / 2

            new_image = self.Map.create_image(y, x, image=self.node_image)
            new_relay = Relay(new_image, y, x, f"Relay {self.next_relay}", self.next_relay, 1000)
            self.Map.create_text(y, x, text=f"{self.next_relay}", font=("Roboto Medium", -20))
            self.relays.append(new_relay)
            text = new_relay.name + f" ( {new_relay.x_pos}, {new_relay.y_pos} ) RSSI: {new_relay.get_ToF()}"
            self.relayLabels[self.next_relay] = customtkinter.CTkLabel(master=self.Relay_Frame, text=text,
                                                                       text_font=("Roboto Medium", -16), padx=20)
            self.relayLabels[self.next_relay].grid(row=self.next_relay + 1, column=0, sticky='w')
            self.next_relay = (self.next_relay + 1) % 10
            ic(self.relays)

        elif choice == "Notebook":
            x = self.x_var + self.nb_image.width() / 2
            y = self.y_var + self.nb_image.height() / 2
            new_image = self.Map.create_image(y, x, image=self.nb_image)
            new_notebook = Notebook(new_image, y, x, f"Notebook {self.nbCount}")
            self.notebooks.append(new_notebook)
            self.nbCount = (self.nbCount + 1) % 10
            print(self.notebooks)

        elif choice == "Marker":
            x = self.x_var + self.marker_image.width() / 2
            y = self.y_var + self.marker_image.height() / 2
            self.Map.create_image(y, x, image=self.marker_image)
        elif choice == "Rover":
            x = self.x_var + self.rover_image.width() / 2
            y = self.y_var + self.rover_image.height() / 2
            self.Map.create_image(y, x, image=self.rover_image)
        else:
            print("ERROR> No marker choice selected.")

        self.pop.grid_forget()

    def Map_hover(self, e):
        self.y_var, self.x_var = self.frame_right.grid_location(x=e.x, y=e.y)
        x_units = self.x_var - 527
        y_units = -1 * (self.y_var - 369)
        x_meters, y_meters = UnitsToMeters(self.x_var, self.y_var)
        self.info.config(text=(
            f"Map Location> ( {self.y_var}, {self.x_var} ) meters> Approximately {np.round(np.sqrt(x_meters ** 2 + y_meters ** 2))} units away from Base Station"))

    def ToF_hover(self, e):
        self.info.config(
            text="Calculate ToF> Opens a window to input and process Time of Flight values from relay Nodes.")

    def Marker_hover(self, e):
        self.info.config(text="Place Marker> Opens a window to select a marker image and place on the Map.")

    def button_hover_leave(self, e):
        self.info.config(text="Terminal> Hover over buttons for descriptions.")

    def change_mode(self):
        if self.switch_2.get() == 1:
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def on_closing(self, event=0):
        serial.close()
        self.destroy()

    def start(self):
        self.mainloop()


def write_read(x):
    serial.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = serial.readline()[:-2]
    return data


if __name__ == "__main__":

    try:
        serial = serial.Serial(port='COM13', baudrate=9600, timeout=.1)
        time.sleep(.5)
        if not serial.isOpen():
            serial.open()
        serial.write("Hello from Python!".encode('utf-8'))
    except serial.SerialException:
        print("Error opening serial device")

    time.sleep(.5)

    app = App()
    app.start()

'''
        def locate(self):
        # right(418, 271) top(295, 147) bottom(295, 396)
        # right(123, 124) top(0  , 0  ) bottom(0  , 249)
        y1, x1 = self.relays[0].x_pos - 295, self.relays[0].y_pos - 147
        y2, x2 = self.relays[1].x_pos - 295, self.relays[1].y_pos - 147
        y3, x3 = self.relays[2].x_pos - 295, self.relays[2].y_pos - 147
        r1 = self.relays[0].get_ToF()
        r2 = self.relays[1].get_ToF()
        r3 = self.relays[2].get_ToF()
        #ic((x1, y1), r1, (x2, y2), r2, (x3, y3), r3)
        x = ((r1 ** 2) - (r2 ** 2) + (x2 ** 2)) / (2 * x2)
        y = ((r1 ** 2) - (r3 ** 2) + (x3 ** 2) + (y3 ** 2) - 2 * (x3 * x)) / (2 * y3)
        temp = y
        y = x
        x = temp
        x += 295
        y += 147

        self.Map.delete(self.rover)
        self.rover = self.Map.create_image(x, y, image=self.rover_image)
        # dist = Absolute{( RSSI + 55.5) / -0.1357}
'''
