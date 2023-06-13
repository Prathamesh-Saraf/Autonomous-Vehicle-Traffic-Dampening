import pygame
import random
import math
import matplotlib.pyplot as plt
import csv

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define constants
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
TRACK_RADIUS = 300
NUM_AGENTS = 5
AGENT_RADIUS = 10
MAX_SPEED = 10
KP = 0.1 # Proportional gain
KI = 0.1

class Agent:
    def __init__(self):
        self.pos = random.uniform(0, 2*math.pi) # Initial position of agent on track
        self.speed = random.uniform(0, MAX_SPEED) # Initial speed of agent
        self.angle = self.pos # Initial angle of agent
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) # Random color for agent
        self.integral_error = 0 # Integral error for controller
        self.x = TRACK_RADIUS + TRACK_RADIUS * math.cos(self.angle) # X position of agent
        self.y = TRACK_RADIUS + TRACK_RADIUS * math.sin(self.angle) # Y position of agent

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

# Initialize the data for the position and velocity graphs
time_data = []
pos_data = [[] for _ in range(NUM_AGENTS)]
vel_data = [[] for _ in range(NUM_AGENTS)]

# Run the simulation
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calculate average speed of all agents
    total_speed = 0
    for agent in agents:
        total_speed += agent.speed
    avg_speed = total_speed / NUM_AGENTS
    
    # Update and draw the agents
    for i, agent in enumerate(agents):
        # Get the distances to the left and right neighbors
        left_dist = abs(agent.pos - agents[(i-1)%NUM_AGENTS].pos)
        right_dist = abs(agent.pos - agents[(i+1)%NUM_AGENTS].pos)

        # Calculate the error between the distances to the left and right neighbors
        dist_error = left_dist - right_dist
        
        # Proportional-Integral controller to adjust position based on the distance error
        agent.integral_error += dist_error
        agent.pos += KP * dist_error + KI * agent.integral_error
        
        # Proportional controller to adjust speed based on difference between current speed and target speed
        speed_error = avg_speed - agent.speed
        agent.speed += KP * speed_error
        
        # Update position based on speed and angle
        agent.angle += agent.speed/TRACK_RADIUS
        agent.x = TRACK_RADIUS + TRACK_RADIUS * math.cos(agent.angle)
        agent.y = TRACK_RADIUS + TRACK_RADIUS * math.sin(agent.angle)

        # Add the position and velocity data to the lists
        time_data.append(pygame.time.get_ticks() / 1000)
        pos_data[i].append(agent.pos)
        vel_data[i].append(agent.speed)
        
        # Draw the agent
        pygame.draw.circle(screen, agent.color, [int(agent.x), int(agent.y)], AGENT_RADIUS)
    
    # Draw the circular track
    pygame.draw.circle(screen, WHITE, track_center, TRACK_RADIUS, 2)
    
    # Update the screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()


# with open('agent_data.csv', mode='w', newline='') as agent_file:
#     agent_writer = csv.writer(agent_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     for i in range(len(vel_data)):
#         row = [i+1] + vel_data[i] + pos_data[i]
#         agent_writer.writerow(row)

# print("Data saved to agent_data.csv")

