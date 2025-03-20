# tests/test_pipeline.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
import pandas as pd
from datetime import datetime
from models import calculate_indicators, generate_alerts
from visualization import export_alerts_to_excel
import yfinance as yf


class TestStrategyPipeline(unittest.TestCase):
    def test_profitability_and_export(self):
        df = yf.download("AAPL", start="2023-01-01", end="2024-01-01")
        df = calculate_indicators(df)
        df = generate_alerts(df)

        # Расчёт доходности после генерации сигналов
        df["position"] = df["alert"].map({"BUY": 1, "SELL": -1, "NONE": 0}).ffill().fillna(0)
        df["returns"] = df["Close"].pct_change().fillna(0)
        df["strategy"] = df["returns"] * df["position"].shift(1).fillna(0)
        df["equity"] = (1 + df["strategy"]).cumprod()

        # Проверки
        self.assertGreater(len(df), 0)
        self.assertIn("equity", df.columns)
        equity_change = df["equity"].iloc[-1] - df["equity"].iloc[0]
        self.assertNotEqual(equity_change, 0)

        # Экспорт в Excel
        export_alerts_to_excel(df, filename="test_alerts_report.xlsx")

        print(f"Final Return: {(df['equity'].iloc[-1] - 1):.2%}")


if __name__ == '__main__':
    unittest.main()
