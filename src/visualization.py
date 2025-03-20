import matplotlib.pyplot as plt
import pandas as pd
import os


def plot_price_with_indicators(df: pd.DataFrame, indicators: list = None, title: str = "Price with Indicators"):
    """
    График цены + выбранные индикаторы
    """
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df["close"], label="Close Price", linewidth=1.5)

    if indicators:
        for ind in indicators:
            if ind in df.columns:
                plt.plot(df.index, df[ind], label=ind)

    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_macd(df: pd.DataFrame):
    """
    MACD-гистограмма и сигнальные линии.
    """
    plt.figure(figsize=(14, 5))
    plt.plot(df.index, df["MACD"], label="MACD", color="blue")
    plt.plot(df.index, df["Signal"], label="Signal", color="orange")
    plt.bar(df.index, df["MACD_Hist"], label="Histogram", color="gray", alpha=0.4)

    plt.title("MACD")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def export_report(df: pd.DataFrame, filename: str = "report.xlsx"):
    """
    Сохранение результата анализа в Excel-отчёт.
    """
    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    df.to_excel(filepath)
    print(f"[INFO] Отчёт сохранён: {filepath}")


if __name__ == "__main__":
    from preprocessing import load_data_yahoo, preprocess_data
    from analysis import sma, ema, macd

    df = preprocess_data(load_data_yahoo("TSLA"))
    df["SMA_20"] = sma(df, 20)
    df["EMA_20"] = ema(df, 20)
    df = macd(df)

    plot_price_with_indicators(df, ["SMA_20", "EMA_20"])
    plot_macd(df)
    export_report(df)
