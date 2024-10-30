import pygame
import cairo
import math

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Infinite Gradient Animation")

# Create a Cairo surface
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
context = cairo.Context(surface)

# Function to draw gradient
def draw_gradient(t):
    # Clear the surface
    context.set_source_rgba(0, 0, 0, 0)  # Clear with transparent
    context.paint()
    
    # Create a linear gradient
    gradient = cairo.LinearGradient(0, 0, 0, HEIGHT)
    
    # Modify the gradient colors based on time `t`
    r1 = (0.5 + 0.5 * math.sin(t)) % 1.0
    g1 = (0.5 + 0.5 * math.sin(t + 2)) % 1.0
    b1 = (0.5 + 0.5 * math.sin(t + 4)) % 1.0
    
    r2 = (0.5 + 0.5 * math.sin(t + 6)) % 1.0
    g2 = (0.5 + 0.5 * math.sin(t + 8)) % 1.0
    b2 = (0.5 + 0.5 * math.sin(t + 10)) % 1.0
    
    gradient.add_color_stop_rgb(0, r1, g1, b1)
    gradient.add_color_stop_rgb(1, r2, g2, b2)

    # Fill the context with the gradient
    context.set_source(gradient)
    context.rectangle(0, 0, WIDTH, HEIGHT)
    context.fill()

# Main loop
running = True
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks() / 1000.0  # Get the starting time

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calculate time elapsed
    current_time = pygame.time.get_ticks() / 1000.0
    elapsed_time = current_time - start_time

    # Draw gradient
    draw_gradient(elapsed_time)

    # Update the Pygame screen with the Cairo surface
    pygame_surface = pygame.image.frombuffer(surface.get_data(), (WIDTH, HEIGHT), 'ARGB')
    screen.blit(pygame_surface, (0, 0))
    
    # Refresh the display
    pygame.display.flip()
    clock.tick(60)  # Limit to 60 FPS

# Clean up
pygame.quit()
