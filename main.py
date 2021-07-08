from Classes import *



def calculate_distance(loc1,loc2):
    """
    Currently calculating straight line distance, eventually include the estimate for curvature of earth (6.009 pset)

    :param loc1: Tuple (x1, y1)
    :param loc2: Tuple (x2, y2)
    :return: dist: Float
    """

    x1, y1 = loc1
    x2, y2 = loc2

    return round(math.sqrt((x2-x1)**2 + (y2-y1)**2), 2)


def calculate_EC_steady1(drone, network):
    """

    Simplification: Thrust = Weight = (mass * 9.81) * L/D Ratio

    :param drone: class obj
    :param network: class obj
    :return: EnergyConsumption: Float
    """

    baseStation = simpleNetwork.network[0]
    drone.position = Position(baseStation[0], baseStation[1])
    nodes = simpleNetwork.network[1:]
    print("Drone will travel from base station to, " ,nodes)
    print("---------------------------------------------------")


    dist1 = calculate_distance(baseStation, nodes[0])
    print("Drone travels ", dist1, "meters from ", baseStation, " to ", str(nodes[0]))

    dist2 = calculate_distance(nodes[0], nodes[1])
    print("Drone travels ", dist2, "meters from ", str(nodes[0]), " to ", str(nodes[1]))

    dist3 = calculate_distance(nodes[1], baseStation)
    print("Drone travels ", dist3, "meters from ", str(nodes[1]), " to ", baseStation)

    totalDistance = dist1 + dist2 + dist3


    #Energy (Flight) = Thrust x Distance. (Steady flight, thrust = drag = (mass x gravity)/L_D ratio) (Wind???)
    #Energy (Avionics) = avionics constant x Distance (??)

    thrust = round((drone.weight * 9.801) / drone.L_D, 2)
    ##lift = __ include lift????
    #drag = .2 * p * v * v * C * ()
    #thrust = math.sqrt(drone.weight**2 + drag**2)

    energy = round((thrust * totalDistance)/3600, 2) ##In Joules, kgm^2/s^2 ->> Wh
    #energy = (drone.weight * drone.speed) / (370 * drone.L_D*.8)


    remainingCapacity = (drone.battery - 1000*energy/ 7.4  ) #In mAh ###2s,

    print("---------------------------------")
    print(thrust, "Newtons of thrust needed to fly w/o wind")

    time = round(totalDistance/drone.speed/60,2)
    print(energy, "Wh lost and would take ", time," minutes cruising in flight.")

    print("drone battery remaining : ", round(remainingCapacity, 2) , "mAh")


    ####Travel amongst nodes: BS -> Cell (CH1 -> CH2 ?)
    ####Hovering at node/cell (?)





def calculate_EC_steady2(drone, network, theta):
    """

    Simplification: Thrust = (W^2 + D^2)**.5 flying at some angle THETA

    :param drone: class obj
    :param network: class obj
    :return: EnergyConsumption: Float
    """

    return None

def calculate_EC_hover(drone,network):
    """

    Simplifications:

    :param drone: class obj
    :param network: class obj
    :return: EnergyConsumption: Float
    """

    return None




#4 stages of flight: Takeoff, hover, steady, land + communications (FUTURE)




def travel(drone,network):
    """

    Run the simulation that will show the drones flight path in the WSN

    :param drone: class obj
    :param network: class obj
    :return: None
    """

    #print("---------------------------------")
    #print("Integrate with visualization")

    baseStation = simpleNetwork.network[0]
    drone.position = Position(baseStation[0], baseStation[1])
    #print(drone.position)

    nodes = simpleNetwork.network[1:]

    #newPos = drone.position.get_new_position(90,drone.speed)
    #drone.set_drone_position(newPos)


    drone.set_drone_direction(90)
    #print(drone.position)

    test_drone_movement(drone, network)




if __name__ == '__main__':

    simpleNetwork = SimpleNetwork(2000, 1000, [(0,250),(1000,250),(1500,1750)])
    drone = StandardDrone("DJJ_Mini_2",simpleNetwork,2250,15, .250, .75)

    #drone = StandardDrone("EVO_2_Pro", simpleNetwork,7100,10,1.174,.30)


    calculate_EC_steady1(drone, simpleNetwork)
    travel(drone,simpleNetwork)



