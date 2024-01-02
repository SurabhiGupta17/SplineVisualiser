import pygame
import sys
from bezier import bezier_point

pygame.init()
pygame_screen_width, pygame_screen_height = 800, 800
grid_size = 40  # Number of squares in each row and column
square_size = 600 // 30

# Dimensions for the radio button box
radio_box_width, radio_box_height = 120, 80
radio_box_x, radio_box_y = 10, 10

# Dimensions for the title box
title_box_width, title_box_height = 400, 40
title_box_x, title_box_y = 150, 10

# Dimensions for the grid area
grid_area_x, grid_area_y, grid_area_width, grid_area_height = 10, 100, 600, 600

pygame_screen = pygame.display.set_mode((pygame_screen_width, pygame_screen_height))
pygame.display.set_caption("Interactive Spline Visualizer")

control_points = []
obstacle_grid = []

# Current mode: 'c' for control point, 'o' for obstacle
current_mode = 'c'

# Colors for the radio buttons and grid cells
radio_button_color_default = (200, 200, 200)
radio_button_color_selected = (150, 150, 150)
grid_cell_color_obstacle = (128, 128, 128)

# Initialize a 2D array to represent the grid
grid = [[False for _ in range(grid_size)] for _ in range(grid_size)]

# Function to draw a round radio button
def draw_radio_button(label, x, y, selected=True):
    color = radio_button_color_selected if selected else radio_button_color_default
    pygame.draw.circle(pygame_screen, color, (x + 20, y + 20), 10)  # Radio button background
    font = pygame.font.Font(None, 20)
    text = font.render(label, True, (0, 0, 0))
    pygame_screen.blit(text, (x + 40, y + 15))

# Function to draw the grid
def draw_grid():
    # Draw the grid with borders
    for i in range(30):
        for j in range(grid_size-1):
            x = grid_area_x + j * square_size
            y = grid_area_y + i * square_size

            # Draw cell
            color = grid_cell_color_obstacle if grid[i][j] else (255, 255, 255)
            pygame.draw.rect(pygame_screen, color, (x, y, square_size, square_size))

            # Draw top border
            pygame.draw.line(pygame_screen, (180, 180, 180), (x, y), (x + square_size, y), 1)

            # Draw left border
            pygame.draw.line(pygame_screen, (180, 180, 180), (x, y), (x, y + square_size), 1)

            # Draw right border
            pygame.draw.line(pygame_screen, (180, 180, 180), (x + square_size, y), (x + square_size, y + square_size), 1)

            # Draw bottom border
            pygame.draw.line(pygame_screen, (180, 180, 180), (x, y + square_size), (x + square_size, y + square_size), 1)

# Pygame main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle mouse clicks in the Pygame window
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if (radio_box_x <= x <= radio_box_x + radio_box_width and
                radio_box_y <= y <= radio_box_y + radio_box_height):
                # Clicked on the radio button box
                if (radio_box_x + 10 <= x <= radio_box_x + 30 and
                    radio_box_y + 10 <= y <= radio_box_y + 30):
                    # Clicked on the "Control Point" radio button
                    current_mode = 'c'
                elif (radio_box_x + 10 <= x <= radio_box_x + 70 and
                      radio_box_y + 40 <= y <= radio_box_y + 60):
                    # Clicked on the "Obstacle" radio button
                    current_mode = 'o'
            elif (grid_area_x <= x <= grid_area_x + grid_area_width and
                  grid_area_y <= y <= grid_area_y + grid_area_height and
                  current_mode == 'c'):
                # Clicked within the grid area in "Control Point" mode
                # Add control point
                control_points.append((x, y))
            elif current_mode == 'o':
                # Toggle obstacle status for the clicked grid cell
                x, y = event.pos
                # Convert pixel coordinates to grid indices
                grid_x, grid_y = (x - grid_area_x) // square_size, (y - grid_area_y) // square_size
                # Toggle the square color
                grid[grid_y][grid_x] = not grid[grid_y][grid_x]

    # Update the Pygame window
    pygame_screen.fill((255, 255, 255))  # Fill with white background

    # Draw the title box
    pygame.draw.rect(pygame_screen, (200, 200, 200), (title_box_x, title_box_y, title_box_width, title_box_height))
    font = pygame.font.Font(None, 30)
    title_text = font.render("Spline Visualizer", True, (0, 0, 0))
    pygame_screen.blit(title_text, (title_box_x + 10, title_box_y + 5))

    # Draw the grid
    draw_grid()

    # Draw the radio buttons
    draw_radio_button("Control Point", radio_box_x + 10, radio_box_y + 10, current_mode == 'c')
    draw_radio_button("Obstacle", radio_box_x + 10, radio_box_y + 40, current_mode == 'o')

    # Draw the user-generated control points
    for point in control_points:
        pygame.draw.circle(pygame_screen, (0, 0, 0), point, 5)

    # Draw the Bézier curve using user-generated control points
    if len(control_points) > 1:
        num_points = 100
        bezier_points = [bezier_point(t / num_points, control_points) for t in range(num_points + 1)]
        pygame.draw.lines(pygame_screen, (0, 0, 255), False, bezier_points, 2)

    pygame.display.flip()

pygame.quit()
sys.exit()
