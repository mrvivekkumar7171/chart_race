from sjvisualizer import Canvas, DataHandler, BarRace, PieRace, Date, StackedBarChart, StaticImage, LineChart, AreaChart
import json


def main(fps = 60, duration = 0.2):

    number_of_frames = duration*60*fps
    # load colors
    with open('colors/colors.json') as f:
        colors = json.load(f)

    colors = {}
    df = DataHandler.DataHandler(excel_file="data/browsers.xlsx", number_of_frames=number_of_frames).df
    canvas = Canvas.canvas()

    width = int(canvas.canvas["width"])
    height = int(canvas.canvas["height"])
    chart_height = int(height/1.25)
    chart_width = int(width / 2.6)

    # creating events for the line chart
    events = {
        "Event 1": {"start_date": "28/01/1998",
                    "end_date": "28/01/2000",
                    "color": (150,150,150),
                    "label": "The Dot-com bubble"
                    },
        "Event 2": {"start_date": "28/01/2018",
                    "end_date": "28/01/2019",
                    "color": (150,150,150),
                    "label": "The GDPR comes into effect"
            }
    }

    # add a line chart
    line = LineChart.line_chart(
        canvas=canvas, 
        df=df, 
        title="Line chart",
        font_size=12,
        font_color=(0,0,0),
        colors=colors, 
        height=chart_height,
        width=chart_width, 
        x_pos=int(height / 8),
        y_pos=int(width / 14),
        events=events
    )
    canvas.add_sub_plot(line)

    # add an area chart
    area = AreaChart.area_chart(
        canvas=canvas, 
        df=df, 
        title="Area chart",
        font_size=12,
        font_color=(0,0,0),
        colors=colors, 
        height=chart_height,
        width=chart_width, 
        x_pos=int(height*0.98),
        y_pos=int(width / 14) 
    )
    canvas.add_sub_plot(area)

    # add time indication
    date = Date.date(
        canvas=canvas, 
        height=int(height / 20),
        width=int(width / 20), 
        x_pos=int(height / 0.62), 
        y_pos=int(width / 40), 
        time_indicator="year", 
        df=df
    )
    canvas.add_sub_plot(date)

    # adding a static image
    img = StaticImage.static_image(
        canvas=canvas, 
        file="img/logo.png", 
        width=height/12, 
        height=height/12, 
        x_pos=width/1.08, 
        y_pos=height/1.15
    )
    canvas.add_sub_plot(img)


    # save colors for next run
    # with open("colors/colors.json", "w") as file:
    #     json.dump(colors, file, indent=4)

    canvas.play(fps=fps)

if __name__ == "__main__":
    main()