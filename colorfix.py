from re import S
from turtle import width
import pygame
import cairo
import sys
import numpy as np

RED = (0.1, 0.1, 1)
BLUE = (1, 0.1, 0.1)
GREEN = (0.1, 1, 0.1)

LAVENDER = (181 / 255, 110 / 255, 231 / 255)
YELLOW = (253 / 255, 197 / 255, 0 / 255)
BRIGHT_YELLOW = (255 / 255, 241 / 255, 0 / 255)

PURPLE = (0.5, 0.1, 0.7)
ORANGE = (0.9, 0.6, 0.1)
CYAN = (0.1, 0.7, 0.7)

class PygameCairo:
    def __init__(self, screen_width=500, screen_height=500):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = self.init_pygame()
        self.surface, self.data, self.context = self.create_surfaces()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        self.char = {'x': 50, 'y': 50,'width':100,'height':100,'speed': 5,'shift': 0}
        
    def init_pygame(self):
        pygame.init()
        pygame.display.set_caption('Pygame Cairo Fana')
        return pygame.display.set_mode((self.screen_width, self.screen_height))

    def create_surfaces(self):
        surface = pygame.Surface((self.screen_width, self.screen_height))
        data = np.zeros((self.screen_height, self.screen_width, 4), dtype=np.uint8)
        cairo_surface = cairo.ImageSurface.create_for_data(data, cairo.FORMAT_ARGB32, self.screen_width, self.screen_height)
        context = cairo.Context(cairo_surface)
        return surface, data, context

    def update_surface(self):
        pygame.surfarray.blit_array(self.surface, self.data[:, :, :3].swapaxes(0, 1))

    def render_fps(self):
        fps = self.clock.get_fps()
        fps_text = self.font.render(f'FPS: {int(fps)}', True, (0, 0, 0))
        self.screen.blit(fps_text, (5, 5))

    def linear_gradient(self,a,b,c):
        x,y,width,height = self.char['x'], self.char['y'], self.char['width'], self.char['height']
        shift = x-self.char['shift']
        grad = cairo.LinearGradient(shift,height/2 ,shift +width*4,height/2 )
        colors = [a[::-1], b[::-1], c[::-1]]  # Define RED, BLUE, GREEN as your RGB values
        for n in range(6):
            grad.add_color_stop_rgb(n / 6, *colors[n % 3])
        grad.add_color_stop_rgb(1, *a[::-1])  # Add the final stop at position 1 with RED
        return grad
    
    def draw_rect(self):
        x,y,width,height = self.char['x'], self.char['y'], self.char['width'], self.char['height']
        
        grad = self.linear_gradient(RED,GREEN,BLUE)
        self.context.rectangle(x, y, width, height)
        grad2 = self.linear_gradient(LAVENDER,YELLOW,BRIGHT_YELLOW)
        
        self.context.set_source(grad)
        self.context.fill()
        
        self.context.set_line_width(10)
        self.context.set_source(grad2)
        self.context.rectangle(x, y,width,height)
        self.context.stroke()
        
        self.update_surface()
        
        self.char['shift'] = (self.char['shift'] + 1) % (width*2)  # Use modulo for seamless looping

        
    def handle_controls(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.char['x'] -= self.char['speed']
        if keys[pygame.K_RIGHT]:
            self.char['x'] += self.char['speed']
        if keys[pygame.K_UP]:
            self.char['y'] -= self.char['speed']
        if keys[pygame.K_DOWN]:
            self.char['y'] += self.char['speed']

    def quit_pygame(self):
        try:
            pygame.quit()
            sys.exit()
        except SystemExit:
            pass

    def main_loop(self):
        while True:
            self.context.set_source_rgb(1, 1, 1)
            self.context.paint()
            
            self.draw_rect()
            
            self.screen.blit(self.surface, (0, 0))
            self.handle_controls()
            self.render_fps()
            pygame.display.flip()
            self.clock.tick(60)
            if any(event.type == pygame.QUIT for event in pygame.event.get()):
                break

    def run(self):
        self.main_loop()
        self.quit_pygame()

if __name__ == "__main__":
    app = PygameCairo()
    app.run()