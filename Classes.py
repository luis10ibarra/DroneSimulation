import math
import random
import matplotlib

from Visualization import *
import pylab

import drone_awe

#m = drone_awe.model({})

#m = drone_awe.model({},plot=True)
#m.simulate()


class Weather(object):

    def __init__(self, T, p, w):

        self.temp = T  ##Avg. temp. in C, 64 F  Or specify weather ... Integrate w/ Accuweather daily forecast
        self.air_density = p  # range of 99-102 kPa, 11.1 PSI or 25.6 kg/m^3
        self.wind_speed = w  # Initialy no windspeed, (Specify direction, seperaate weather class)

    def update_weather(self, T_new, p_new, w_new):

        pass






class Position(object):
    """
    A Position represents a location in a two-dimensional room, where
    coordinates are given by floats (x, y).
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_new_position(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.get_x(), self.get_y()

        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))

        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y

        return Position(new_x, new_y)

    def __str__(self):
        return "Position: " + str(math.floor(self.x)) + ", " + str(math.floor(self.y))






class SimpleNetwork(): ##ComplexNetwork, Environment w/ obstacles?
    def __init__(self, width, length, Nodes):
        """
        :param width: Int for x axis bound
        :param length: Int for y axis bound
        :param Nodes: List of network nodes, first value is Base Station loc. and rest are ClusterHeads
        """
        self.width = width
        self.length = length
        self.network = Nodes  # {cell: 0 for cell in boundary unless cell is X distance from a cluster head}

        self.emergency = [] ##Routes which can not be taken during specific emergencies
        self.clusters = {} #Cluster heads mapped to all cluster members

    def update_channels_at_pos(self, pos, amount):
        """
        Update channels available based on Cluster Head distance & Drone position by a specific amount

        :param pos:
        :param amount:
        :return:
        """
        pass

    def is_cell_available(self, m,n):
        """
        Returns True if > x channels are available,
        Returns False if < x channels are available


        :param m:
        :param n:
        :return:
        """
        pass

    def get_total_availability(self):
        """
        Return stats on coverage/dropped calls in our WSN

        :return:
        """
        pass

    def is_pos_in_room(self, pos):
        """
        Determines if pos is inside the network.

        pos: a Position object.
        Returns: True if pos is in the network, False otherwise.
        """
        x = math.floor(pos.get_x())
        y = math.floor(pos.get_y())

        position = (x, y)

        for tile in self.network:
            if tile == position:
                return True
        return False

    def get_available_channels(self, m,n):
        """
        Returns the amount of channels available at that specific cell

        :param m:
        :param n:
        :return:
        """
        return self.network[(m,n)]

    def get_num_cells(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        return self.width * self.length

    def get_random_position(self):
        """
        Returns: a Position object; a random position inside the room
        """
        x = random.uniform(0, self.width)  # random float value
        y = random.uniform(0, self.length)  # random float value

        return Position(x, y)

class Drone():

    def __init__(self, name, network, battery, speed, weight, L_D ):
        """


        ######:param BS: Tuple (x,y) of the location of the drone's Base Station (starting position)  ???

        :param network:
        :param battery: int, battery capacity in mAh
        :param speed: int, avg. speed in m/s
        :param weight: int, payload weight in grams
        :param L_D: float,  Lift/Drag ratio (unitless)
        """

        self.name = name
        #self.pos = network.get_random_position()
        self.direction = 0 #Facing North, (degrees measured CW)

        self.network = network
        self.battery = battery ### Option for 2s, 3s, etc.
        self.speed = speed
        self.weight = weight #kg
        self.L_D = L_D #For fixed wing values are inbetween .10 - .30

    #Energy consumption at each stage

    def get_drone_position(self):
        """
        Returns: a Position object giving the drone's position in the room.
        """
        return self.position

    def get_drone_direction(self):
        """
        Returns: a float d giving the direction of the drone as an angle in
        degrees, 0.0 <= d < 360.0.
        """
        return self.direction

    def set_drone_position(self, position):
        """
        Set the position of the drone to position.

        position: a Position object.
        """
        self.position = position

    def set_drone_direction(self, direction):
        """
        Set the direction of the drone to direction.

        direction: float representing an angle in degrees
        """
        self.direction = direction

    def update_position(self):
        """
        Simulates the passage of a single time-step.

        Moves drone to new position and cleans tile according to drone movement
        rules.
        """
        # do not change -- implement in subclasses
        raise NotImplementedError



class StandardDrone(Drone):

    ###Set channel amount
    ###Set dropped call probability
    ##More?


    def update_position_and_clean(self):
        """
        Simulates the passage of a single time-step.

        Calculate the next position for the robot.

        If that position is valid, move the robot to that position. Mark the
        tile it is on as having been cleaned by capacity amount.

        If the new position is invalid, do not move or clean the tile, but
        rotate once to a random new direction.
        """

        #print("in here x2")
        newPosition = self.get_drone_position().get_new_position(self.get_drone_direction(), self.speed)

        #if self.network.is_pos_in_room(newPosition):
            #print("new pos updated", newPosition)

        self.set_drone_position(newPosition)  # updating position

        #else:  # if position isn't valid
            #print("random direction")
            #self.set_drone_direction(random.uniform(0, 360))  # get new random direction



