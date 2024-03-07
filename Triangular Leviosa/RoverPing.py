import serial
import time
from icecream import ic

rover = serial.Serial(port='COM16', baudrate=9600)
if not rover.isOpen():
    rover.open()
arduino = serial


def uart(s):
    print(s)
    msg_out = f"{s}\r\n"
    Data_out = bytes(msg_out, 'utf-8')
    rover.write(Data_out)

    time.sleep(.5)
    rover.readall()
    data_in = rover.read_until(expected=b'\n')[:-2]
    message = data_in.decode('utf-8')
    print(message)
    return message


def uartWrite(s):
    print(s)
    msg_out = f"{s}\r\n"
    Data_out = bytes(msg_out, 'utf-8')
    rover.write(Data_out)

    time.sleep(.5)

    data_in = rover.read_until(expected=b'\n')[:-2]
    message = data_in.decode('utf-8')
    print(message)
    return message


def uartRead():
    data_in = rover.read_until(expected=b'\n')[:-2]
    message = data_in.decode('utf-8')
    #print(message)
    return message


EX_ADD = ["40", "41", "42"]
EX_RES = ["", "", "",]
buffer = 0

uartWrite("AT+BAND=915000000")
uartWrite("AT+ADDRESS=49")
uartWrite("AT+NETWORKID=12")
uartWrite("AT+IPR=9600")


def ping():
    buffer = rover.in_waiting

    for i in range(3):
        timeout = 0
        reply = uartWrite(f"AT+SEND={EX_ADD[i]},1,R")
        if timeout < 1:
            if reply.startswith("+RCV"):
                print(reply)
                rssi = reply.split(',')[3]
                EX_RES[i] = rssi
                print(EX_RES[i])
            else:
                timeout += 1

    text = "$0,{0}:1,{1}:2,{2}:3".format(EX_RES[0], EX_RES[1], EX_RES[2])
    return text




while True:
    ping()
    time.sleep(5)
    # message = ""
    # buffer = rover.in_waiting
    # #ic(buffer)
    # while buffer == 0:
    #     buffer = rover.in_waiting
    # s = uartRead()
    # print(s)
    # repl = input("Reply->")
    # uart(f"AT+SEND=48,{len(repl)},{repl}")



