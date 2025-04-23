import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
import pandas as pd
from models import calculate_indicators, generate_alerts
from visualization import export_alerts_to_excel
import yfinance as yf


class TestStrategyPipeline(unittest.TestCase):
    def test_multiple_tickers(self):
        tickers = ["AAPL", "MSFT", "GOOGL", "NVDA", "TSLA"]
        start_date = "2023-01-01"
        end_date = "2024-01-01"

        for ticker in tickers:
            with self.subTest(ticker=ticker):
                df = yf.download(ticker, start=start_date, end=end_date)
                df = calculate_indicators(df)
                df = generate_alerts(df)

                df["position"] = df["alert"].map({"BUY": 1, "SELL": -1, "NONE": 0}).ffill().fillna(0)
                df["returns"] = df["Close"].pct_change().fillna(0)
                df["strategy"] = df["returns"] * df["position"].shift(1).fillna(0)
                df["equity"] = (1 + df["strategy"]).cumprod()

                self.assertGreater(len(df), 0)
                self.assertIn("equity", df.columns)
                equity_change = df["equity"].iloc[-1] - df["equity"].iloc[0]
                self.assertNotEqual(equity_change, 0)

                filename = f"test_alerts_report_{ticker}.xlsx"
                export_alerts_to_excel(df, filename=filename)

                print(f"[{ticker}] Final Return: {(df['equity'].iloc[-1] - 1):.2%}")


if __name__ == '__main__':
    unittest.main()
