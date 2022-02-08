from hashlib import new
from mimetypes import init
from operator import mul
from re import X
import pygame
import math

class Map:
    def __init__(self):
        self.width = 32
        self.height = 24
        self.grid = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]


class Player:
    def __init__(self, x, y):
        self.fov = 60
        self.xpos = x 
        self.ypos = y
        self.view_angle = 45
        self.speed = .25
        self.rotate_speed = 5


# import the pygame module, so you can use it
color_ceiling = (135, 206, 235)
color_walls = (203, 65, 84)
color_floor = (127, 128, 118)

color_screen=(49,150,100)
color_shapes=(255,0,0)
color_background=(220,220,220)
color_lines=(0,0,0)
player = Player(100, 100)
map = Map()
screen_width = 640
screen_height = 480
grid_pixels = screen_height / map.height
casting_increment_angle = player.fov / screen_width
casting_precision = 64
player_movement_speed = player.speed * grid_pixels



def draw_ray_casting(surface, lines_for_3d):
    for x in range(len(lines_for_3d)):
        pygame.draw.line(surface, lines_for_3d[x][2], lines_for_3d[x][1], lines_for_3d[x][0])

def generate_ray_casting(player: Player):
    ray_angle = player.view_angle - player.fov / 2
    
    lines_for_3d = []
    for x in range(screen_width):
        ray_x = player.xpos
        ray_y = player.ypos
        ray_cos = math.cos(math.radians(ray_angle)) * 2
        ray_sin = math.sin(math.radians(ray_angle)) * 2
        hit_wall = False
        while not hit_wall:
            ray_x += ray_cos
            ray_y += ray_sin
            position = get_grid_position(math.floor(ray_x), math.floor(ray_y))
            hit_wall = map.grid[position[0]][position[1]] != 0

        distance = math.sqrt(math.pow(player.xpos - ray_x, 2) + math.pow(player.ypos - ray_y, 2)) 
        # fisheye fix
        distance = distance * math.cos(math.radians(ray_angle - player.view_angle))

        darkened_color_walls = shade_by_distance(color_walls, distance)
        wall_height = math.floor(((screen_height / 2) / distance) * grid_pixels)

        lines_for_3d.append([(x, 0), (x, (screen_height / 2) - wall_height), color_ceiling])
        lines_for_3d.append([(x, (screen_height / 2) - wall_height), (x, (screen_height / 2) + wall_height), darkened_color_walls])
        lines_for_3d.append([(x, (screen_height / 2) + wall_height), (x, screen_height), color_floor])
        ray_angle += player.fov / screen_width
    return lines_for_3d

def shade_by_distance(color, distance):
    color_darkness = distance * .1
    color = list(color)
    # rgb has three values
    for x in range(3):
        if color[x] - color_darkness > 0:
            color[x] -= color_darkness
    return color

def draw_ray_casting_dda(player: Player, surface):
    ray_angle = player.view_angle - player.fov / 2
    for x in range(10):
        continue
        #get negative inverse of tangent
        #find x and y where ray will hit closest horizontal line
            #if angle greater than 180:
                # ray y is player y //round to nearest 64. 
                # ray x is (player y - ray y ) * atan + px
    return

def degree_to_radiens(angle_in_degrees):
    return angle_in_degrees * math.pi / 180

def get_grid_position(x, y):
    return (int(y // grid_pixels), int(x // grid_pixels))

def draw_grid(screen):
    screen.fill(color_screen)
    pygame.draw.circle(screen, color_shapes, (player.xpos, player.ypos), grid_pixels / 2)
    for col in range(len(map.grid[0])):
        for row in range(len(map.grid)):
            if map.grid[row][col] == 1:
                pygame.draw.rect(screen, color_shapes, (col * grid_pixels, row * grid_pixels, grid_pixels - 1, grid_pixels - 1))
            else:
                pygame.draw.rect(screen, color_background, (col * grid_pixels, row * grid_pixels, grid_pixels - 1, grid_pixels - 1))

 
# define a main function
def main():
     
    pygame.init()
    pygame.display.set_caption("Ray Casting in 3D")
     
    screen = pygame.display.set_mode((screen_width, screen_height))
    #draw_grid(screen)

    pygame.display.flip()


     
    # define a variable to control the main loop
    running = True
     
    # main loop
    while running:
        keys = pygame.key.get_pressed()
        pygame.draw.circle(screen, color_screen, (player.xpos, player.ypos), grid_pixels)
        if keys[pygame.K_LEFT]:
            new_grid_pos = get_grid_position(player.xpos -player_movement_speed, player.ypos)
            if map.grid[new_grid_pos[0]][new_grid_pos[1]] == 0:
                player.xpos -= player_movement_speed
        elif keys[pygame.K_RIGHT]:
            new_grid_pos = get_grid_position(player.xpos + player_movement_speed, player.ypos)
            if map.grid[new_grid_pos[0]][new_grid_pos[1]] == 0:
                player.xpos += player_movement_speed
        elif keys[pygame.K_UP]:
            new_grid_pos = get_grid_position(player.xpos, player.ypos + player_movement_speed)
            if map.grid[new_grid_pos[0]][new_grid_pos[1]] == 0:
                player.ypos += player_movement_speed                
        elif keys[pygame.K_DOWN]:
            new_grid_pos = get_grid_position(player.xpos, player.ypos - player_movement_speed)
            if map.grid[new_grid_pos[0]][new_grid_pos[1]] == 0:
                player.ypos -= player_movement_speed
        elif keys[pygame.K_a]:
            player.view_angle  -= player.rotate_speed
        elif keys[pygame.K_d]:
            player.view_angle  += player.rotate_speed
        elif keys[pygame.K_w]:
            new_x = player.xpos + math.cos(math.radians(player.view_angle)) * player_movement_speed
            new_y = player.ypos + math.sin(math.radians(player.view_angle)) * player_movement_speed
            new_grid_pos_x = get_grid_position(new_x, player.ypos)
            new_grid_pos_y = get_grid_position(new_x, player.ypos)
            if map.grid[new_grid_pos_x[0]][new_grid_pos_x[1]] == 0:
                player.xpos = new_x
            if map.grid[new_grid_pos_y[0]][new_grid_pos_y[1]] == 0:
                player.ypos = new_y
        elif keys[pygame.K_s]:
            new_x = player.xpos - math.cos(math.radians(player.view_angle)) * player_movement_speed
            new_y = player.ypos - math.sin(math.radians(player.view_angle)) * player_movement_speed
            if get_grid_position(new_x, player.ypos) == 0:
                player.xpos = new_x
            if get_grid_position(player.xpos, new_y) == 0:
                player.ypos = new_y

        lines_for_3d = generate_ray_casting(player)
        draw_ray_casting(screen, lines_for_3d)
        # draw_ray_casting_dda(player, screen)
        pygame.display.flip()

        for event in pygame.event.get():               
            if event.type == pygame.QUIT:
                running = False
            #draw_grid(screen)
            #pygame.draw.circle(screen, color_shapes, (player.xpos, player.ypos), grid_pixels / 2)
        


if __name__=="__main__":
    # call the main function
    main()