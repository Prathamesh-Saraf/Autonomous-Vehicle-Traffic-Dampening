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
MAX_SPEED = 0.1
GAIN_P = 0.1
GAIN_I = 0.01
SATURATION = 0.5

class Agent:
    def __init__(self, index, num_agents):
        self.index = index
        self.num_agents = num_agents
        self.angle = random.uniform(0, 2*math.pi)
        self.speed = random.uniform(0.1, MAX_SPEED)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    def update(self, agents):
        # Calculate the distance to the next and previous neighbors
        next_index = (self.index + 1) % self.num_agents
        prev_index = (self.index - 1) % self.num_agents
        next_dist = abs(self.angle - agents[next_index].angle)
        prev_dist = abs(self.angle - agents[prev_index].angle)
        
        # Calculate the desired speed based on the distance to the neighbors
        if next_dist < prev_dist:
            desired_speed = (next_dist / (2*math.pi/self.num_agents)) * MAX_SPEED
        else:
            desired_speed = (prev_dist / (2*math.pi/self.num_agents)) * MAX_SPEED
        
        # Calculate the error and integral error
        error = desired_speed - self.speed
        self.int_error = max(min(self.int_error + error, MAX_INTEGRAL), -MAX_INTEGRAL)
        
        # Calculate the control signal
        control_signal = GAIN_P * error + GAIN_I * self.int_error
        
        # Apply the control signal to adjust the speed
        self.speed += control_signal
        
        # Update the position
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
    agents.append(Agent(i, NUM_AGENTS))
    
# Set the target angle
target_angle = 2 * math.pi / NUM_AGENTS

# Run the simulation
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Clear the screen
    screen.fill(BLACK)
    
    # Update and draw the agents
    for i, agent in enumerate(agents):
        target = target_angle * i
        agent.update(target)
        pygame.draw.circle(screen, agent.color, [int(agent.x), int(agent.y)], AGENT_RADIUS)
    
    # Draw the circular track
    pygame.draw.circle(screen, WHITE, track_center, TRACK_RADIUS, 2)
    
    # Update the screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()
