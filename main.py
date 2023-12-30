import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
from bezier import de_casteljau
from b_spline import b_spline
from catmullrom import catmull_rom_spline 

# Initialize an empty list for control points
control_points = []

# Define fixed axis limits  
min_x, max_x = -10, 10
min_y, max_y = -10, 10

# Set up the figure and axes
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)

# Function to handle mouse clicks on the plot
def on_plot_click(event):
    if event.inaxes:
        x, y = event.xdata, event.ydata
        control_points.append([x, y])
        update_plot()

# Function to handle checkbox events
def on_checkbox_clicked(label):
    update_plot()

# Function to update the plot
def update_plot():
    ax.cla()

    # Disconnect the mouse click event to avoid multiple connections
    fig.canvas.mpl_disconnect(fig.canvas.manager.key_press_handler_id)

    # Plot the curves
    if len(control_points) > 1:
        control_points_array = np.array(control_points)

        # Plot Bézier curve if 'Bezier' checkbox is checked
        if check.get_status()[0]:
            t_vals = np.linspace(0, 1, 1000)
            bezier_spline = np.array([de_casteljau(t, control_points_array) for t in t_vals]).T
            ax.plot(bezier_spline[0], bezier_spline[1], label="Bézier Curve", color='blue')

        # Plot B-spline if 'B-spline' checkbox is checked
        if check.get_status()[2] and len(control_points) >= 3:  # Assuming you add a third checkbox for B-spline
            b_spline_points = b_spline(control_points_array, 1000, 2)  # Assuming quadratic B-spline (degree=2)
            ax.plot(b_spline_points[0], b_spline_points[1], label="B-spline", color='orange')

        # Plot Catmull-Rom spline if 'Catmull Rom' checkbox is checked
        if check.get_status()[1] and len(control_points) >= 4:
            catmull_rom_spline_points = catmull_rom_spline(control_points_array, 1000)
            ax.plot(catmull_rom_spline_points[0], catmull_rom_spline_points[1], label="Catmull Rom", color='green')

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
    ax.legend()

    # Show the plot
    plt.draw()

# Connect the mouse click event
fig.canvas.mpl_connect('button_press_event', on_plot_click)

# Set up checkboxes
rax = plt.axes([0.125, 0.83, 0.15, 0.15])   
check = CheckButtons(rax, ['Bezier', 'Catmull Rom', 'B-Spline'], (True, True, True))
check.on_clicked(on_checkbox_clicked)  # Connect the checkbox event

# Define a color sequence for rectangles
colors = ['blue', 'green', 'orange']

# Set face color for each rectangle using the color sequence
[rect.set_facecolor(colors[i]) for i, rect in enumerate(check.rectangles)]

for rect, label in zip(check.rectangles, check.labels):
    rect.set_width(0.1)  # Increase the width of the checkbox
    rect.set_height(0.2)  # Increase the height of the checkbox
    rect.set_edgecolor('black')  # Set the border color
    label.set_fontsize(7)  # Set the font size

# Show the initial plot
update_plot()

plt.show()
