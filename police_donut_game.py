import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 30
PLAYER_SPEED = 4
DONUT_SIZE = 20
DONUT_APPEAR_TIME = 5  # Seconds a donut stays on screen
DONUT_SPAWN_RATE = 3   # Seconds between donut spawns
MAX_MISSED_DONUTS = 3
WALL_COLOR = (34, 139, 34)  # Forest green for walls (grass-like)
CELL_SIZE = 40  # Size of each cell in the maze

# Colors
BACKGROUND_COLOR = (222, 184, 135)  # Light brown/tan background
PLAYER_COLOR = (0, 0, 255)          # Blue for police
DONUT_COLOR = (255, 51, 153)        # Strawberry pink for donut
TEXT_COLOR = (0, 0, 0)              # Black (changed for better visibility on light background)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Police Donut Chase")
clock = pygame.time.Clock()

# Load fonts
font = pygame.font.Font(None, 36)

# Define the maze layout (0 = path, 1 = wall)
# This creates a Pac-Man style maze
MAZE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
]

# Calculate wall rectangles for collision detection
wall_rects = []
for y, row in enumerate(MAZE):
    for x, cell in enumerate(row):
        if cell == 1:
            wall_rects.append(pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

class Player:
    def __init__(self):
        # Start at a valid position in the maze
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.score = 0
        self.find_valid_position()
    
    def find_valid_position(self):
        # Find a valid starting position (not in a wall)
        while True:
            x = random.randint(1, len(MAZE[0]) - 2)
            y = random.randint(1, len(MAZE) - 2)
            if MAZE[y][x] == 0:
                self.x = x * CELL_SIZE + (CELL_SIZE - self.size) // 2
                self.y = y * CELL_SIZE + (CELL_SIZE - self.size) // 2
                return
    
    def move(self, keys):
        # Store original position to revert if collision occurs
        original_x, original_y = self.x, self.y
        
        # Move based on key presses
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed
        
        # Create player rectangle for collision detection
        player_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        
        # Check for collisions with walls
        for wall_rect in wall_rects:
            if player_rect.colliderect(wall_rect):
                # Collision detected, revert to original position
                self.x, self.y = original_x, original_y
                break
        
        # Keep player within screen bounds
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.size))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.size))
    
    def draw(self):
        # Draw a simple police officer (blue circle with a badge)
        pygame.draw.circle(screen, PLAYER_COLOR, 
                          (self.x + self.size // 2, self.y + self.size // 2), 
                          self.size // 2)
        # Draw a simple badge (yellow circle)
        pygame.draw.circle(screen, (255, 255, 0), 
                          (self.x + self.size // 2, self.y + self.size // 3), 
                          self.size // 6)

class Donut:
    def __init__(self):
        self.size = DONUT_SIZE
        self.spawn()
    
    def spawn(self):
        # Find a valid position for the donut (not in a wall)
        while True:
            x = random.randint(0, len(MAZE[0]) - 1)
            y = random.randint(0, len(MAZE) - 1)
            if MAZE[y][x] == 0:
                self.x = x * CELL_SIZE + (CELL_SIZE - self.size) // 2
                self.y = y * CELL_SIZE + (CELL_SIZE - self.size) // 2
                break
        
        self.spawn_time = time.time()
        self.active = True
    
    def draw(self):
        if not self.active:
            return
            
        # Draw donut (circle with hole)
        pygame.draw.circle(screen, DONUT_COLOR, 
                          (self.x + self.size // 2, self.y + self.size // 2), 
                          self.size // 2)
        # Add white frosting details to make it more visible
        pygame.draw.circle(screen, (255, 255, 255), 
                          (self.x + self.size // 2, self.y + self.size // 2), 
                          self.size // 3, 2)
        # Donut hole
        pygame.draw.circle(screen, BACKGROUND_COLOR, 
                          (self.x + self.size // 2, self.y + self.size // 2), 
                          self.size // 5)
    
    def check_timeout(self):
        if time.time() - self.spawn_time > DONUT_APPEAR_TIME:
            self.active = False
            return True
        return False
    
    def check_collision(self, player):
        # Simple collision detection
        player_rect = pygame.Rect(player.x, player.y, player.size, player.size)
        donut_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        return player_rect.colliderect(donut_rect)

def draw_maze():
    for y, row in enumerate(MAZE):
        for x, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, WALL_COLOR, 
                               (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def reset_game():
    global player, donuts, missed_donuts, last_spawn_time, game_over
    player = Player()
    donuts = []
    missed_donuts = 0
    last_spawn_time = time.time()
    game_over = False

# Initialize game
player = Player()
donuts = []
missed_donuts = 0
last_spawn_time = time.time()
game_over = False

# Game loop
running = True
while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                reset_game()
    
    if not game_over:
        # Get keyboard input
        keys = pygame.key.get_pressed()
        player.move(keys)
        
        # Spawn new donuts
        current_time = time.time()
        if current_time - last_spawn_time > DONUT_SPAWN_RATE:
            donuts.append(Donut())
            last_spawn_time = current_time
        
        # Check donut timeouts and collisions
        for donut in donuts[:]:
            if donut.active:
                if donut.check_collision(player):
                    donut.active = False
                    player.score += 1
                elif donut.check_timeout():
                    missed_donuts += 1
            
        # Remove inactive donuts
        donuts = [donut for donut in donuts if donut.active]
        
        # Check game over condition
        if missed_donuts >= MAX_MISSED_DONUTS:
            game_over = True
    
    # Clear the screen
    screen.fill(BACKGROUND_COLOR)
    
    # Draw the maze
    draw_maze()
    
    # Draw player and donuts
    player.draw()
    for donut in donuts:
        donut.draw()
    
    # Draw the score and missed donuts
    score_text = font.render(f"Score: {player.score}", True, TEXT_COLOR)
    screen.blit(score_text, (10, 10))
    
    missed_text = font.render(f"Missed: {missed_donuts}/{MAX_MISSED_DONUTS}", True, TEXT_COLOR)
    screen.blit(missed_text, (10, 50))
    
    # Draw game over message
    if game_over:
        game_over_text = font.render("Game Over! Press R to restart", True, TEXT_COLOR)
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - 180, SCREEN_HEIGHT//2))
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
