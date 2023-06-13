import pygame
import random
import math
import matplotlib.pyplot as plt

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
TRACK_RADIUS = 300
NUM_AGENTS = 5
AGENT_RADIUS = 5
MAX_SPEED = 0.5
KP = 0.01 
KI = 0.0001

class Agent:
    def __init__(self):
        self.integral_error = 0
        self.angle = random.uniform(0, 2*math.pi)
        self.speed = random.uniform(0.1, MAX_SPEED)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.speed_history = [self.speed]  # List to store history of speeds
        # self.position_history = [self.speed]  # List to store history of positions

    def update(self, target_speed):
        # Proportional controller to adjust speed based on difference between current speed and target speed
        speed_error = target_speed - self.speed
        self.speed += KP * speed_error

        # Integral controller to adjust speed based on accumulated error over time
        self.integral_error += speed_error
        self.speed += KI * self.integral_error

        # Update position based on speed and angle
        self.angle += self.speed/TRACK_RADIUS
        self.x = TRACK_RADIUS + TRACK_RADIUS * math.cos(self.angle)
        self.y = TRACK_RADIUS + TRACK_RADIUS * math.sin(self.angle)

        # Store current speed in history
        self.speed_history.append(self.speed)
        # self.position_history.append(self.angle)

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

    # Calculate average speed of all agents
    total_speed = 0
    for agent in agents:
        total_speed += agent.speed
    avg_speed = total_speed / NUM_AGENTS
    
    # Update and draw the agents
    for agent in agents:
        agent.update(avg_speed)
        pygame.draw.circle(screen, agent.color, [int(agent.x), int(agent.y)], AGENT_RADIUS)
    
    pygame.draw.circle(screen, WHITE, track_center, TRACK_RADIUS, 2)
    
    pygame.display.flip()

# Quit Pygame
pygame.quit()

# Plot velocity graph for each agent over time
for i, agent in enumerate(agents):
    plt.plot(agent.speed_history, label=f"Agent {i+1}")
plt.xlabel("Time")
plt.ylabel("Velocity")
plt.legend()
plt.show()

# for i, agent in enumerate(agents):
#     plt.plot(agent.position_history, label=f"Agent {i+1}")
# plt.xlabel("Time")
# plt.ylabel("Position")
# plt.legend()
# plt.show()