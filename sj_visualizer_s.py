# Import the plotting module from sjvisualizer
from sjvisualizer import plot as plt

# Import the JSON module to handle JSON files
import json

# Open and read colors from a JSON file (if needed later)
with open('colors/colors.json') as f:
    colors = json.load(f)

# Create a pie chart visualization using data from an Excel file
plt.pie(
    excel="data/Nuclear.xlsx",             # Excel file containing input data
    title="Desktop Browser Market Share",  # Title of the chart
    sub_title="By Mr. Vivek Kumar",        # Subtitle of the chart
    unit="%",                              # Unit of measurement shown in chart
    duration=0.5,                          # Animation duration between frames
    output_video="img/output.mp4",         # Output file to save video animation
    record=False,                          # If True, saves chart as images
    fps=60,                                # Frames per second for animation/video
    time_indicator="year",                 # Time label (e.g., year, month)
    font_color=(255, 255, 255),            # Font color (RGB: White)
    background_color=(0, 0, 0),            # Background color (RGB: Black)

    # Custom colors assigned to different browsers
    colors={
        "Edge": (255, 0, 0),       # Red
        "Chrome": (0, 255, 0),     # Green
        "Safari": (0, 0, 255),     # Blue
        "Opera": (255, 255, 0),    # Yellow
        "Firefox": (255, 0, 255),  # Magenta
        "IE": (0, 255, 255),       # Cyan
        "Others": (255, 255, 255), # White
        "Netscape": (128, 128, 128), # Gray
        "Mosaic": (64, 64, 64)       # Dark Gray
    },

    sort=True  # Sort data automatically in the chart
)
