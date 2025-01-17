import pygame
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 10
BALL_COLOR = (255, 0, 0)
HOLE_RADIUS = 15
HOLE_COLOR = (0, 0, 255)
BACKGROUND_COLOR = (200, 200, 200)
WALL_COLOR = (0, 0, 0)
FPS = 60

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Maze Puzzle with Goal")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Maze walls
walls = [
    pygame.Rect(100, 100, 600, 20),
    pygame.Rect(100, 180, 20, 300),
    pygame.Rect(200, 260, 400, 20),
    pygame.Rect(680, 100, 20, 300),
    pygame.Rect(300, 400, 300, 20),
    pygame.Rect(300, 160, 20, 240),
    pygame.Rect(480, 300, 20, 120),
    pygame.Rect(580, 160, 20, 180),
]

# Ball initial position and velocity
ball_x, ball_y = 120, 120
velocity_x, velocity_y = 0.0, 0.0
acceleration = 0.5
friction = 0.98
velocity_threshold = 0.1

# Goal hole location
hole_x, hole_y = 700, 500
goal_reached = False  # Win condition

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key states
    keys = pygame.key.get_pressed()
    # Control ball movement
    if keys[pygame.K_UP]:
        velocity_y -= acceleration
    if keys[pygame.K_DOWN]:
        velocity_y += acceleration
    if keys[pygame.K_LEFT]:
        velocity_x -= acceleration
    if keys[pygame.K_RIGHT]:
        velocity_x += acceleration

    # Apply friction to slow the ball down naturally
    velocity_x *= friction
    velocity_y *= friction

    # Stop the ball if velocity is very small (threshold)
    if abs(velocity_x) < velocity_threshold:
        velocity_x = 0
    if abs(velocity_y) < velocity_threshold:
        velocity_y = 0

    # Update ball position
    ball_x += velocity_x
    ball_y += velocity_y

    # Keep ball within screen bounds
    ball_x = max(BALL_RADIUS, min(WIDTH - BALL_RADIUS, ball_x))
    ball_y = max(BALL_RADIUS, min(HEIGHT - BALL_RADIUS, ball_y))

    # Collision detection with walls
    ball_rect = pygame.Rect(
        ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2
    )
    for wall in walls:
        if ball_rect.colliderect(wall):
            # Collision response: push ball back
            if abs(wall.top - ball_rect.bottom) < 10 and velocity_y > 0:
                velocity_y = -abs(velocity_y) * 0.5
            if abs(wall.bottom - ball_rect.top) < 10 and velocity_y < 0:
                velocity_y = abs(velocity_y) * 0.5
            if abs(wall.left - ball_rect.right) < 10 and velocity_x > 0:
                velocity_x = -abs(velocity_x) * 0.5
            if abs(wall.right - ball_rect.left) < 10 and velocity_x < 0:
                velocity_x = abs(velocity_x) * 0.5

    # Check if ball reaches the hole
    distance_to_hole = math.sqrt((ball_x - hole_x) ** 2 + (ball_y - hole_y) ** 2)
    if distance_to_hole < HOLE_RADIUS:
        goal_reached = True
        running = False  # Exit the game loop

    # Drawing
    screen.fill(BACKGROUND_COLOR)
    for wall in walls:
        pygame.draw.rect(screen, WALL_COLOR, wall)
    pygame.draw.circle(screen, BALL_COLOR, (int(ball_x), int(ball_y)), BALL_RADIUS)
    pygame.draw.circle(screen, HOLE_COLOR, (hole_x, hole_y), HOLE_RADIUS)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Win message
if goal_reached:
    screen.fill((0, 255, 0))
    font = pygame.font.Font(None, 74)
    text = font.render("You Win!", True, (0, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

# Quit Pygame
pygame.quit()