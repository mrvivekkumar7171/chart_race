# moving_average.py
import pandas as pd

def moving_average(data, window=3):
    return data.rolling(window=window).mean()

if __name__ == "__main__":
    # Example data
    dates = pd.date_range("2025-01-01", periods=10)
    values = [5, 7, 9, 4, 8, 10, 12, 11, 13, 14]
    df = pd.DataFrame({"Date": dates, "Value": values}).set_index("Date")
    df["MA_3"] = moving_average(df["Value"], window=3)
    print("📊 Time Series with 3-point Moving Average:")
    print(df)
