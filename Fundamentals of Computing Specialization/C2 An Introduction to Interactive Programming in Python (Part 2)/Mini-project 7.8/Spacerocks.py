## An Introduction to Interactive Programming in Python (Part 2)
## Mini-project 7/8: Spaceship/RiceRocks
## Spacerocks.py

## Required packages:
## pygame - http://www.pygame.org/download.shtml
## SimpleGUICS2Pygame - https://simpleguics2pygame.readthedocs.org/

## Module was initially intended to be run with CodeSkulptor http://www.codeskulptor.org/#examples-spaceship_template.py
## In order to run on local Phython instance, call to import module 'simplegui' has been modified.

# program template for Spaceship

# import simplegui
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            center = (self.image_center[0]+self.image_size[0], self.image_center[1])
            canvas.draw_image(self.image, center, self.image_size, self.pos, self.image_size, self.angle)        
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.vel[0] *= 0.98
        self.vel[1] *= 0.98
        forward = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += forward[0] * 0.55
            self.vel[1] += forward[1] * 0.55

    def change_angle_vel(self, ori, key_state):
        if ((ori == "right" and key_state == "keyup") or
            (ori == "left" and key_state == "keydown")):
            self.angle_vel -= 0.1
        elif ((ori == "right" and key_state == "keydown") or
            (ori == "left" and key_state == "keyup")):
            self.angle_vel += 0.1

    def set_thruster(self, thruster_state):
        self.thrust = thruster_state
        if self.thrust:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()    
        else:
            ship_thrust_sound.rewind()

    def shoot(self):
        global missile_group
        offset = self.image_size[0] / 2.0
        forward = angle_to_vector(self.angle)
        pos = [self.pos[0] + offset * forward[0], self.pos[1] + offset * forward[1]]
        vel = [self.vel[0] + 8 * forward[0], self.vel[1] + 8 * forward[1]]
        ang = 0
        ang_vel = 0
        missile_group.add(Sprite(pos, vel, ang, ang_vel, missile_image, missile_info, missile_sound))

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            center = (self.image_center[0] + self.age * self.image_size[0], self.image_center[1])
            canvas.draw_image(self.image, center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        if started:
            self.angle += self.angle_vel
            self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
            self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
            self.age += 1
            if self.age >= self.lifespan:
                return True
            else:
                return False

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def collide(self, other_object):
        dis = self.get_radius() + other_object.get_radius()
        if dis > dist(self.get_position(), other_object.get_position()):
            return True
        else:
            return False

def group_collide(group, other_object):
    is_collide = False
    remove_set = set([])
    for obj in group:
        if obj.collide(other_object):
            is_collide = True
            remove_set.add(obj)
            pos = [other_object.pos[0], other_object.pos[1]]
            new_explosion = Sprite(pos, [0, 0], other_object.angle, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(new_explosion)

    group.difference_update(remove_set)
    return is_collide

def group_group_collide(group, other_group):
    num_collide = 0
    for obj in list(group):
        if group_collide(other_group, obj):
            group.discard(obj)
            num_collide += 1
    return num_collide

def process_sprite_group(sprite_group, canvas):
    remove_set = set([])
    for sprite in sprite_group:
        sprite.draw(canvas)
        if sprite.update():
            remove_set.add(sprite)
    sprite_group.difference_update(remove_set)

def draw(canvas):
    global time, lives, rock_group, missile_group, ship, score, started
    
    # animiate background
    time += 1
    wtime = (time / 8) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))    
    
    # draw ship and sprites
    ship.draw(canvas)
    ship.update()
    canvas.draw_text("Lives: " + str(lives), [(WIDTH / 20), HEIGHT / 15], 30, "White")
    canvas.draw_text("Score: " + str(score), [(WIDTH / 20) * 15, HEIGHT / 15], 30, "White")
    
    if started:
        process_sprite_group(rock_group, canvas)
        process_sprite_group(missile_group, canvas)
        process_sprite_group(explosion_group, canvas)
        if group_collide(rock_group, ship):
            lives -= 1
        if lives <= 0:
            init_game()
        score += group_group_collide(rock_group, missile_group) * 10
    else:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), (WIDTH / 2, HEIGHT / 2), splash_info.get_size()) 

# timer handler that spawns a rock
def rock_spawner():
    global rock_group, canvas
    if started and len(rock_group) < 9:  # max rock count
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        pos = [x, y]
        if dist(pos, ship.get_position()) > 150:
            vx = random.randrange(1, 3, 1) * random.choice([1, -1])
            vy = random.randrange(1, 3, 1) * random.choice([1, -1])
            vel = [vx, vy]
            ang = 0
            ang_vel = random.randrange(5, 10, 1) / 100.0 * random.choice([1, -1])
            a_rock = Sprite(pos, vel, ang, ang_vel, asteroid_image, asteroid_info)
            rock_group.add(a_rock)

def key_up(key):
    if started:
        if simplegui.KEY_MAP['left'] == key:
            ship.change_angle_vel("left", "keyup")
        elif simplegui.KEY_MAP['right'] == key:
            ship.change_angle_vel("right", "keyup")
        elif simplegui.KEY_MAP['up'] == key:
            ship.set_thruster(False)

def key_down(key):
    if started:
        if simplegui.KEY_MAP['left'] == key:
            ship.change_angle_vel("left", "keydown")
        elif simplegui.KEY_MAP['right'] == key:
            ship.change_angle_vel("right", "keydown")
        elif simplegui.KEY_MAP['up'] == key:
            ship.set_thruster(True)
        elif simplegui.KEY_MAP['space'] == key:
            ship.shoot()
 
def mouse_click(position):
    global started
    if position[0] < WIDTH and position[1] < HEIGHT and not started :
        started = True
        soundtrack.rewind()
        soundtrack.play()

def init_game():
    global ship, rock_group, missile_group, explosion_group, started, score, lives
    ship = Ship([WIDTH / 2, HEIGHT / 3], [0, 0], 1.5 * math.pi, ship_image, ship_info)
    rock_group = set([])
    missile_group = set([])
    explosion_group = set([])
    score, lives = 0, 3  # set no. of starting lives
    started = False
    soundtrack.rewind()
    ship_thrust_sound.rewind()
    missile_sound.rewind()
    explosion_sound.rewind()

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

init_game()

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(mouse_click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
