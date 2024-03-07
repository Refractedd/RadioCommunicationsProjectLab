import serial
import time
from icecream import ic

base = serial.Serial(port='COM16', baudrate=9600)
if not base.isOpen():
    base.open()
arduino = serial
def uart(s):
    print(s)
    msg_out = f"{s}\r\n"
    Data_out = bytes(msg_out, 'utf-8')
    base.write(Data_out)

    time.sleep(.5)

    data_in = base.read_until(expected=b'\n')[:-2]
    message = data_in.decode('utf-8')
    print(message)
    return message

def uartWrite(s):
    print(s)
    msg_out = f"{s}\r\n"
    Data_out = bytes(msg_out, 'utf-8')
    base.write(Data_out)

def uartRead():
    time.sleep(.5)
    data_in = base.read_until(expected=b'\n')[:-2]
    message = data_in.decode('utf-8')
    print(message)
    return message


uart("AT+BAND=915000000")
uart("AT+ADDRESS=48")
uart("AT+NETWORKID=12")
uart("AT+IPR=9600")

buffer = 0
while True:
    #repl = input("->")
    uart(f"AT+SEND=49,1,B")
    time.sleep(.5)
    buffer = base.in_waiting
    print(buffer)
    while buffer == 1:
        buffer = buffer.in_waiting
        #time.sleep(.5)
    s = uartRead()
    print(s)


    #repl = input("Reply->")
    #uart(f"AT+SEND=49,{len(repl)},{repl}")

    # message = input("->")
    # msg = f"AT+SEND=59,{len(message)},{message}\r\n"
    # uart(message)
    # buffer = base.in_waiting
    # #ic(buffer)
    # if buffer > 1:
    #     s = uartRead()
    #     print(s)
    #     repl = input("->")
    #     uart(repl)




