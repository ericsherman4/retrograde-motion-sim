from vpython import *
from gui_control import *
import atexit

class g: 
    earth_rad = 10
    sun_rad = 30
    earth_orbit_rad = 150
    mercury_rad = 10
    mercury_orbit_rad = 100
    mercury_rod_len = 200
    pass

class time:
    t = 0
    end = 1000
    delta = 0.3
    rate = 60

# wrapper class for box that places pos at the end of the rectangle rather than in the middle
class new_rect:
    # pos is where to place the end of the rectangle
    def __init__(self, pos : vector, length_dim, side_dim, color_in : color):
        self.rect = box(length = length_dim, width = side_dim, height= side_dim, color= color_in)
        self.pos = vector(0,0,0)
        self.length = length_dim
        self.place(pos)

    # pos indicates where you want the end to placed
    def place(self, pos_in : vector):
        vec_mag = self.length
        vec_norm = norm(self.rect.axis)
        # print("vec_mag", vec_mag)
        # print("norm", vec_norm)
        self.rect.pos = pos_in
        self.rect.pos.x += vec_mag * vec_norm.x/2
        self.rect.pos.y += vec_mag * vec_norm.y/2

        self.pos = pos_in
        # print(self.pos)
        # print(self.rect.pos)


if __name__ == "__main__":

    scene = canvas()
    earth = sphere(pos= vector(0,g.earth_orbit_rad, 0), color = color.green, radius = g.earth_rad)
    sun = sphere(pos= vector(0,0,0), color = color.yellow, radius = g.sun_rad)
    mercury = sphere(pos = vector(0, g.mercury_orbit_rad, 0), radius = g.mercury_rad ,color= color.gray(0.6))
    mercury_stick = new_rect(vector(0,g.earth_orbit_rad,0), g.mercury_rod_len, 5, color.purple)

    # get intersect
    # rect is represented by length of rod_len. 
    # then you also have the position of mercury
    # test by moving around mercury and seeing if it works.


    #plot axis
    length = 200
    yaxis = arrow(pos=vector(0,-length,0), axis=vector(0, length << 1,0), shaftwidth=5, color=color.green, headwidth = 5 ) 
    xaxis = arrow(pos=vector(-length,0,0), axis=vector(length << 1,0,0), shaftwidth=5, color=color.red, headwidth = 5 )
    zaxis = arrow(pos=vector(0,0,-length), axis=vector(0,0,length << 1), shaftwidth=5, color=color.blue, headwidth = 5 )


    

    while time.t < time.end:
        rate(time.rate)

        monitor_pause()
        monitor_terminate()

        # earth.rotate(angle=radians(2), axis = vector(0,0,1), origin=vector(0,0,0))
        # mercury.rotate(angle=radians(4), axis = vector(0,0,1), origin = vector(0,0,0))
        # time.t += time.delta



