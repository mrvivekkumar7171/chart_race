# conda activate yt
from sjvisualizer import DataHandler, Canvas, BarRace, StaticImage, Date, StaticText, PieRace, StackedBarChart
import json


def main(
        fps = 60, 
        duration = 0.5, 
        data_code=5, 
        extra_decoration=False,
        font_color=(150,150,150), 
        background=(255,255,255), # (0,0,0) black and (255,255,255) white and (150,150,150) and (100,100,100)
        color_file_name = "colors/colors.json",
        time_indicator="year", # month, day, year
        background_img=False,
        background_img_name="img/background.png",
        record=True,
        file_name_video="img/output.mp4",
        explosion_img_name = "img/explosion.png",
        logo_img_name = "img/logo.png"
    ):

    # duration = 0.5 (for 720p using the commented settings for all the elements below) and duration = 0.15 (for 1440p using the commented settings for all the elements below)

    if data_code == 1:
        excel_file = "data/Nuclear.xlsx"
        unit = ''
        shift = 0
    elif data_code == 2:
        excel_file = "data/Insta.xlsx"
        unit = ''
        shift = 0
    elif data_code == 3:
        excel_file = "data/GDP PPP Data.xlsx"
        unit = ''
        shift = 0
    elif data_code == 4:
        excel_file = "data/military budget.xlsx"
        unit = " $M"
        shift = 150
    elif data_code == 5:
        excel_file = "data/DesktopOS.xlsx"
        unit = " $M"
        shift = 150
    else:
        raise ValueError("Invalid data_code. Please use 1, 2, 3, or 4.")
    
    number_of_frames = fps*duration*60
    df = DataHandler.DataHandler(excel_file=excel_file, number_of_frames=number_of_frames).df # data load
    canvas = Canvas.canvas(bg=background) # creating the canvas
    width = int(canvas.canvas["width"])
    height = int(canvas.canvas["height"])
    with open(color_file_name) as f: # load colors
        colors = json.load(f)

    # adding bar chart
    # width=2200/2, height=1000/2, x_pos=100/2 (720p) and width=2200, height=1000, x_pos=100 (1440p)
    bar_chart = BarRace.bar_race(
        df=df,
        font_size=14,
        canvas=canvas.canvas,
        colors=colors,
        width=1350,
        height=650,
        x_pos=-150,
        y_pos=95,
        max_bars=9,
        number_of_bars=9,
        shift=shift, # ??????
        unit=unit, 
        font_color=font_color
        ) 
    canvas.add_sub_plot(bar_chart)

    # add time indication # canvas.add_time(df=df, time_indicator="year")
    date = Date.date(
        canvas=canvas.canvas,
        font_color=font_color,
        font_size=25,
        height=100,
        width=100, 
        x_pos=1200, 
        y_pos=670,
        time_indicator=time_indicator,
        df=df, 
        number_of_bars=25
    )
    canvas.add_sub_plot(date)

    if background_img:
        static_img = StaticImage.static_image(
            canvas=canvas.canvas, 
            x_pos=0, 
            y_pos=0, 
            height=1350,
            width=1350,
            file=background_img_name
        )
        canvas.add_sub_plot(static_img)

    # adding a title
    if data_code == 1:
        canvas.add_title("Nuclear Warheads by Country", color=font_color)

        if extra_decoration:
            # adding decoration with TkInter
            # 800/2, 40/2, 800/2, 150/2, width=10/2 (720p)
            # 800, 40, 800, 150, width=10 (1440p)
            line = canvas.canvas.create_line(800/2, 40/2, 800/2, 150/2, width=10/2, fill=Canvas._from_rgb((75, 75, 155)))

            square = canvas.canvas.create_rectangle(10, 10, 1355, 760)

            # adding a static image
            # x_pos = 650/2, y_pos=25/2, width=125/2, height=125/2 (for 720p)
            # x_pos = 650, y_pos=25, width=125, height=125 (for 1440p)
            ex = StaticImage.static_image(
                    canvas=canvas.canvas, 
                    file=explosion_img_name, 
                    x_pos = 650/2, 
                    y_pos=25/2, 
                    width=125/2, 
                    height=125/2
                ) 
            canvas.add_sub_plot(ex)

            canvas.add_sub_title("From 1950 - 2025", color=font_color)

            # adding a logo
            # canvas.add_logo(logo=logo_img_name)
    elif data_code == 2:
        # add title using static text
        canvas.add_title("Most Followed Instagram Accounts", color=font_color)
    elif data_code == 3:
        title = StaticText.static_text(
            canvas=canvas.canvas,
            text="GDP per Capita (PPP)",
            font_size=12,
            width=0,
            height=60,
            anchor="c",
            x_pos=600,
            y_pos=0,
            colors=font_color,
            font_color=font_color
        )
        canvas.add_sub_plot(title)
    elif data_code == 4:
        # add pie chart
        pie = PieRace.pie_plot(
            canvas=canvas.canvas, 
            df=df, 
            x_pos=650, 
            y_pos=200, 
            height=600,
            width=600, 
            colors=colors, 
            shift=shift, 
            unit=unit, 
            display_percentages=False, 
            display_label=False, 
            back_ground_color=background
        )
        canvas.add_sub_plot(pie)

        title = StaticText.static_text(
            canvas=canvas.canvas, 
            text="Military Budget", 
            width=0, 
            height=65, 
            anchor="c",
            x_pos=650, 
            y_pos=0,
            font_color=font_color
        )
        canvas.add_sub_plot(title)

        title = StaticText.static_text(
            canvas=canvas.canvas, 
            text="Data Source : World Bank", 
            colors=font_color,
            width=0,
            height=15,
            anchor="w",
            x_pos=447,
            y_pos=58,
            font_color=font_color
        )
        canvas.add_sub_plot(title)

    # save colors for next run
    with open(color_file_name, "w") as file:
        json.dump(colors, file, indent=4)

    # play the animation
    canvas.play(fps=fps, file_name=file_name_video, record=record)

if __name__ == "__main__":
    main()