import pygame
import nethelpers
import sprites
import json
import colours
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "shared_modules")))
import vectors
from math import atan2, degrees, pi, sin, cos

class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self, dir, x, y, colour = colours.alpha.GREEN, owner = ""):
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
        """
        if self.dir == 270:
            self.rect.x += 20
        elif self.dir == 90:
            self.rect.x -= 20
        elif self.dir == 0:
            self.rect.y -= 20
        elif self.dir == 180:
            self.rect.y += 20
        """
        delta = vectors.vectorStep(self.rect.x, self.rect.y, dir)
        self.rect.x += round((20 * delta['x']))
        self.rect.y += round((20 * delta['y']))

class Player(pygame.sprite.Sprite):
    """ This class represents the Player. """

    def __init__(self, x, y, name, colour=colours.alpha.BLACK):
        """ Set up the player on creation. """
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([20, 20])
        self.colour = colour
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
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
        # reduce the gun cooldown timer towards 0 by 1
        if self.gun_cooldown_timer > 0:
            self.gun_cooldown_timer -= 1
        else:
            # make sure we don't go negative!
            self.gun_cooldown_timer = 0
        # colour in
        self.image.fill(self.colour)
        # update position based on self.dir
        # TODO: DEGREEESSS!!!
        if self.dir != "still":
            self.look_dir = self.dir
            if self.dir == 90:
                self.rect.x -= 6
            elif self.dir == 270:
                self.rect.x += 6
            elif self.dir == 180:
                self.rect.y += 6
            elif self.dir == 0:
                self.rect.y -= 6

        # die if off the screen
        if self.rect.x > 620:
            self.dead = True
        if self.rect.x < 0:
            self.dead = True
        if self.rect.y > 460:
            self.dead = True
        if self.rect.y < 0:
            self.dead = True
        
class Wall(pygame.sprite.Sprite):
    """ Wall the player can run into. """
    def __init__(self, x, y, width, height):
        """ Constructor for the wall that the player can run into. """
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(colours.alpha.PURPLE)
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

class Dark(pygame.sprite.Sprite):
    def __init__(self, x, y):
        image = pygame.Surface([1280,960], pygame.SRCALPHA, 32)
        image = image.convert_alpha()
        image.fill(colours.alpha.BLACK)
        self.x = x + 10
        self.y = y + 10
        pygame.draw.circle(image, colours.alpha.TRANSPARENT, (self.x, self.y), 180)
        self.image = image
    def update(self, x, y, dead = False):
        self.x = x
        self.y = y
        
        image = pygame.Surface([1280,960], pygame.SRCALPHA, 32)
        image = image.convert_alpha()
        if not dead:
            image.fill(colours.alpha.BLACK)
            self.x = x + 10
            self.y = y + 10
            pygame.draw.circle(image, colours.alpha.TRANSPARENT, (self.x, self.y), 180)
        else:
            image.fill(colours.alpha.SEMI_TRANSPARENT)
        self.image = image
            
        
