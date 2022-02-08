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

class RaycastingEngine:
    screen_width = 640
    screen_height = 480
    def __init__(self):
        self.color_ceiling = (135, 206, 235)
        self.color_walls = (203, 65, 84)
        self.color_floor = (127, 128, 118)
        self.color_screen= (49,150,100)
        self.color_shapes= (255,0,0)
        self.color_background = (220,220,220)
        self.map = Map()
        self.player = Player(100, 200)
        self.grid_pixels = self.screen_height / self.map.height
        self.casting_increment_angle = self.player.fov / self.screen_width
        self.casting_precision = 64
        self.player_movement_speed = self.player.speed * self.grid_pixels

    
    def draw_ray_casting(self, surface, lines_for_3d):
        for x in range(len(lines_for_3d)):
            pygame.draw.line(surface, lines_for_3d[x][2], lines_for_3d[x][1], lines_for_3d[x][0])
        
    def generate_ray_casting(self, player: Player):
        ray_angle = player.view_angle - player.fov / 2
        
        lines_for_3d = []
        for x in range(self.screen_width):
            ray_x = player.xpos
            ray_y = player.ypos
            ray_cos = math.cos(math.radians(ray_angle)) * 1.5
            ray_sin = math.sin(math.radians(ray_angle)) * 1.5
            hit_wall = False
            while not hit_wall:
                ray_x += ray_cos
                ray_y += ray_sin
                position = self.get_grid_position(math.floor(ray_x), math.floor(ray_y))
                hit_wall = self.map.grid[position[0]][position[1]] != 0

            distance = math.sqrt(math.pow(player.xpos - ray_x, 2) + math.pow(player.ypos - ray_y, 2)) 
            # fisheye fix
            distance = distance * math.cos(math.radians(ray_angle - player.view_angle))

            darkened_color_walls = self.shade_by_distance(self.color_walls, distance)
            wall_height = math.floor(((self.screen_height / 2) / distance) * self.grid_pixels)

            lines_for_3d.append([(x, 0), (x, (self.screen_height / 2) - wall_height), self.color_ceiling])
            lines_for_3d.append([(x, (self.screen_height / 2) - wall_height), (x, (self.screen_height / 2) + wall_height), darkened_color_walls])
            lines_for_3d.append([(x, (self.screen_height / 2) + wall_height), (x, self.screen_height), self.color_floor])
            ray_angle += player.fov / self.screen_width
        return lines_for_3d

    def shade_by_distance(self, color, distance):
        color_darkness = distance * .1
        color = list(color)
        # rgb has three values
        for x in range(3):
            if color[x] - color_darkness > 0:
                color[x] -= color_darkness
        return color

    def degree_to_radiens(self, angle_in_degrees):
        return angle_in_degrees * math.pi / 180

    def get_grid_position(self, x, y):
        return (int(y // self.grid_pixels), int(x // self.grid_pixels))
 
# define a main function
    def game_loop(self):
        pygame.init()
        pygame.display.set_caption("Ray Casting in 3D")
            
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        #draw_grid(screen)

        pygame.display.flip()


            
        # define a variable to control the main loop
        running = True
            
        # main loop
        while running:
            keys = pygame.key.get_pressed()
            pygame.draw.circle(screen, self.color_screen, (self.player.xpos, self.player.ypos), self.grid_pixels)
            if keys[pygame.K_LEFT]:
                new_grid_pos = self.get_grid_position(self.player.xpos -self.player_movement_speed, self.player.ypos)
                if self.map.grid[new_grid_pos[0]][new_grid_pos[1]] == 0:
                    self.player.xpos -= self.player_movement_speed
            elif keys[pygame.K_RIGHT]:
                new_grid_pos = self.get_grid_position(self.player.xpos + self.player_movement_speed, self.player.ypos)
                if self.map.grid[new_grid_pos[0]][new_grid_pos[1]] == 0:
                    self.player.xpos += self.player_movement_speed
            elif keys[pygame.K_UP]:
                new_grid_pos = self.get_grid_position(self.player.xpos, self.player.ypos + self.player_movement_speed)
                if self.map.grid[new_grid_pos[0]][new_grid_pos[1]] == 0:
                    self.player.ypos += self.player_movement_speed                
            elif keys[pygame.K_DOWN]:
                new_grid_pos = self.get_grid_position(self.player.xpos, self.player.ypos - self.player_movement_speed)
                if self.map.grid[new_grid_pos[0]][new_grid_pos[1]] == 0:
                    self.player.ypos -= self.player_movement_speed
            elif keys[pygame.K_a]:
                self.player.view_angle  -= self.player.rotate_speed
            elif keys[pygame.K_d]:
                self.player.view_angle  += self.player.rotate_speed
            elif keys[pygame.K_w]:
                new_x = self.player.xpos + math.cos(math.radians(self.player.view_angle)) * self.player_movement_speed
                new_y = self.player.ypos + math.sin(math.radians(self.player.view_angle)) * self.player_movement_speed
                new_grid_pos_x = self.get_grid_position(new_x, self.player.ypos)
                new_grid_pos_y = self.get_grid_position(new_x, self.player.ypos)
                if self.map.grid[new_grid_pos_x[0]][new_grid_pos_x[1]] == 0:
                    self.player.xpos = new_x
                if self.map.grid[new_grid_pos_y[0]][new_grid_pos_y[1]] == 0:
                    self.player.ypos = new_y
            elif keys[pygame.K_s]:
                new_x = self.player.xpos - math.cos(math.radians(self.player.view_angle)) * self.player_movement_speed
                new_y = self.player.ypos - math.sin(math.radians(self.player.view_angle)) * self.player_movement_speed
                if self.get_grid_position(new_x, self.player.ypos) == 0:
                    self.player.xpos = new_x
                if self.get_grid_position(self.player.xpos, new_y) == 0:
                    self.ypos = new_y

            lines_for_3d = self.generate_ray_casting(self.player)
            self.draw_ray_casting(screen, lines_for_3d)
            # draw_ray_casting_dda(player, screen)
            pygame.display.flip()

            for event in pygame.event.get():               
                if event.type == pygame.QUIT:
                    running = False


if __name__=="__main__":
    # call the main function
    engine = RaycastingEngine()
    engine.game_loop()