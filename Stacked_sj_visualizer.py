from sjvisualizer import Canvas, DataHandler, BarRace, PieRace, Date, StackedBarChart, StaticImage
import json

def main(fps = 60, duration = 0.35):

    # load colors
    with open('colors/colors.json') as f:
        colors = json.load(f)

    number_of_frames = duration*60*fps
    df = DataHandler.DataHandler(excel_file="data/DesktopOS.xlsx", number_of_frames=number_of_frames).df
    canvas = Canvas.canvas()
    width = int(canvas.canvas["width"])
    height = int(canvas.canvas["height"])

    # add stacked bar chart
    stacked = StackedBarChart.stacked_bar_chart(
        canvas=canvas.canvas,
        df=df,
        title="Stacked",
        font_size=14,
        font_color=(150,150,150),
        colors=colors,
        height=int(height-150),
        width=int(width-400),
        x_pos=50,
        y_pos=100
    )
    canvas.add_sub_plot(stacked)

    # add time indication
    date = Date.date(
        canvas=canvas.canvas, 
        height=int(height / 20),
        width=int(width / 20), 
        x_pos=int(height / 0.62), 
        y_pos=int(width / 40), 
        time_indicator="month", 
        df=df, 
        number_of_bars=25
    )
    canvas.add_sub_plot(date)

    # save colors for next run
    with open("colors/colors.json", "w") as file:
        json.dump(colors, file, indent=4)

    canvas.play(fps=fps)

if __name__ == "__main__":
    main()