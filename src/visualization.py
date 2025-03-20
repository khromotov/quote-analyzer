import pandas as pd
import matplotlib.pyplot as plt
import os


def plot_price_with_alerts(df, title="Price with Alerts"):
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df["Close"], label="Close Price", color="gray")

    buy_signals = df[df["alert"] == "BUY"]
    sell_signals = df[df["alert"] == "SELL"]

    plt.scatter(buy_signals.index, buy_signals["Close"], marker="^", color="green", label="BUY", zorder=5)
    plt.scatter(sell_signals.index, sell_signals["Close"], marker="v", color="red", label="SELL", zorder=5)

    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def export_alerts_to_excel(df, filename="alerts_report.xlsx"):
    os.makedirs("reports", exist_ok=True)
    path = os.path.join("reports", filename)

    # Сигналы
    signals = df[df["alert"] != "NONE"]

    # Доходность стратегии
    df = df.copy()
    df["position"] = df["alert"].map({"BUY": 1, "SELL": -1, "NONE": 0}).ffill().fillna(0)
    df["returns"] = df["Close"].pct_change()
    df["strategy"] = df["returns"] * df["position"].shift(1)
    df["equity"] = (1 + df["strategy"]).cumprod()

    with pd.ExcelWriter(path) as writer:
        df.to_excel(writer, sheet_name="Full Data")
        signals.to_excel(writer, sheet_name="Alerts")

    print(f"Отчёт сохранён: {path}")
