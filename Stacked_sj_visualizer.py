from sjvisualizer import Canvas, DataHandler, BarRace, PieRace, Date, StackedBarChart, StaticImage
import json
import os
import logging
from typing import Optional

def main(fps: int = 60, duration: float = 0.35) -> None:
    """
    Displays a stacked bar chart visualization with time progression for Desktop OS market share.
    
    Args:
        fps (int): Frames per second for the animation.
        duration (float): Duration (in minutes) for the visualization timeline.
    """
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    colors_path = 'colors/colors.json'

    # Load colors
    if not os.path.exists(colors_path):
        logging.warning(f"Colors JSON file not found at {colors_path}. Creating a default empty file.")
        os.makedirs(os.path.dirname(colors_path), exist_ok=True)
        with open(colors_path, 'w') as f:
            json.dump({}, f)

    with open(colors_path) as f:
        colors = json.load(f)

    number_of_frames = int(duration * 60 * fps)
    try:
        df = DataHandler.DataHandler(excel_file="data/DesktopOS.xlsx", number_of_frames=number_of_frames).df
    except Exception as e:
        logging.error(f"Failed to load data: {e}")
        return

    canvas = Canvas.canvas()
    width = int(canvas.canvas["width"])
    height = int(canvas.canvas["height"])

    # Add stacked bar chart
    stacked = StackedBarChart.stacked_bar_chart(
        canvas=canvas.canvas,
        df=df,
        title="Stacked",
        font_size=14,
        font_color=(150, 150, 150),
        colors=colors,
        height=height - 150,
        width=width - 400,
        x_pos=50,
        y_pos=100
    )
    canvas.add_sub_plot(stacked)

    # Add time indicator
    date_display = Date.date(
        canvas=canvas.canvas,
        height=int(height / 20),
        width=int(width / 20),
        x_pos=int(height / 0.62),
        y_pos=int(width / 40),
        time_indicator="month",
        df=df,
        number_of_bars=25
    )
    canvas.add_sub_plot(date_display)

    # Save colors for next run
    with open(colors_path, "w") as file:
        json.dump(colors, file, indent=4)

    # Play animation
    try:
        canvas.play(fps=fps)
        logging.info("Visualization played successfully.")
    except Exception as e:
        logging.error(f"Error during animation: {e}")

if __name__ == "__main__":
    main()
