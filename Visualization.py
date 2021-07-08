import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

import math
import time as t
import base64
from tkinter import *
from urllib.request import urlopen
import numpy as np





###Visual for Cost of UAV travel b/w nodes

class DroneVisualization:
    def __init__(self, num_drones, width, height, delay = 0.1 ):
        # Number of seconds to pause after each frame
        self.delay = delay

        self.max_dim = max(width, height)
        self.width = width
        self.height = height
        self.num_drones = num_drones

        # Initialize a drawing surface
        self.master = Tk()
        self.w = Canvas(self.master, width=500, height=500)
        self.w.pack()
        self.master.update()

        # Draw a backing and lines
        x1, y1 = self._map_coords(0, 0) ##MapCOORDS (READ DOCS), curvature???
        x2, y2 = self._map_coords(width, height)
        self.w.create_rectangle(x1, y1, x2, y2, fill="white")


        v1 = (1500,67)
        v2 = (1000,67)
        v3 = (750,500)
        v4 = (1000,933)
        v5 = (1500 ,933)
        v6 = (1750,500)

        x1,y1 = self._map_coords(v1[0],v1[1])
        x2,y2 = self._map_coords(v2[0],v2[1])

        x3, y3 = self._map_coords(v3[0], v3[1])
        x4, y4 = self._map_coords(v4[0], v4[1])

        x5, y5 = self._map_coords(v5[0], v5[1])
        x6, y6 = self._map_coords(v6[0], v6[1])

        ##Draw sample WSN with one Hexagon Cell

        self.w.create_line(x1, y1, x6, y6, width=2)
        self.w.create_line(x1,y1, x2, y2, width =2)
        self.w.create_line(x2, y2, x3, y3, width=2)
        self.w.create_line(x3, y3, x4, y4, width=2)
        self.w.create_line(x4, y4, x5, y5, width=2)
        self.w.create_line(x5, y5, x6, y6, width=2)
        
        #self.w.create_polygon(x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6)
        

        ##Some Text
        self.drones = None
        self.text = self.w.create_text(25, 0, anchor=NW, text=self._status_string(0, 0, 1))
        self.time = 0

        # Bring window to front and focus
        self.master.attributes("-topmost", True)  # Brings simulation window to front upon creation
        self.master.focus_force()  # Makes simulation window active window
        self.master.attributes("-topmost", False)  # Allows you to bring other windows to front

        self.master.update()

    def _status_string(self, time, num_clean_tiles, num_total_tiles):
        "Returns an appropriate status string to print."
        channels_available = 10
        status = "Time: " + str(time) + "s. ; ValidChannel" \
                                        "" \
                                        "" \
                                        "" \
                                        "" \
                                        "" \
                                        "s: " + str(num_clean_tiles) + " with a " + str(num_total_tiles) + "% dropped call probability."

        return status

    def _map_coords(self, x, y):
        "Maps grid positions to window positions (in pixels)."
        return (250 + 450 * ((x - self.width / 2.0) / self.max_dim),
                250 + 450 * ((self.height / 2.0 - y) / self.max_dim))

    def _draw_robot(self, position, direction):
        "Returns a polygon representing a robot with the specified parameters."
        x, y = position.get_x(), position.get_y()
        d1 = direction + 165
        d2 = direction - 165
        x1, y1 = self._map_coords(x, y)
        x2, y2 = self._map_coords(x + 60 * math.sin(math.radians(d1)),
                                  y + 60 * math.cos(math.radians(d1)))
        x3, y3 = self._map_coords(x + 60 * math.sin(math.radians(d2)),
                                  y + 60 * math.cos(math.radians(d2)))

        return self.w.create_polygon([x1, y1, x2, y2, x3, y3], fill="red")

    def update(self, network, drones):


        # Delete all existing robots.

        if self.drones:
            for drone in self.drones:
                self.w.delete(drone)
                self.master.update_idletasks()



        # Draw new robots
        self.drones = [] ######################
        for drone in drones:
            pos = drone.get_drone_position()
            #print(pos)
            x, y = pos.get_x(), pos.get_y()
            x1, y1 = self._map_coords(x - 8, y - 8)
            x2, y2 = self._map_coords(x + 8, y + 8)
            self.drones.append(self.w.create_oval(x1, y1, x2, y2, fill="black"))
            self.drones.append(self._draw_robot(drone.get_drone_position(), drone.get_drone_direction()))
            #print(self.drones)
        # Update text
        self.w.delete(self.text)
        self.time += 1
        self.text = self.w.create_text(25, 0, anchor=NW, text=self._status_string(self.time, 0, 1))

        self.master.update()
        t.sleep(self.delay)
        #print("end")




    def done(self):
        "Indicate that the animation is done so that we allow the user to close the window."
        mainloop()





def test_drone_movement(drone_type, network_type):

    drones =  [drone_type] # room_type(2000, 1000, [(0,250),(1000,250),(1500,1750)] ) #2000, 1000, [(0,250),(1000,250),(1500,1750)]
    network = network_type #[robot_type("DJJ_Mini_2",room_type,2250,15, .250, .30)]
    coverage = 0
    time_steps = 0
    min_coverage = 1.0
    anim = DroneVisualization(1, 2000, 1000)

   #print("in here")
    #print(robots[0].position)
    #print(robots[0].direction)

    while time_steps < 100: #coverage < min_coverage
        time_steps += 1
        for drone in drones:

            drone.update_position_and_clean()
            #print(robot.position)
            anim.update(network, drones)
            #coverage = float(room.get_num_cleaned_tiles())/room.get_num_tiles()

    anim.done()



##Visual of channels, dropped calls, QoS  (Dashboard??)

import numpy as np
from matplotlib import cm
from colorspacious import cspace_converter
from collections import OrderedDict



"""
network = {"base": (0,250),
           "a":(1000,250),
           "b":(1500,1750),
           "c":(750,1250),
           }


X = []
Y = []


for loc in network:
    if loc == 'base':
        pass
    else:
        ##Plot CH Location
        x,y = network[loc]
        X.append(x)
        Y.append(y)

        ##Plot coverage area (Hexagon, Voronoi)

        #hexagon((x,y))



plt.ylim([0,2000])
plt.xlim([0,2000])

#YlGn,YlGnBu,G
plt.scatter(network['base'][0], network['base'][1], color ='red' )

#plt.scatter(X,Y, color ='blue')
#plt.hexbin(X,Y, cmap= 'YlGn', gridsize=4, edgecolors= 'black')


#fig, ax = plt.subplots(1)
#ax.set_aspect('equal')

#hex = RegularPolygon((250, 250), numVertices=6, radius=150. / 3., orientation=np.radians(30), facecolor='Green', alpha=0.2, edgecolor='k')
#ax.add_patch(hex)


plt.show()

"""



