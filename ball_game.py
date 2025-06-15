import pygame
import sys
import random
import math
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
PADDLE_SPEED = 8
BALL_RADIUS = 10
BALL_SPEED = 5
SPEED_INCREASE_RATE = 0.05  # How much to increase speed per second
BACKGROUND_COLOR = (0, 0, 0)  # Black
PADDLE_COLOR = (0, 0, 139)    # Dark Blue
BALL_COLOR = (255, 255, 255)  # White
TEXT_COLOR = (255, 0, 0)      # Red
GRASS_LIGHT = (76, 187, 23)   # Light green
GRASS_DARK = (56, 142, 17)    # Dark green

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ball Bounce Game")
clock = pygame.time.Clock()

# Create grass pattern background
def draw_grass_background():
    # Draw alternating stripes of grass
    stripe_width = 30
    for y in range(0, SCREEN_HEIGHT, stripe_width):
        for x in range(0, SCREEN_WIDTH, stripe_width):
            color = GRASS_LIGHT if (x // stripe_width + y // stripe_width) % 2 == 0 else GRASS_DARK
            pygame.draw.rect(screen, color, (x, y, stripe_width, stripe_width))

# Paddle position
paddle_x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2
paddle_y = SCREEN_HEIGHT - PADDLE_HEIGHT - 10

# Ball position and velocity
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
# Random initial direction
angle = random.uniform(math.pi/4, 3*math.pi/4)  # Start with downward angle
ball_dx = BALL_SPEED * math.cos(angle)
ball_dy = BALL_SPEED * math.sin(angle)

# Speed variables
current_ball_speed = BALL_SPEED
start_time = time.time()

# Game state
score = 0
game_over = False
font = pygame.font.Font(None, 36)

def reset_game():
    global paddle_x, paddle_y, ball_x, ball_y, ball_dx, ball_dy, score, game_over, current_ball_speed, start_time
    paddle_x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2
    paddle_y = SCREEN_HEIGHT - PADDLE_HEIGHT - 10
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 2
    angle = random.uniform(math.pi/4, 3*math.pi/4)
    current_ball_speed = BALL_SPEED
    ball_dx = current_ball_speed * math.cos(angle)
    ball_dy = current_ball_speed * math.sin(angle)
    score = 0
    game_over = False
    start_time = time.time()

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
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] and paddle_x < SCREEN_WIDTH - PADDLE_WIDTH:
            paddle_x += PADDLE_SPEED
        
        # Increase ball speed over time
        elapsed_time = time.time() - start_time
        speed_multiplier = 1 + (elapsed_time * SPEED_INCREASE_RATE)
        current_speed = min(BALL_SPEED * speed_multiplier, BALL_SPEED * 3)  # Cap at 3x initial speed
        
        # Normalize the direction vector and apply current speed
        speed_ratio = current_speed / math.sqrt(ball_dx**2 + ball_dy**2)
        ball_dx *= speed_ratio
        ball_dy *= speed_ratio
        
        # Update ball position
        ball_x += ball_dx
        ball_y += ball_dy
        
        # Ball collision with walls
        if ball_x <= BALL_RADIUS or ball_x >= SCREEN_WIDTH - BALL_RADIUS:
            ball_dx = -ball_dx
        if ball_y <= BALL_RADIUS:
            ball_dy = -ball_dy
        
        # Ball collision with paddle
        if (ball_y + BALL_RADIUS >= paddle_y and 
            ball_x >= paddle_x and ball_x <= paddle_x + PADDLE_WIDTH):
            # Calculate bounce angle based on where the ball hits the paddle
            # Middle of paddle gives straight bounce, edges give angled bounce
            relative_intersect_x = (paddle_x + (PADDLE_WIDTH / 2)) - ball_x
            normalized_intersect_x = relative_intersect_x / (PADDLE_WIDTH / 2)
            bounce_angle = normalized_intersect_x * (math.pi / 3)  # Max 60 degree bounce
            
            # Update ball direction and slightly increase speed
            normalized_speed = math.sqrt(ball_dx**2 + ball_dy**2)
            ball_dx = -normalized_speed * math.sin(bounce_angle)
            ball_dy = -normalized_speed * math.cos(bounce_angle)
            
            # Ensure the ball is moving upward after bounce
            if ball_dy > 0:
                ball_dy = -ball_dy
                
            # Increase score
            score += 1
        
        # Check if ball is out of bounds (game over)
        if ball_y >= SCREEN_HEIGHT:
            game_over = True
    
    # Clear the screen
    screen.fill(BACKGROUND_COLOR)
    
    # Draw grass background
    draw_grass_background()
    
    # Draw the paddle
    pygame.draw.rect(screen, PADDLE_COLOR, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    
    # Draw the ball
    pygame.draw.circle(screen, BALL_COLOR, (int(ball_x), int(ball_y)), BALL_RADIUS)
    
    # Draw the score
    score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(score_text, (10, 10))
    
    # Draw current speed
    if not game_over:
        elapsed_time = time.time() - start_time
        speed_multiplier = 1 + (elapsed_time * SPEED_INCREASE_RATE)
        speed_text = font.render(f"Speed: {speed_multiplier:.2f}x", True, TEXT_COLOR)
        screen.blit(speed_text, (10, 50))
    
    # Draw game over message
    if game_over:
        game_over_text = font.render("Game Over! Press R to restart", True, TEXT_COLOR)
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2))
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
