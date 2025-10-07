# conda activate yt
import os
import json
import logging
from typing import Tuple, Union

from sjvisualizer import DataHandler, Canvas, BarRace, StaticImage, Date, StaticText, PieRace

def main(
    fps: int = 60, 
    duration: float = 0.5, 
    data_code: int = 5, 
    extra_decoration: bool = False,
    font_color: Tuple[int, int, int] = (150, 150, 150), 
    background: Tuple[int, int, int] = (255, 255, 255),
    color_file_name: str = "colors/colors.json",
    time_indicator: str = "year", 
    background_img: bool = False,
    background_img_name: str = "img/background.png",
    record: bool = True,
    file_name_video: str = "img/output.mp4",
    explosion_img_name: str = "img/explosion.png",
    logo_img_name: str = "img/logo.png"
) -> None:
    """
    Main function for visualizing data races/animations.
    """
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    # Validate data_code and get correct Excel/data file
    data_set = {
        1: ("data/Nuclear.xlsx", '', 0),
        2: ("data/Insta.xlsx", '', 0),
        3: ("data/GDP PPP Data.xlsx", '', 0),
        4: ("data/military budget.xlsx", ' $M', 150),
        5: ("data/DesktopOS.xlsx", ' $M', 150)
    }
    if data_code not in data_set:
        logging.error("Invalid data_code. Please use 1, 2, 3, 4, or 5.")
        return
    excel_file, unit, shift = data_set[data_code]

    number_of_frames = int(fps * duration * 60)

    # Load data
    try:
        df = DataHandler.DataHandler(excel_file=excel_file, number_of_frames=number_of_frames).df
    except Exception as e:
        logging.error(f"Could not load data from {excel_file}: {e}")
        return

    # Set up canvas
    canvas = Canvas.canvas(bg=background)
    width = int(canvas.canvas["width"])
    height = int(canvas.canvas["height"])

    # Load color configuration
    if not os.path.exists(color_file_name):
        os.makedirs(os.path.dirname(color_file_name), exist_ok=True)
        default_colors = {}
        with open(color_file_name, "w") as f:
            json.dump(default_colors, f)
    with open(color_file_name) as f:
        colors = json.load(f)

    # Add bar chart
    bar_chart = BarRace.bar_race(
        df=df, font_size=14, canvas=canvas.canvas, colors=colors,
        width=1350, height=650, x_pos=-150, y_pos=95, max_bars=9, number_of_bars=9, shift=shift,
        unit=unit, font_color=font_color
    )
    canvas.add_sub_plot(bar_chart)

    # Add time indication
    date = Date.date(
        canvas=canvas.canvas, font_color=font_color, font_size=25, height=100, width=100, 
        x_pos=1200, y_pos=670, time_indicator=time_indicator, df=df, number_of_bars=25
    )
    canvas.add_sub_plot(date)

    # Optional: Add background image
    if background_img and os.path.exists(background_img_name):
        static_img = StaticImage.static_image(
            canvas=canvas.canvas, x_pos=0, y_pos=0, height=1350,
            width=1350, file=background_img_name
        )
        canvas.add_sub_plot(static_img)

    # Context-based visualization
    if data_code == 1:
        canvas.add_title("Nuclear Warheads by Country", color=font_color)
        if extra_decoration:
            line = canvas.canvas.create_line(
                800 / 2, 40 / 2, 800 / 2, 150 / 2, width=10 / 2,
                fill=Canvas._from_rgb((75, 75, 155))
            )
            square = canvas.canvas.create_rectangle(10, 10, 1355, 760)
            if os.path.exists(explosion_img_name):
                ex = StaticImage.static_image(
                    canvas=canvas.canvas, file=explosion_img_name,
                    x_pos=650 / 2, y_pos=25 / 2, width=125 / 2, height=125 / 2
                )
                canvas.add_sub_plot(ex)
            canvas.add_sub_title("From 1950 - 2025", color=font_color)
            # canvas.add_logo(logo=logo_img_name) # Uncomment if implemented
    elif data_code == 2:
        canvas.add_title("Most Followed Instagram Accounts", color=font_color)
    elif data_code == 3:
        title = StaticText.static_text(
            canvas=canvas.canvas, text="GDP per Capita (PPP)",
            font_size=12, width=0, height=60,
            anchor="c", x_pos=600, y_pos=0,
            colors=font_color, font_color=font_color
        )
        canvas.add_sub_plot(title)
    elif data_code == 4:
        pie = PieRace.pie_plot(
            canvas=canvas.canvas, df=df, x_pos=650, y_pos=200, height=600, width=600,
            colors=colors, shift=shift, unit=unit, display_percentages=False,
            display_label=False, back_ground_color=background
        )
        canvas.add_sub_plot(pie)
        title = StaticText.static_text(
            canvas=canvas.canvas, text="Military Budget", width=0, height=65, anchor="c",
            x_pos=650, y_pos=0, font_color=font_color
        )
        canvas.add_sub_plot(title)
        subtitle = StaticText.static_text(
            canvas=canvas.canvas, text="Data Source : World Bank", colors=font_color,
            width=0, height=15, anchor="w", x_pos=447, y_pos=58, font_color=font_color
        )
        canvas.add_sub_plot(subtitle)

    # Save colors for future runs
    with open(color_file_name, "w") as file:
        json.dump(colors, file, indent=4)

    # Play and (optionally) record the animation
    try:
        canvas.play(fps=fps, file_name=file_name_video, record=record)
        logging.info(f"Video saved as {file_name_video}")
    except Exception as e:
        logging.error(f"Error during animation: {e}")

if __name__ == "__main__":
    main()
