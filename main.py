import numpy as np

import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons, RadioButtons, Button
from bezier import de_casteljau
from cubic_spline import cubic_spline
from b_spline import b_spline
from catmullrom import catmull_rom_spline 

# Initialize an empty list for control points
control_points = []
obstacle_points = []

# Define fixed axis limits  
min_x, max_x = 0, 100
min_y, max_y = 0, 100

# Set up the figure and axes
fig, ax = plt.subplots()
fig.suptitle("Spline Visualiser")
ax.set_title("Spline Visualiser")
plt.subplots_adjust(bottom=0.1)
plt.subplots_adjust(top=0.8)

# Define the grid parameters
grid_size = 20  # Number of cells in each dimension
cell_width = (max_x - min_x) / grid_size
cell_height = (max_y - min_y) / grid_size

current_mode = 'Control Points'

# Function to handle mouse clicks on the plot
def on_plot_click(event):
    global current_mode
    if event.inaxes:
        x, y = event.xdata, event.ydata

        # Define the boundary for control points
        boundary_x_min, boundary_x_max = 0, 100
        boundary_y_min, boundary_y_max = 0, 100

        # Check if the mouse click is within the boundary
        if (
            boundary_x_min <= x <= boundary_x_max
            and boundary_y_min <= y <= boundary_y_max
            and event.inaxes != check.ax  # Exclude the checkbox region
        ):
            if current_mode == 'Control Points':
                control_points.append([x, y])
            elif current_mode == 'Obstacles':
                # Convert the clicked coordinates to grid indices
                grid_x = int((x - min_x) // cell_width)
                grid_y = int((y - min_y) // cell_height)
                obstacle_points.append((grid_x, grid_y))

            update_plot()

# Function to handle checkbox events
def on_checkbox_clicked(label):
    update_plot()

# Function to handle reset button click
def on_reset_button_clicked(event):
    global control_points, obstacle_points
    control_points = []
    obstacle_points = []
    update_plot()

# Function to update the plot
def update_plot():
    ax.cla()

    # Plot grid lines
    for i in range(1, grid_size):
        ax.axvline(i * cell_width, color='lightgray', linestyle='-', linewidth=0.5)
        ax.axhline(i * cell_height, color='lightgray', linestyle='-', linewidth=0.5)

    # Plot the obstacles
    for obstacle_point in obstacle_points:
        grid_x, grid_y = obstacle_point
        obstacle_x = min_x + grid_x * cell_width
        obstacle_y = min_y + grid_y * cell_height
        obstacle_rect = plt.Rectangle((obstacle_x, obstacle_y), cell_width, cell_height, color='lightgray')
        ax.add_patch(obstacle_rect)

    # Disconnect the mouse click event to avoid multiple connections
    #fig.canvas.mpl_disconnect(fig.canvas.manager.key_press_handler_id)

    # Plot the curves
    if len(control_points) > 1:
        control_points_array = np.array(control_points)

        # Plot Bézier curve if 'Bezier' checkbox is checked
        if check.get_status()[0]:
            t_vals = np.linspace(0, 1, 1000)
            bezier_spline = np.array([de_casteljau(t, control_points_array) for t in t_vals]).T
            ax.plot(bezier_spline[0], bezier_spline[1], label="Bézier Curve", color='blue')

        # Plot Cubic Spline curve if 'Cubic-Spline' checkbox is checked
        if check.get_status()[1]:
            cubic_spline_points = cubic_spline(control_points_array, 1000)
            ax.plot(cubic_spline_points[0], cubic_spline_points[1], label="Cubic-Spline", color='black')

        # Plot Catmull-Rom spline if 'Catmull Rom' checkbox is checked
        if check.get_status()[2] and len(control_points) >= 4:
            catmull_rom_spline_points = catmull_rom_spline(control_points_array, 1000)
            ax.plot(catmull_rom_spline_points[0], catmull_rom_spline_points[1], label="Catmull Rom", color='green')

        # Plot B-spline if 'B-spline' checkbox is checked
        if check.get_status()[3] and len(control_points) >= 3: 
            b_spline_points = b_spline(control_points_array, 2, 1000)  
            ax.plot(b_spline_points[:, 0], b_spline_points[:, 1], label="B-spline", color='orange')

    # Plot the control points
    if control_points:
        points = np.array(control_points)
        ax.scatter(points[:, 0], points[:, 1], c='red', marker='o', label="Control Points")

    # Set fixed axis limits
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)

    # Set labels and legend
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.legend(loc = 'upper right', fontsize='7')

    # Show the plot
    plt.draw()

# Connect the mouse click event
fig.canvas.mpl_connect('button_press_event', on_plot_click)

# Set up checkboxes
rax = plt.axes([0.125, 0.82, 0.15, 0.15])   
check = CheckButtons(rax, ['Bezier', 'Cubic-Spline', 'Catmull Rom', 'B-Spline'], (True, False, True, False))
check.on_clicked(on_checkbox_clicked)  

for rect, label in zip(check.rectangles, check.labels):
    rect.set_width(0.1)
    rect.set_height(0.2)
    rect.set_edgecolor('black') 
    label.set_fontsize(7) 

# Set up radio buttons for modes
modes = ['Control Points', 'Obstacles']
mode_selector_ax = plt.axes([0.7, 0.82, 0.2, 0.15])
mode_selector = RadioButtons(mode_selector_ax, modes, activecolor='black')

# Customize the appearance of the radio buttons
for circles, label in zip(mode_selector.circles, mode_selector.labels):
    circles.set_radius(0.08)
    circles.set_width(0.08)
    circles.set_edgecolor('black')  
    label.set_fontsize(9)

# Function to update the current mode
def update_mode(label):
    global current_mode
    current_mode = label

# Connect the mode selector event
mode_selector_ax.set_box_aspect(0.5)
mode_selector.on_clicked(update_mode)

# Create a reset button
reset_button_ax = plt.axes([0.92, 0.01, 0.066, 0.04])  # Adjust the position and size as needed
reset_button = Button(reset_button_ax, 'Reset', color='lightgray', hovercolor='gray')
reset_button.on_clicked(on_reset_button_clicked)

# Show the initial plot
update_plot()

plt.show()