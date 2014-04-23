class alpha:
    BLACK    = (   0,   0,   0, 255)
    GREY     = ( 128, 128, 128, 255)
    WHITE    = ( 255, 255, 255, 255)
    BLUE     = (   0,   0, 255, 255)
    CYAN     = (   0, 255, 255, 255)
    GREEN    = (   0, 255,   0, 255)
    DARK_GREEN    = (   0, 192,   0, 255)
    RED      = ( 255,   0,   0, 255)
    PURPLE   = ( 128,   0, 128, 255)
    PINK     = ( 255,   0, 255, 255)
    ORANGE   = ( 255, 165,   0, 255)
    YELLOW   = ( 255, 255,   0, 255)
    TRANSPARENT = (0,0,0,0)
    SEMI_TRANSPARENT = (0,0,0,128)
    
    def colourize(colour_string):
        if colour == "yellow":
            return  alpha.YELLOW
        elif colour == "blue":
            return  alpha.BLUE
        elif colour == "cyan":
            return  alpha.CYAN  
        elif colour == "red":
            return  alpha.RED
        elif colour == "orange":
            return  alpha.ORANGE
        elif colour == "pink":
            return  alpha.PINK
        elif colour == "green":
            return  alpha.GREEN
        # the given colour couldn't be matched
        return False
 
class nonalpha:
    BLACK    = (   0,   0,   0)
    GREY     = ( 128, 128, 128)
    WHITE    = ( 255, 255, 255)
    BLUE     = (   0,   0, 255)
    CYAN     = (   0, 255, 255)
    GREEN    = (   0, 255,   0)
    DARK_GREEN    = (   0, 192,   0,)
    RED      = ( 255,   0,   0)
    PURPLE   = ( 128,   0, 128)
    PINK     = ( 255,   0, 255)
    ORANGE   = ( 255, 165,   0)
    YELLOW   = ( 255, 255,   0)
    def colourize(colour_string):
        if colour == "yellow":
            return  nonalpha.YELLOW
        elif colour == "blue":
            return  nonalpha.BLUE
        elif colour == "cyan":
            return  nonalpha.CYAN  
        elif colour == "red":
            return  nonalpha.RED
        elif colour == "orange":
            return  nonalpha.ORANGE
        elif colour == "pink":
            return  nonalpha.PINK
        elif colour == "green":
            return  nonalpha.GREEN
        # the given colour couldn't be matched
        return False

