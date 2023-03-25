from vpython import *
from gui_control import *
import atexit
import math

##########################
###### GLOBAL VARS  ######
##########################

class g: 
    earth_rad = 10
    sun_rad = 20
    earth_orbit_rad = 250
    mercury_rad = 10
    mercury_orbit_rad = 100
    mercury_rod_len = 600
    
    def monitor_loop():
        monitor_pause()
        monitor_terminate()

##########################
##### TIME CLASS #####
##########################

class time:
    t = 0
    end = 1000
    delta = 0.3
    rate = 60



##########################
##### WRAPPER CLASS ######
##########################

# wrapper class for box that places pos at the end of the rectangle rather than the center
# and also tracks the head and tail of the rectangle
# docs: https://www.glowscript.org/docs/VPythonDocs/box.html
class new_rect:
    # pos is where to place the end of the rectangle
    def __init__(self, pos : vector, length_dim, side_dim, color_in : color):
        self.rect = box(length = length_dim, width = side_dim, height= side_dim, color= color_in)
        self.pos_head = vector(0,0,0)
        self.pos_tail = vector(length_dim,0,0)
        self.length = length_dim
        self.place_pos(pos)

    # pos indicates where you want the end to placed
    def place_pos(self, pos_in : vector):
        vec_mag = self.length
        vec_norm = norm(self.rect.axis)
        self.rect.pos = pos_in
        self.rect.pos.x += vec_mag * vec_norm.x/2
        self.rect.pos.y += vec_mag * vec_norm.y/2

        # update head and tail of the rectangle
        self.pos_head = pos_in
        self.pos_tail = self.pos_head + self.rect.axis

    # update the direction in which the rectangle points
    def place_axis(self, axis_in : vector):
        # original approach, find angle between vectors and then rotate og vector
        # problem: need to determine sign for theta based on planets positions
        # theta = math.acos(dot(self.rect.axis, axis_in)/ mag(self.rect.axis) / mag(axis_in))
        # self.rect.rotate(angle = theta, origin = self.pos_head, axis = vector(0,0,1))

        # second approach
        # extend a vector's magnitude but maintain direction
        self.rect.axis = hat(axis_in) * mag(self.rect.axis)
        self.place_pos(self.pos_head)


##########################
######  AXIS CLASS  ######
##########################

class axis:
    def __init__(self, length):
        self.yaxis = arrow(pos=vector(0,-length,0), axis=vector(0, length << 1,0), shaftwidth=5, color=color.green, headwidth = 5 ) 
        self.xaxis = arrow(pos=vector(-length,0,0), axis=vector(length << 1,0,0), shaftwidth=5, color=color.red, headwidth = 5 )
        self.zaxis = arrow(pos=vector(0,0,-length), axis=vector(0,0,length << 1), shaftwidth=5, color=color.blue, headwidth = 5 )
        

##########################
######     MAIN     ######
##########################

if __name__ == "__main__":

    scene = canvas(height=800,width=800)
    earth = sphere(pos= vector(0,g.earth_orbit_rad, 0), color = color.green, radius = g.earth_rad)
    sun = sphere(pos= vector(0,0,0), color = color.yellow, radius = g.sun_rad)
    mercury = sphere(pos = vector(0, g.mercury_orbit_rad, 0), radius = g.mercury_rad ,color= color.gray(0.6))
    mercury_stick = new_rect(vector(0,g.earth_orbit_rad,0), g.mercury_rod_len, 5, color.purple)
    mercury_retrograde = sphere(color = color.purple, radius = 5, make_trail = True)

    # plot coordinate grid
    grid = axis(200)


    while time.t < time.end:
        rate(time.rate)

        g.monitor_loop()

        earth.rotate(angle=radians(0.3), axis = vector(0,0,1), origin=vector(0,0,0))
        mercury.rotate(angle=radians(2), axis = vector(0,0,1), origin = vector(0,0,0))

        mercury_stick.place_pos(earth.pos)

        # get intersect
        # rect is represented by length of rod_len. 
        # then you also have the position of mercury
        # test by moving around mercury and seeing if it works.
        denom = (mercury.pos.x - earth.pos.x)
        num = (mercury.pos.y - earth.pos.y)
        slope = 0
        if denom < 0.0001 and denom > -0.0001:
            slope = 1e8
        else:
            slope = num / denom
        b = (earth.pos.y - slope*earth.pos.x)
        # print("slope", slope, "b", b)

        mercury_stick.place_axis(vector(denom, num, 0))
        mercury_retrograde.pos = mercury_stick.pos_tail


        time.t += time.delta



