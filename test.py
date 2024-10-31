import pygame
import cairo


pygame.init()
WIDTH, HEIGHT = 1000, 500
pygame.display.set_caption("Cairo with Pygame")
running = True
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)

class Draw:
    x,y = 0,0
    lebar,tinggi = 50,50
    kecepatan = 5
    derajat = 1
    def __init__(self, surface=surface):
        self.surface = surface
        self.ctx = cairo.Context(self.surface)
        
    def draw(self):
        self.ctx.set_source_rgb(1, 1, 1)
        self.ctx.paint()
        # Create a gradient
        self.ctx.save()
        
        gradient = cairo.LinearGradient(self.x, self.y, self.x + self.lebar, self.y + self.tinggi)
        gradient.add_color_stop_rgb(0, 1, 0, 0)  # Red at the start
        gradient.add_color_stop_rgb(1, 0, 0, 1)  # Blue at the end
        # Apply the gradient
        self.ctx.set_source(gradient)
        self.ctx.rectangle(self.x, self.y, self.lebar, self.tinggi)
        self.ctx.fill() 
        self.ctx.restore()

    
    def move(self , x, y):
        self.x += x
        if self.x > WIDTH - self.lebar:
            self.x = 0
        elif self.x < 0:
            self.x = WIDTH - self.lebar

        # Move vertically and wrap around
        self.y += y
        if self.y > HEIGHT - self.tinggi:
            self.y = 0
        elif self.y < 0:
            self.y = HEIGHT - self.tinggi
    
    def control(self,keys):
        if keys[pygame.K_LEFT]:
            self.move(-self.kecepatan,0)
        if keys[pygame.K_RIGHT]:
            self.move(self.kecepatan,0)
        if keys[pygame.K_UP]:
            self.move(0,-self.kecepatan)
        if keys[pygame.K_DOWN]:
            self.move(0,self.kecepatan)

gambar = Draw()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    gambar.draw()
    
    gambar.control(pygame.key.get_pressed())

    
    # Create PyGame surface from Cairo Surface
    buffer = surface.get_data()
    image = pygame.image.frombuffer(buffer, (WIDTH, HEIGHT), "ARGB")
    screen.blit(image, (0,0))
    # Refresh the display
    pygame.display.flip()
    clock.tick(60)  # Limit to 60 FPS

# Clean up
pygame.quit()
