from math import atan2, degrees, radians, pi, sin, cos, tan, sqrt

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
Takes a start cooridinate and an angle read anticlockwise from the x axis
Returns the x and y deltas for a single step in the given angle
"""
def vectorStep(x, y, degs):
    if degs < 0:
        return {"x": 0, "y": 0}
    real_degs = degs
    while degs >= 90:
        degs -= 90 
    m = tan(radians(degs))
    deltax = sqrt(1/(m**2+1))
    deltay = (m * deltax)

    if real_degs < 90:
        # we are in top right quadrant
        oldx = deltax
        if deltay != 0:
            deltay *= -1
        deltax = deltay
        deltay = oldx
        
    elif real_degs < 180:
        # we are in bottom right quadrant
        if deltax > 0:
            deltax *= -1
    elif real_degs < 270:
        # we are in bottom left quadrant
        oldy = deltay
        if deltay != 0:
            deltax *= -1
        deltay = deltax
        deltax = oldy
    elif real_degs < 360:
        # we are in top left quadrant
        deltay = deltay
    else:
        return {"x": 0, "y": 0}

    return {"x": deltax, "y": deltay}
