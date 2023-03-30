from vpython import *
from gui_control import *
import atexit
import math

##########################
###### GLOBAL VARS  ######
##########################

class g: 
    vel_scale = 109
    earth_rad = 17
    sun_rad = 25
    earth_orbit_rad = 250
    earth_orbit_vel = 1/ 365 * vel_scale
    mercury_rad = 15
    mercury_orbit_rad = 100
    mercury_rod_len = 600
    mercury_orbit_vel = 1 / 88 * vel_scale
    venus_rad = 20
    venus_orbit_rad = 200
    venus_rod_len = 800
    venus_orbit_vel = 1/ 255 * vel_scale
    mars_rad = 17
    mars_orbit_rad = 300
    mars_rod_len = 900
    mars_orbit_vel = 1/ 687 * vel_scale
    
    
    def monitor_loop():
        monitor_pause()
        monitor_terminate()

##########################
##### TIME CLASS #####
##########################

class time:
    t = 0
    end = 13000
    delta = 0.3
    rate = 500



##################################
##### WRAPPER CLASS FOR REC ######
##################################

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
    
################################
### RETROGRADE PLANET CLASS  ###
################################

class retrograde_planet:

    def __init__(self, orbit_rad, planet_rad, color_in : color, stick_len, orbit_vel):
        self.planet = sphere(pos =vector(0, orbit_rad,0), color=color_in, radius = planet_rad)
        self.stick = new_rect(vector(0, g.earth_orbit_rad, 0), stick_len, 5, color_in)
        self.trace = sphere(color = color_in, radius = 5, make_trail = True, trail_radius = 3)
        self.orbit_vel = orbit_vel

    def update(self, earth_pos : vector):

        # make the planet orbit
        self.planet.rotate(angle=radians(self.orbit_vel), axis = vector(0,0,1), origin = vector(0,0,0))

        # place the end of the stick at earth's new position
        self.stick.place_pos(earth_pos)
        
        # determine stick slope between earth and the planet
        xdelta = (self.planet.pos.x - earth_pos.x)
        ydelta = (self.planet.pos.y - earth_pos.y)
        
        # update what direction stick points in
        self.stick.place_axis(vector(xdelta, ydelta, 0))

        # place trace planet at end of the stick
        self.trace.pos = self.stick.pos_tail


################################
####  RETROGRADE SIM CLASS  ####
################################

class retrograde_sim:
    
    def __init__(self, earth_orbit_vel):
       # create the earth and sun
       self.earth = sphere(pos= vector(0,g.earth_orbit_rad, 0), color = color.green, radius = g.earth_rad) 
       self.sun = sphere(pos= vector(0,0,0), color = color.yellow, radius = g.sun_rad)
       self.earth_orbit_vel = earth_orbit_vel

       # list to hold retrograde planets
       self.planets = list()

    def add_planet(self, orbit_rad, planet_rad, color_in : color, stick_len, orbit_vel):
        self.planets.append(retrograde_planet(orbit_rad, planet_rad, color_in, stick_len, orbit_vel))

    def update(self):
        self.earth.rotate(angle=radians(self.earth_orbit_vel), axis = vector(0,0,1), origin=vector(0,0,0))
        for planet in self.planets:
            planet.update(self.earth.pos)


##########################
######     MAIN     ######
##########################

if __name__ == "__main__":

    # create the scene
    scene = canvas(height=1000,width=1900)

    # plot coordinate grid
    grid = axis(200)

    # create simulation and add planets
    rs = retrograde_sim(g.earth_orbit_vel)
    rs.add_planet(g.mercury_orbit_rad, g.mercury_rad, color.gray(0.6), g.mercury_rod_len, g.mercury_orbit_vel)
    rs.add_planet(g.venus_orbit_rad, g.venus_rad, color.orange, g.venus_rod_len, g.venus_orbit_vel)
    rs.add_planet(g.mars_orbit_rad, g.mars_rad, color.red, g.mars_rod_len, g.mars_orbit_vel)

    while time.t < time.end:
        # rate limit loop
        if(time.t > 500):
            rate(400)
        else:
            rate(100)
        # print(time.t)

        # monitor keyboard inputs
        g.monitor_loop()

        # update simulation
        rs.update()

        # increment time
        time.t += time.delta

    while(True):
        g.monitor_loop()
        


