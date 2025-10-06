import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os

# Config
INPUT_FILE = "data/nuclear.xlsx"
OUT_VIDEO = "img/matplotlib.mp4"
FPS = 1                # frames per second in output
INTERVAL_MS = 1000     # interval between frames in milliseconds (for FuncAnimation)
DPI = 150

def load_data(path):
    df = pd.read_excel(path)
    # assume first column is year (or time) and remaining columns are categories
    df = df.set_index(df.columns[0])
    # ensure it's numeric
    df = df.apply(pd.to_numeric, errors='coerce').fillna(0)
    return df

def make_colors(n):
    # pick a stable palette large enough for n categories
    cmap = plt.get_cmap('tab20')
    colors = [cmap(i % cmap.N) for i in range(n)]
    return colors

def create_animation(df, out_file, fps=FPS, interval=INTERVAL_MS, dpi=DPI):
    years = df.index.tolist()
    countries = df.columns.tolist()
    n_cats = len(countries)
    colors = make_colors(n_cats)

    # create figure with 2 subplots side-by-side
    fig, (ax_bar, ax_pie) = plt.subplots(1, 2, figsize=(14, 7))
    plt.tight_layout()

    # compute global max for consistent x-axis
    global_max = df.max().max()
    xlim = global_max * 1.1 if global_max > 0 else 1.0

    def update(year):
        ax_bar.clear()
        ax_pie.clear()

        # get values for this year
        values = df.loc[year].astype(float)

        # sort values for barh (descending -> top to bottom)
        sorted_values = values.sort_values(ascending=True)  # ascending True for barh (bottom->top)
        names = sorted_values.index.tolist()
        vals = sorted_values.values

        # BAR CHART (horizontal)
        ax_bar.barh(names, vals, color=[colors[countries.index(n) % len(colors)] for n in names])
        ax_bar.set_xlim(0, xlim)
        ax_bar.set_title(f"Nuclear Warheads by Country — {year}", fontsize=14, pad=12)
        ax_bar.set_xlabel("Number of Nuclear Warheads")
        # annotate values at end of bars
        for i, (v, name) in enumerate(zip(vals, names)):
            ax_bar.text(v + xlim*0.005, i, f"{int(v):,}", va='center', ha='left', fontsize=9)

        # PIE CHART (right)
        # Only include countries with non-zero values to avoid degenerate pie slices
        pie_vals = values.values
        pie_names = countries
        # don't reorder slices — use original columns order for stable color mapping
        # filter zero values for pie (matplotlib can handle zeros but it's cleaner)
        nonzero_mask = pie_vals > 0
        pie_vals_nz = pie_vals[nonzero_mask]
        pie_names_nz = np.array(pie_names)[nonzero_mask]
        pie_colors_nz = [colors[i % len(colors)] for i, flag in enumerate(nonzero_mask) if flag]

        if pie_vals_nz.sum() > 0:
            wedges, texts, autotexts = ax_pie.pie(
                pie_vals_nz,
                labels=pie_names_nz,
                autopct=lambda pct: f"{int(round(pct * pie_vals_nz.sum()/100)):,}",
                startangle=140,
                colors=pie_colors_nz,
                textprops={'fontsize': 8}
            )
            ax_pie.set_title(f"Distribution — {year}", fontsize=14)
            # equal aspect ratio ensures pie is drawn as a circle
            ax_pie.axis('equal')
        else:
            ax_pie.text(0.5, 0.5, "No data", ha='center', va='center')
            ax_pie.set_title(f"Distribution — {year}", fontsize=14)
            ax_pie.axis('off')

    # build animation
    ani = animation.FuncAnimation(
        fig,
        update,
        frames=years,
        interval=interval,
        repeat=False
    )

    # ensure output directory exists
    out_dir = os.path.dirname(out_file)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    # Save animation as mp4 (requires ffmpeg installed)
    try:
        writer = animation.FFMpegWriter(fps=fps)
        ani.save(out_file, writer=writer, dpi=dpi)
        print(f"Saved animation to {out_file}")
    except Exception as e:
        print("Failed to save mp4 via FFmpeg:", e)
        print("Falling back to saving GIF (slower).")
        try:
            ani.save(out_file.replace('.mp4', '.gif'), dpi=dpi, writer='pillow')
            print("Saved GIF.")
        except Exception as e2:
            print("Also failed to save GIF:", e2)

    plt.close(fig)
    return ani

if __name__ == "__main__":
    df = load_data(INPUT_FILE)
    create_animation(df, OUT_VIDEO, fps=FPS, interval=INTERVAL_MS, dpi=DPI)
