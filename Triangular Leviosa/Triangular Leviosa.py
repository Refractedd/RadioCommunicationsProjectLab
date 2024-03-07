import serial
from main import *
import matplotlib.pyplot as plt
import matplotlib.patches as shape
import numpy as np
# https://journals.sagepub.com/doi/full/10.5772/63246#fig1-63246
'''serial = serial.Serial('COM9', 9600)'''

x1 = 418
y1 = 262
x2 = 316
y2 = 147
x3 = 295
y3 = 396

x1=0
x2=102
x3=0
y1=147
y2=262
y3=396

r1 = 217
r2 = 232
r3 = 262

x = ((r1**2)-(r2**2) + (x2**2)) / (2 * x2)
y = ((r1**2)-(r3**2) + (x3**2)+(y3**2)-2*(x3*x)) / (2*y3)

print(x, y)
'''
ToF_1 = 60     # nS
ToF_2 = -60
ToF_3 = 150

relay_1_pos = (0, 0)
relay_2_pos = (100, 100)
rover_pos = (50, 50)
r1_center = (25,25)

plt.axes()
rect_1 = plt.Rectangle(relay_1_pos, ToF_1, ToF_1, fill=False)
rect_2 = plt.Rectangle(relay_2_pos, ToF_2, ToF_2, fill=False)

circle_1 = plt.Circle(relay_1_pos, ToF_1, fill=False, color='blue')

dot = plt.Circle(rover_pos, 1, color='black')
plt.gca().add_patch(rect_1)
plt.gca().add_patch(rect_2)
plt.gca().add_patch(dot)
plt.gca().add_patch(circle_1)

plt.axis('scaled')
plt.show()


xi = (c1 - c2) / (m2 - m1)
yi = m1 * xi + c1

plt.axvline(x=xi, color='gray', linestyle='--')
plt.axhline(y=yi, color='gray', linestyle='--')

plt.scatter(xi, yi, color='black')

plt.show()

#if __name__ == "__main__":
#    app = App()
#    app.start()
'''
