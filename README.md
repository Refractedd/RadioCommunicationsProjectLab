# Triangular Leviosa
This is a Project created by Benjamin Williams, Devin Shade, and Megan Leeman for Project Lab III at Texas Tech University

https://github.com/Refractedd/RadioCommunicationsProjectLab/assets/80213576/5367a979-eefc-4d6d-8777-c883ad75f4e2

## What Problem does it solve?
Project Lab III groups must use Radio Frequency Communication devices to:
- Provide constant location tracking of one teammate acting as a 'Rover.'
- This 'Rover' must move around campus looking for notebooks containing a 'Codeword'.
- Constant radio message communication must be established between the rover and base station
- Groups must find at least 3 of 5 notebooks and comminicate back to the base station to recieve the page, line, and word number of the codeword to send back.
  
## How did you solve it?
Triangular Leviosa is a GUI complete with a messaging terminal, a map canvas, and an informational textbox. The algorithm works by:
1. The rover sends out a ping message to the 3 pre-positioned relay stations.
2. The relays reply with the RSSI value of the message.
3. The rover transmits these 3 RSSI values back to base station.
4. The base station uses the 3 RSSI values effectively as Time of Flight (ToF) in a trilateration algorithm to re-position the rover icon on the map as shown in the video.
5. The terminal can be used at any time to communicate to the rover.

## Rover GUI
The rover also has a GUI for sending messages to the base station and doing radio pings in the background.
![image](https://github.com/Refractedd/RadioCommunicationsProjectLab/assets/80213576/5d107ecd-150c-4a3c-84e3-3851f45dc603)



