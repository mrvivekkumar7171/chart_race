import pandas as pd
import matplotlib.pyplot as plt # pip install matplotlib
import matplotlib.animation as animation

# Read Excel file
df = pd.read_excel("data/nuclear.xlsx")

# Ensure the first column is the year (index)
df = df.set_index(df.columns[0])

# List of countries (columns after the year)
countries = df.columns.tolist()

# Set up the figure
fig, ax = plt.subplots(figsize=(10, 6))

def update(year):
    ax.clear()
    values = df.loc[year].sort_values(ascending=True)
    ax.barh(values.index, values.values, color="skyblue")
    ax.set_title(f"Nuclear Warheads by Country - {year}", fontsize=16)
    ax.set_xlabel("Number of Nuclear Warheads")
    ax.set_xlim(0, df.max().max() * 1.1)  # scale to max value
    for i, (val, name) in enumerate(zip(values.values, values.index)):
        ax.text(val, i, str(val), va='center', ha='left', fontsize=9)

# Create animation
ani = animation.FuncAnimation(
    fig, update, frames=df.index, interval=1000, repeat=False
)

# Save animation as mp4 (requires ffmpeg installed)
ani.save("img/matplotlib.mp4", writer="ffmpeg", dpi=150)

plt.show()