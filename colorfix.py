import pygame
import cairo
import sys
import numpy as np

class PygameCairoApp:
    def __init__(self, screen_width=500, screen_height=500):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = self.init_pygame()
        self.surface, self.data, self.context = self.create_surfaces()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)


    def init_pygame(self):
        pygame.init()
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

    def draw_rect(self):
        self.context.rectangle(50, 50, 100, 100)
        self.context.set_source_rgb(1, 0, 0)
        self.context.fill()
        self.update_surface()

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
            self.render_fps()
            pygame.display.flip()
            self.clock.tick(60)
            
            if any(event.type == pygame.QUIT for event in pygame.event.get()):
                break

    def run(self):
        self.main_loop()
        self.quit_pygame()

if __name__ == "__main__":
    app = PygameCairoApp()
    app.run()