import pygame
import random
import math

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define constants
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
TRACK_RADIUS = 300
NUM_AGENTS = 5
AGENT_RADIUS = 10
MAX_SPEED = 0.5

class Agent:
    def __init__(self):
        self.angle = random.uniform(0, 2*math.pi)
        self.speed = random.uniform(0.1, MAX_SPEED)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    def update(self):
        self.angle += self.speed/TRACK_RADIUS
        self.x = TRACK_RADIUS + TRACK_RADIUS * math.cos(self.angle)
        self.y = TRACK_RADIUS + TRACK_RADIUS * math.sin(self.angle)

# Initialize Pygame
pygame.init()

# Set the size of the screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Set the caption of the screen
pygame.display.set_caption('Circular Track Simulation')

# Set the font for the text on the screen
font = pygame.font.SysFont(None, 30)

# Create the circular track
track_center = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
pygame.draw.circle(screen, WHITE, track_center, TRACK_RADIUS, 2)

# Initialize the agents
agents = []
for i in range(NUM_AGENTS):
    agents.append(Agent())

# Run the simulation
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Clear the screen
    screen.fill(BLACK)
    
    # Update and draw the agents
    for agent in agents:
        agent.update()
        pygame.draw.circle(screen, agent.color, [int(agent.x), int(agent.y)], AGENT_RADIUS)
    
    # Draw the circular track
    pygame.draw.circle(screen, WHITE, track_center, TRACK_RADIUS, 2)
    
    # Update the screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()
