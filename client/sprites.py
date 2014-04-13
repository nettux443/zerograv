import pygame
import nethelpers
import sprites
import json
from math import atan2, degrees, pi, sin, cos


# colours
BLACK    = (   0,   0,   0)
GREY     = ( 128, 128, 128)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
CYAN     = (   0, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
PURPLE   = ( 128,   0, 128)
PINK     = ( 255,   0, 255)
ORANGE   = ( 255, 165,   0)
YELLOW   = ( 255, 255,   0)
TRANSPARENT = (0,0,0,0)


class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self, dir, x, y, colour = GREEN, owner = ""):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        self.owner = owner
        self.colour = colour
        self.image = pygame.Surface([12, 12])
        self.dir = dir
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = x - 6
        self.rect.y = y - 6
        self.update()

    def update(self):
        self.image.fill(self.colour)
        """ Move the bullet. """
        if self.dir == "right":
            self.rect.x += 20
        elif self.dir == "left":
            self.rect.x -= 20
        elif self.dir == "up":
            self.rect.y -= 20
        elif self.dir == "down":
            self.rect.y += 20
        elif self.dir == "up-left":
            self.rect.y -= 10
            self.rect.x -= 10
        elif self.dir == "up-right":
            self.rect.y -= 10
            self.rect.x += 10
        elif self.dir == "down-left":
            self.rect.y += 10
            self.rect.x -= 10
        elif self.dir == "down-right":
            self.rect.y += 10
            self.rect.x += 10






class Player(pygame.sprite.Sprite):
    """ This class represents the Player. """

    def __init__(self, x, y, name, colour=BLACK):
        """ Set up the player on creation. """
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([20, 20])
        self.colour = colour
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.last_x = x
        self.last_y = y
        self.rect.x = x
        self.rect.y = y
        self.name = name
        self.dead = False
        self.firing = False
        self.fired = False
        self.dir = "still"
        self.look_dir = "right"
        self.aim_dir = "right"
        self.walled = True
        self.gun_cooldown_timer = 0
        self.gun_cooldown = 3 * 30

    def update(self):
        if self.gun_cooldown_timer > 0:
            self.gun_cooldown_timer -= 1
        self.last_x = self.rect.x
        self.last_y = self.rect.y
        self.image.fill(self.colour)
        if self.dir != "still":
            self.look_dir = self.dir
            if self.dir == "left":
                self.rect.x -= 6
            elif self.dir == "right":
                self.rect.x += 6
            elif self.dir == "down":
                self.rect.y += 6
            elif self.dir == "up":
                self.rect.y -= 6
            elif self.dir == "up-left":
                self.rect.y -= 4
                self.rect.x -= 4
            elif self.dir == "up-right":
                self.rect.y -= 4
                self.rect.x += 4
            elif self.dir == "down-left":
                self.rect.y += 4
                self.rect.x -= 4
            elif self.dir == "down-right":
                self.rect.y += 4
                self.rect.x += 4
    
        if self.rect.x > 620:
            self.dead = True
            #self.rect.x = 620
        if self.rect.x < 0:
            self.dead = True
            #self.rect.x = 0
        if self.rect.y > 460:
            self.dead = True
            #self.rect.y = 460
        if self.rect.y < 0:
            self.dead = True
            #self.rect.y = 0
        
class Wall(pygame.sprite.Sprite):
    """ Wall the player can run into. """
    def __init__(self, x, y, width, height):
        """ Constructor for the wall that the player can run into. """
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(PURPLE)
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

class Dark(pygame.sprite.Sprite):
    def __init__(self, x, y):
        image = pygame.Surface([1280,960], pygame.SRCALPHA, 32)
        image = image.convert_alpha()
        image.fill((0,0,0,255))
        self.x = x + 10
        self.y = y + 10
        pygame.draw.circle(image, TRANSPARENT, (self.x, self.y), 180)
        self.image = image
    def update(self, x, y, dead = False):
        self.x = x
        self.y = y
        
        image = pygame.Surface([1280,960], pygame.SRCALPHA, 32)
        image = image.convert_alpha()
        if not dead:
            image.fill((0,0,0,255))
            self.x = x + 10
            self.y = y + 10
            pygame.draw.circle(image, TRANSPARENT, (self.x, self.y), 180)
        else:
            image.fill((0,0,0,128))
        self.image = image
            
        
