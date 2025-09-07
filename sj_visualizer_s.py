from sjvisualizer import plot as plt
import json

with open('colors/colors.json') as f:
    colors = json.load(f)

plt.pie(excel="data/Nuclear.xlsx",
        title="Desktop Browser Market Share",
        sub_title="By Mr. Vivek Kumar",
        unit="%",
        duration=0.5,
        output_video="img/output.mp4",
        record=False,
        fps=60,
        time_indicator="year",
        font_color=(255, 255, 255),
        background_color=(0, 0, 0),
        colors={
            "Edge": (255, 0, 0),
            "Chrome": (0, 255, 0),
            "Safari": (0, 0, 255),
            "Opera": (255, 255, 0),
            "Firefox": (255, 0, 255),
            "IE": (0, 255, 255),
            "Others": (255, 255, 255),
            "Netscape": (128, 128, 128),
            "Mosaic": (64, 64, 64)
        },
        sort=True
        )