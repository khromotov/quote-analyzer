# run_strategy.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

import yfinance as yf
from models import calculate_indicators, generate_alerts
from visualization import export_alerts_to_excel, plot_price_with_alerts


def run_strategy(ticker, start_date="2023-01-01", end_date="2024-01-01"):
    print(f"[INFO] Запуск стратегии для {ticker} с {start_date} по {end_date}")

    df = yf.download(ticker, start=start_date, end=end_date)
    df = calculate_indicators(df)
    df = generate_alerts(df)

    df["position"] = df["alert"].map({"BUY": 1, "SELL": -1, "NONE": 0}).ffill().fillna(0)
    df["returns"] = df["Close"].pct_change().fillna(0)
    df["strategy"] = df["returns"] * df["position"].shift(1).fillna(0)
    df["equity"] = (1 + df["strategy"]).cumprod()

    final_return = df["equity"].iloc[-1] - 1
    print(f"[RESULT] {ticker}: Доходность стратегии: {final_return:.2%}")

    filename = f"alerts_report_{ticker}.xlsx"
    export_alerts_to_excel(df, filename=filename)
    plot_price_with_alerts(df, title=f"{ticker} Alerts")


def run_multiple(tickers, start_date, end_date):
    for ticker in tickers:
        run_strategy(ticker, start_date, end_date)


if __name__ == "__main__":
    tickers = ["AAPL", "MSFT", "GOOGL", "NVDA", "TSLA"]
    run_multiple(tickers, start_date="2023-01-01", end_date="2024-01-01")