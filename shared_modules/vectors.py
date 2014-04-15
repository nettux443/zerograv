from math import atan2, degrees, pi, sin, cos

"""
Takes two coordinates
Returns the angle from the first to the second in degrees
"""
def vectDegs(x1,y1,x2,y2):
    dx = x2 - x1
    dy = y2 - y1
    rads = atan2(-dy,dx)
    rads %= 2*pi
    degs = degrees(rads)
    return int(round(degs))

"""
Takes a start cooridinate and an angle.
Returns the x and y deltas for a single step in the given angle
"""
def vectorStep(x0, y0, degs):
    theta = pi/6
    r = 1.0
    deltax = r*cos(theta)
    deltay = r*sin(theta)
    return {"x": deltax, "y": deltay}


