import pygame
import random
import cairo
import numpy as np

# Initialize pygame
pygame.init()
pygame.mixer.init()

backsound = pygame.mixer.Sound("./backsound.mp3")

# Window dimensions
W_H = 500
W_W = 1000
win = pygame.display.set_mode((W_W, W_H))
pygame.display.set_caption("Dino Game with Gradient Effects")

KEWER_KEWER =[0, 0, 0 ]

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Constants
GROUND_HEIGHT = 100
DINO_WIDTH = 50
DINO_HEIGHT = 50


class Dino:
    def __init__(self):
        self.x = 50
        self.y = W_H - DINO_HEIGHT - GROUND_HEIGHT  # Adjust based on ground height
        self.vel = 10
        self.is_jumping = False
        self.jump_count = 10
        self.color_shift = 0  # Used to animate the gradient
        self.rect = pygame.Rect(self.x, self.y, DINO_WIDTH, DINO_HEIGHT)  # Create a rect for collision

    def draw(self, win):
        # Create a Cairo ImageSurface for Dino gradient
        data = np.zeros((DINO_HEIGHT, DINO_WIDTH, 4), dtype=np.uint8)  # Shape for ARGB
        cairo_surface = cairo.ImageSurface.create_for_data(data, cairo.FORMAT_ARGB32, DINO_WIDTH, DINO_HEIGHT)
        ctx = cairo.Context(cairo_surface)

        # Set up a radial gradient for Dino with looping color shift
        grad = cairo.RadialGradient(DINO_WIDTH / 2, DINO_HEIGHT / 2, 0, DINO_WIDTH / 2, DINO_HEIGHT / 2, DINO_WIDTH / 2)
        grad.add_color_stop_rgb(0, (self.color_shift % 255) / 255, 0.5, 1)
        grad.add_color_stop_rgb(1, 1, (self.color_shift % 255) / 255, 0.5)
        ctx.set_source(grad)
        ctx.rectangle(0, 0, DINO_WIDTH, DINO_HEIGHT)
        ctx.fill()

        # Increment color shift for continuous animation
        self.color_shift = (self.color_shift + 1) % 255

        # Convert Cairo surface to Pygame surface
        pygame_surface = pygame.image.frombuffer(data.tobytes(), (DINO_WIDTH, DINO_HEIGHT), 'ARGB')
        win.blit(pygame_surface, (self.x, self.y))  # Draw Dino at its position
        self.rect.topleft = (self.x, self.y)  # Update the rect position

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            self.is_jumping = False
            self.y = W_H - DINO_HEIGHT - GROUND_HEIGHT
            self.jump_count = 10
        
        if not self.is_jumping:
            if keys[pygame.K_SPACE]:  # Start jump on SPACE
                self.is_jumping = True
                for i in range(KEWER_KEWER.__len__()-1):
                    KEWER_KEWER[i] = random.randint(1,255)
        else:
            # Simulate jump by adjusting the y-coordinate
            if self.jump_count >= -10:
                neg = 1 if self.jump_count > 0 else -1
                self.y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = 10  # Reset jump

class Obstacle:
    def __init__(self):
        self.width = 20
        self.height = 20
        self.x = W_W
        self.y = W_H - self.height - GROUND_HEIGHT
        self.speed = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win):
        pygame.draw.rect(win, RED, self.rect)

    def move(self):
        self.x -= self.speed
        self.rect.x = self.x

def draw_ground(win):
    # Create an empty data buffer for the Cairo surface    
    data = np.zeros((GROUND_HEIGHT, W_W, 4), dtype=np.uint8)  # Shape for ARGB
    cairo_surface = cairo.ImageSurface.create_for_data(data, cairo.FORMAT_ARGB32, W_W, GROUND_HEIGHT)
    ctx = cairo.Context(cairo_surface)
    # Load the background image
    
    # Create a linear gradient for the ground with animated shift
    grad = cairo.LinearGradient(0, 0, 0, GROUND_HEIGHT)

    # Calculate the color shift based on time
    color_shift = (pygame.time.get_ticks() // 10) % 256  # Use 256 for smooth transitions

    # Define the gradient colors
    grad.add_color_stop_rgb(0, color_shift / 255.0, 0, 0.5)  # Vary red based on color_shift
    grad.add_color_stop_rgb(0.5, 0, color_shift / 255.0, 0)  # Vary green based on color_shift
    grad.add_color_stop_rgb(1, 0, 0.5, color_shift / 255.0)  # Vary blue based on color_shift

    # Set the gradient as the source and fill the rectangle
    ctx.set_source(grad)
    ctx.rectangle(0, 0, W_W, GROUND_HEIGHT)
    ctx.fill()

    # Convert Cairo surface to Pygame surface and blit to the window
    pygame_surface = pygame.image.frombuffer(data.tobytes(), (W_W, GROUND_HEIGHT), 'ARGB')
    win.blit(pygame_surface, (0, W_H - GROUND_HEIGHT))


def main():
    dino = Dino()
    obstacles = []
    score = 0
    font = pygame.font.Font("./gragon.otf", 42)
    font_bold = pygame.font.Font("./gragon.otf", 52)
    game_over = False
    played=False
    clock = pygame.time.Clock()
    
    while True:
        if not played:
            backsound.play(-1)
            played=True
        

        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Press R to reset the game
                    score = 0
                    obstacles.clear()
                    dino = Dino()  # Reset Dino
                    game_over = False
                    played=False

        if not game_over:
            # Handle Dino movements
            dino.handle_keys()

            # Spawn obstacles at intervals
            if random.randint(1, 100) < 2:
                obstacles.append(Obstacle())

            # Move obstacles and check for collisions
            for obstacle in obstacles[:]:
                obstacle.move()
                if obstacle.x < -obstacle.width:  # Remove off-screen obstacles
                    obstacles.remove(obstacle)
                    score += 1
                if dino.rect.colliderect(obstacle.rect):  # Check collision
                    game_over = True
                    backsound.stop()

        # Draw everything
        random.shuffle(obstacles)  # Shuffle to prevent flickering
        win.fill(WHITE)
        draw_ground(win)
        dino.draw(win)
        for obstacle in obstacles:
            obstacle.draw(win)

        # Display score
        score_text = font.render(f"Score: {score}", True, BLACK)
        win.blit(score_text, (10, 10))

        # Display game-over message
        if game_over:
            game_over_text = font_bold.render("Game Over! Press R to Restart", True, RED)
            win.blit(game_over_text, (W_W // 2 - game_over_text.get_width() // 2, W_H // 2 -50))

        pygame.display.update()

if __name__ == "__main__":
    main()
