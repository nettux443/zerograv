#!/usr/bin/python

import pygame
import nethelpers
import sprites
import json
import random
import os

from math import atan2, degrees, pi, sin, cos

# colours
BLACK    = (   0,   0,   0)
GREY     = ( 192, 192, 192)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
CYAN     = (   0, 255, 255)
GREEN    = (   0, 255,   0)
DARK_GREEN  = (   0, 192,   0)
RED      = ( 255,   0,   0)
PURPLE   = ( 128,   0, 128)
PINK     = ( 255,   0, 255)
ORANGE   = ( 255, 165,   0)
YELLOW   = ( 255, 255,   0)
TRANSPARENT = (0,0,0,0)

def colourize(colour_string):
    if colour == "yellow":
        return  YELLOW
    elif colour == "blue":
        return  BLUE
    elif colour == "cyan":
        return  CYAN  
    elif colour == "red":
        return  RED
    elif colour == "orange":
        return  ORANGE
    elif colour == "pink":
        return  PINK
    elif colour == "green":
        return  GREEN
    return False

def getPlayerByName(player_list, name):
    for player in player_list:
        if player.name == name:
            return player
    return False

def vectDegs(x1,y1,x2,y2):
    dx = x2 - x1
    dy = y2 - y1
    rads = atan2(-dy,dx)
    rads %= 2*pi
    degs = degrees(rads)
    return int(round(degs))

def vectorStep(x0, y0, degs):
    theta = pi/6
    r = 1.0
    deltax = r*cos(theta)
    deltay = r*sin(theta)
    x1 = x0 + deltax
    y1 = y0 + deltay
    return {"x": x1, "y": y1}

def getDir(keys):
    dir = "still"
    if keys[pygame.K_LEFT]:
        dir = "left"
    if keys[pygame.K_RIGHT]:
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

def getAimDir(keys):
    dir = "still"
    if keys[pygame.K_a]:
        dir = "left"
    if keys[pygame.K_d]:
        if dir == "left":
            dir = "still"
        else:
            dir = "right"
    if keys[pygame.K_w]:
        if dir == "left":
            dir = "up-left"
        elif dir == "right":
            dir = "up-right"
        else:
            dir = "up"

    if keys[pygame.K_s]:
        if dir == "left":
            dir = "down-left"
        elif dir == "right":
            dir = "down-right"
        elif dir == "up":
            dir = "still"
        else:
            dir = "down"
    return dir

def getServerData(me, keys, fire, laser_sound):
    if me.dead:
        data = server.sendToServer({"x": 0, "y": 0, "shooting": "none", "token": token, "username": username, "action": "dead", "data": "none"})
    elif fire:

        if not me.fired and me.gun_cooldown_timer <= 0:
            me.gun_cooldown_timer = me.gun_cooldown
            me.firing = True
            me.fired = True
            laser_sound.play()
            if not me.walled:
                if me.aim_dir == "left":
                    me.dir = "right"
                elif me.aim_dir == "right":
                    me.dir = "left"
                elif me.aim_dir == "up":
                    me.dir = "down"
                elif me.aim_dir == "down":
                    me.dir = "up"
                elif me.aim_dir == "down-left":
                    me.dir = "up-right"
                elif me.aim_dir == "down-right":
                    me.dir = "up-left"
                elif me.aim_dir == "up-left":
                    me.dir = "down-right"
                elif me.aim_dir == "up-right":
                    me.dir = "down-left"

                    
            data = server.sendToServer({"x": me.rect.x, "y": me.rect.y, "shooting": me.aim_dir, "token": token, "username": username, "action": "none", "data": "none"})
        else:
            data = server.sendToServer({"x": me.rect.x, "y": me.rect.y, "shooting": "none", "token": token, "username": username, "action": "none", "data": "none"})
    else:
        me.fired = False
        data = server.sendToServer({"x": me.rect.x, "y": me.rect.y, "shooting": "none", "token": token, "username": username, "action": "none", "data": "none"})
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


def spawn(player):
    ran = random.random()
    player.dead = False
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
        
server_ip = raw_input("Server IP/hostname? ")
server_port = raw_input("Server port? ")

server = nethelpers.server(server_ip, server_port)

username = raw_input("Username? ")

while True:
    colour = raw_input("Colour? ")
    colour = colour.strip().lower()
    player_colour = colourize(colour)
    if player_colour != False:
        break
    print "Choose: yellow, orange, pink, blue, red, cyan or green."
    
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.mixer.init()
font=pygame.font.Font(None,18)
# Set the width and height of the screen [width, height]
size = (640, 480)
window = pygame.display.set_mode(size)

screen = pygame.Surface(size)

pygame.display.set_caption("0Game")

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
player_names = []
player_names.append(username)
dead = False
laser_sound = pygame.mixer.Sound(os.path.join("sounds", "laser.ogg"))
player_dict = {}
player_dict[username] = pygame.sprite.GroupSingle(me)
wall_list = pygame.sprite.Group()


drawMap(wall_list)




ticks_per_second = 30

gun_cooldown_timer = 0
gun_cooldown = 3 * ticks_per_second

# -------- Main Program Loop -----------
while not done:
    fire = False
    if gun_cooldown_timer > 0:
        gun_cooldown_timer -= 1        
    keys=pygame.key.get_pressed()  
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL or event.key == pygame.K_SPACE):
            fire = True
        elif event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
    # get keys down
        
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
        me.dir = getDir(keys)

    dir = getAimDir(keys)
    if dir != "still":
        me.aim_dir = dir

    player_list.update()
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
        



                    
    bullet_list.update()

    dark.update(me.rect.x, me.rect.y, me.dead)

        
        

    me.firing = False

    # send me data to the server and get other client data
    data = getServerData(me, keys, fire, laser_sound)

    if data != "{}":
        # if we have data from the server ...
        data = json.loads(data)

        # handle new players
        for peer in data.keys():
            # update our list of players with any new additions
            if not peer in player_names:
                """ new player!!! """
                player_names.append(peer)
                new_player=sprites.Player(data[peer]['x'], data[peer]['y'], peer)
                player_list.add(new_player)
                player_dict.update({peer: pygame.sprite.GroupSingle(new_player)})

        # process player position and death
        for player in player_list:
            if player.name in data.keys():
                data_entry = data[player.name]
                if data_entry['action'] == 'dead':
                    player.dead = True
                else:
                    player.dead = False
                    if player.name != me.name:
                        player.rect.x = data_entry['x']
                        player.rect.y = data_entry['y']
                    
                    

        # proccess player shooting
        for player in player_list:
            if data[player.name]['shooting'] != 'none':
                player.firing = True
                if player.name !=  me.name:
                    laser_sound.play()
                if data[player.name]['shooting'] == "up-left":
                    bullet_list.add(sprites.Bullet(data[player.name]['shooting'], data[player.name]['x'] + 10 - 10, data[player.name]['y'] + 10 - 10))
                elif data[player.name]['shooting'] == "down-left":
                    bullet_list.add(sprites.Bullet(data[player.name]['shooting'], data[player.name]['x'] + 10 - 10, data[player.name]['y'] + 10 + 10))
                elif data[player.name]['shooting'] == "up-right":
                    bullet_list.add(sprites.Bullet(data[player.name]['shooting'], data[player.name]['x'] + 10 + 10, data[player.name]['y'] + 10 - 10))
                elif data[player.name]['shooting'] == "down-right":
                    bullet_list.add(sprites.Bullet(data[player.name]['shooting'], data[player.name]['x'] + 10 + 10, data[player.name]['y'] + 10 + 10))
                else:
                    bullet_list.add(sprites.Bullet(data[player.name]['shooting'], data[player.name]['x'] + 10, data[player.name]['y'] + 10))



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

    hit_list = pygame.sprite.spritecollide(me, bullet_list, True)
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
    window.fill(BLACK)
    screen.fill(GREY)
                
    bullet_list.draw(screen)

    wall_list.draw(screen)

        
    # draw each player that isn't dead
    for player_group in player_dict.values():
        if not player_group.sprite.dead:
            player_group.draw(screen)
            screen.blit(font.render(player_group.sprite.name, 1,BLACK), (player_group.sprite.rect.x - 6, player_group.sprite.rect.y - 15))

    for bullet in bullet_list:        
        # tidy up bullets that have left the screen
        pygame.draw.circle(dark.image, TRANSPARENT, (bullet.rect.x + 6, bullet.rect.y + 6), 80)
        if bullet.rect.y < -10 or bullet.rect.x < -200:
            bullet_list.remove(bullet)
        if bullet.rect.y > 490 or bullet.rect.x > 900:
            bullet_list.remove(bullet)

    screen.blit(dark.image, (0, 0))
    window_origin = ((320 - (me.rect.x + 10) ), (240 - (me.rect.y + 10)))
    window.blit(screen, (window_origin))
    # update the screen
    pygame.display.flip()

    # 30 frames per second
    clock.tick(ticks_per_second)
    
pygame.quit()
