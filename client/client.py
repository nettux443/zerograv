#!/usr/bin/python

import pygame
import nethelpers
import sprites
import json
import random
import os
import colours

from math import atan2, degrees, pi, sin, cos

"""
Takes a colour string
returns the corresnponding colour constant
"""
def colourize(colour_string):
    if colour == "yellow":
        return  colours.alpha.YELLOW
    elif colour == "blue":
        return  colours.alpha.BLUE
    elif colour == "cyan":
        return  colours.alpha.CYAN  
    elif colour == "red":
        return  colours.alpha.RED
    elif colour == "orange":
        return  colours.alpha.ORANGE
    elif colour == "pink":
        return  colours.alpha.PINK
    elif colour == "green":
        return  colours.alpha.GREEN
    # the given colour couldn't be matched
    return False

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

"""
Takes an array of keys
Returns a direction for movement as a string
TODO: use degrees here!!
"""
def getDir(keys):
    # assume that we aren't moving to begin with
    dir = "still"
    # if we are press an arrow key, move that way
    if keys[pygame.K_LEFT]:
        dir = "left"
    if keys[pygame.K_RIGHT]:
        # if we are press right and left just stay still
        if dir == "left":
            dir = "still"
        else:
            dir = "right"
    if keys[pygame.K_UP]:
        if dir == "down":
            dir = "still"
        else:
            dir = "up"
    if keys[pygame.K_DOWN]:
        if dir == "up":
            dir = "still"
        else:
            dir = "down"
    return dir

"""
Takes a list of currently pressed keys
Returns a direction string for aim direction based on the keys
TODO: use degress here!!!!!
"""
def getAimDir(keys):
    # initialise to still
    dir = "still"
    if keys[pygame.K_s]:
        dir = "down"
    if keys[pygame.K_w]:
        dir = "up"
    if keys[pygame.K_a]:
        dir = "left"
    if keys[pygame.K_d]:
        dir = "right"
    return dir



"""
Converse with the server
takes the player's sprite object  and a sound object to play when firing
returns info on all other clients from the server
"""
def getServerData(me, laser_sound):
    # if dead just send the dead action and put you at (0, 0)
    if me.dead:
        data = server.sendToServer({"x": 0, "y": 0, "s": "none", "t": token, "u": username, "a": "dead"})
    elif me.firing and me.gun_cooldown_timer <= 0:
        # we want to and can fire
        me.gun_cooldown_timer = me.gun_cooldown
        laser_sound.play()

        if not me.walled:
            # if we shoot in mid-air go flying off in the opposite direction
            # TODO: use degrees!!
            if me.aim_dir == "left":
                me.dir = "right"
            elif me.aim_dir == "right":
                me.dir = "left"
            elif me.aim_dir == "up":
                me.dir = "down"
            elif me.aim_dir == "down":
               me.dir = "up"
            # send my location and the direction that I'm shooting in
        data = server.sendToServer({"x": me.rect.x, "y": me.rect.y, "s": me.aim_dir, "t": token, "u": username, "a": "none"})
    else:
        # not shooting so just send my position
        data = server.sendToServer({"x": me.rect.x, "y": me.rect.y, "s": "none", "t": token, "u": username, "a": "none"})
    return data

def drawMap(wall_list):
    # middle wall
    wall_list.add(sprites.Wall(315, 100, 10, 260))

    # L shape left
    wall_list.add(sprites.Wall(30, 40, 10, 160))
    wall_list.add(sprites.Wall(30, 200, 100, 10))

    # L shape right
    wall_list.add(sprites.Wall(600, 40, 10, 160))
    wall_list.add(sprites.Wall(510, 200, 100, 10))

    # lower wall
    wall_list.add(sprites.Wall(140, 420, 360, 10))

    # upper wall
    wall_list.add(sprites.Wall(150, 20, 340, 10))
    
    # left box
    wall_list.add(sprites.Wall(50, 290, 150, 20))

    # right box
    wall_list.add(sprites.Wall(440, 290, 150, 20))

    # r shape left
    wall_list.add(sprites.Wall(180, 150, 10, 90))
    wall_list.add(sprites.Wall(190, 150, 60, 10))

    # r shape right
    wall_list.add(sprites.Wall(450, 150, 10, 90))
    wall_list.add(sprites.Wall(390, 150, 60, 10))

"""
takes a Player sprite object
sets that object's .dead attribute to False and spawns it randomly(-ish)
"""
def spawn(player):
    # set the player to alive
    player.dead = False
    # make a random number
    ran = random.random()
    # spawn player at a spawn point chosen based on ran
    if ran < 0.25:
        player.rect.x = 40
        player.rect.y = 120
    elif ran < 0.5:
        player.rect.x = 580
        player.rect.y = 120
    elif ran < 0.75:
        player.rect.x = 190
        player.rect.y = 170
    else:
        player.rect.x = 430
        player.rect.y = 170
    return True


# prompt for username, colour and server to connect to
# TODO: Add GUI menus for player name and server ip:port
server_ip = raw_input("Server IP/hostname? ")
server_port = raw_input("Server port? ")
server = nethelpers.server(server_ip, server_port)
username = raw_input("Username? ")
while True:
    colour = raw_input("Colour? ")
    # normalize
    colour = colour.strip().lower()
    # convert choice to constant
    player_colour = colourize(colour)
    if player_colour != False:
        break
    # re-prompt if there was no constant
    print "Choose: yellow, orange, pink, blue, red, cyan or green."


# initialize pygame
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.mixer.init()

# set up a basic font object to use
font=pygame.font.Font(None,18)
# Set the width and height of the screen [width, height]
size = (640, 480)
window = pygame.display.set_mode(size)

screen = pygame.Surface(size)

pygame.display.set_caption("zerograv")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Hide the mouse cursor
pygame.mouse.set_visible(0)
look_dir = "right"
token = server.handshake(username)
bullet_list = pygame.sprite.Group()
player_list = pygame.sprite.Group()
me = sprites.Player(0 , 0, username, player_colour)
spawn(me)
dark = sprites.Dark(me.rect.x, me.rect.y)
player_list.add(me)
dead = False
laser_sound = pygame.mixer.Sound(os.path.join("sounds", "laser.ogg"))
player_dict = {}
player_dict[username] = pygame.sprite.GroupSingle(me)
wall_list = pygame.sprite.Group()

# TODO: add choice of maps here..
drawMap(wall_list)

ticks_per_second = 30

# -------- Main Program Loop -----------
while not done:
    me.firing = False
    keys=pygame.key.get_pressed()  
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL or event.key == pygame.K_SPACE):
            me.firing = True
        elif event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
    # get keys down

    """
    are we toucing a wall?
    TODO: functionalise
    """        
    me.walled = False
    hit_list = pygame.sprite.spritecollide(me, wall_list, False, pygame.sprite.collide_rect_ratio(1.1))
    if len(hit_list) > 0:
        for hit in hit_list:
            if hit.rect.bottom == me.rect.top or hit.rect.top == me.rect.bottom or hit.rect.left == me.rect.right or hit.rect.right == me.rect.left:
                if me.rect.left == hit.rect.right and me.rect.bottom > hit.rect.top and me.rect.top < hit.rect.bottom:
                    me.walled = True
                elif me.rect.right == hit.rect.left and me.rect.bottom > hit.rect.top and me.rect.top < hit.rect.bottom:
                    me.walled = True
                elif me.rect.top == hit.rect.bottom and me.rect.right > hit.rect.left and me.rect.left < hit.rect.right:
                    me.walled = True
                elif me.rect.bottom == hit.rect.top and me.rect.right > hit.rect.left and me.rect.left < hit.rect.right:
                    me.walled = True            
       



    if me.walled:
        # only listen to movement commands if we are touching a wall
        me.dir = getDir(keys)

    # which way does the keyboard say we should look?
    # if no aim commands recieved keep the old look_dir
    # TODO: use degrees!!!!!
    dir = getAimDir(keys)
    if dir != "still":
        me.aim_dir = dir


    # update all player positions
    player_list.update()

    # am I colliding with (intersecting with) a wall?
    # if so snap to the edge of the wall
    hit_list = pygame.sprite.spritecollide(me, wall_list, False)
    if len(hit_list) > 0:
        for hit in hit_list:
            if me.look_dir == "left":
                me.rect.x = hit.rect.right
            elif me.look_dir == "right":
                me.rect.x = hit.rect.left - 20
            elif me.look_dir == "up":
                me.rect.y = hit.rect.bottom
            elif me.look_dir == "down":
                me.rect.y = hit.rect.top - 20
            elif me.look_dir == "up-right":
                if me.rect.y >= hit.rect.bottom - 4:
                    me.rect.y = hit.rect.bottom
                else:
                    me.rect.x = hit.rect.left - 20
            elif me.look_dir == "up-left":
                if me.rect.y >= hit.rect.bottom - 4:
                    me.rect.y = hit.rect.bottom
                else:
                    me.rect.x = hit.rect.right
            elif me.look_dir == "down-right":
                if me.rect.y <= hit.rect.top - 16:
                    me.rect.y = hit.rect.top - 20
                else:
                    me.rect.x = hit.rect.left - 20
            elif me.look_dir == "down-left":
                if me.rect.y <= hit.rect.top - 16:
                    me.rect.y = hit.rect.top - 20
                else:
                    me.rect.x = hit.rect.right

    # shift bullets
    bullet_list.update()

    # move the darkness with light circle cutout so that the cicle's centre is on me
    dark.update(me.rect.x, me.rect.y, me.dead)


    # send me data to the server and get other client data
    data = getServerData(me, laser_sound)


    # did we here from the server? this should always be true (for now)
    if data:
        # if we have data from the server ...
        data = json.loads(data)

        # handle new players
        for peer in data.keys():
            # update our list of players with any new additions
            if not peer in player_dict.keys():
                # new player
                new_player=sprites.Player(data[peer]['x'], data[peer]['y'], peer)
                player_list.add(new_player)
                player_dict.update({peer: pygame.sprite.GroupSingle(new_player)})

        # process player actions and death
        for player in player_list:
            if player.name in data.keys():
                data_entry = data[player.name]
                if data_entry['a'] == 'dead':
                    player.dead = True
                else:
                    player.dead = False
                    if player.name != me.name:
                        player.rect.x = data_entry['x']
                        player.rect.y = data_entry['y']
                    if data[player.name]['s'] != 'none':
                        # player shoots
                        player.firing = True
                        if player.name !=  me.name:
                            laser_sound.play()
                        if data[player.name]['s'] == "up-left":
                            bullet_list.add(sprites.Bullet(data[player.name]['s'], data[player.name]['x'] + 10 - 10, data[player.name]['y'] + 10 - 10))
                        elif data[player.name]['s'] == "down-left":
                            bullet_list.add(sprites.Bullet(data[player.name]['s'], data[player.name]['x'] + 10 - 10, data[player.name]['y'] + 10 + 10))
                        elif data[player.name]['s'] == "up-right":
                            bullet_list.add(sprites.Bullet(data[player.name]['s'], data[player.name]['x'] + 10 + 10, data[player.name]['y'] + 10 - 10))
                        elif data[player.name]['s'] == "down-right":
                            bullet_list.add(sprites.Bullet(data[player.name]['s'], data[player.name]['x'] + 10 + 10, data[player.name]['y'] + 10 + 10))
                        else:
                            bullet_list.add(sprites.Bullet(data[player.name]['s'], data[player.name]['x'] + 10, data[player.name]['y'] + 10))

    # get number of living players
    living_count = 0
    for player in player_list:
        if not player.dead:
            living_count += 1

    if me.dead and living_count < 2:
        # respawn if I'm dead and less than two others are alive
        player_list.add(me)
        spawn(me)

    pygame.sprite.groupcollide(bullet_list, wall_list, True, False)

    # detect when I'm hit but don't remove the bullet
    hit_list = pygame.sprite.spritecollide(me, bullet_list, False)
    if len(hit_list) > 0:
        for hit in hit_list:
            # me was hit!
            me.dead = True
            bullet_list.remove(hit)

    # ^^^ Game logic should go above
    # vvv Drawing code should go below

    # at this point we expect
    """
    player_list to include all current players
    all entries in player_list to also be in player_dict in individual groups
    all player sprites must have a correct .dead attribute
    all player sprites must have correct .rect.x and y attributes
    all bullet sprites in bullet_list with correct .rect.x and y attributes
    """

    # clear the screen to white
    window.fill(colours.nonalpha.BLACK)
    screen.fill(colours.alpha.GREY)
                
    bullet_list.draw(screen)

    wall_list.draw(screen)
        
    # draw each player that isn't dead
    for player_group in player_dict.values():
        if not player_group.sprite.dead:
            player_group.draw(screen)
            screen.blit(font.render(player_group.sprite.name, 1, colours.alpha.BLACK), (player_group.sprite.rect.x - 6, player_group.sprite.rect.y - 15))

    for bullet in bullet_list:        
        # tidy up bullets that have left the screen
        pygame.draw.circle(dark.image, colours.alpha.TRANSPARENT, (bullet.rect.x + 6, bullet.rect.y + 6), 80)
        if bullet.rect.y < -10 or bullet.rect.x < -200:
            bullet_list.remove(bullet)
        if bullet.rect.y > 490 or bullet.rect.x > 900:
            bullet_list.remove(bullet)

    screen.blit(dark.image, (0, 0))
    
    window_origin = ((320 - (me.rect.x + 10) ), (240 - (me.rect.y + 10)))
    window.blit(screen, (window_origin))
    
    if me.gun_cooldown_timer <= 0:
        # print ready in top left corner when we can fire
        window.blit(font.render("Ready", 1, colours.alpha.DARK_GREEN), (10, 10))
    
    # update the screen
    pygame.display.flip()

    # 30 frames per second
    clock.tick(ticks_per_second)
    
pygame.quit()
