import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
from preprocessing import load_data_yahoo, preprocess_data
from analysis import sma, ema, macd, ichimoku
from models import rolling_volatility
from visualization import export_report

class TestPipeline(unittest.TestCase):
    def test_full_flow(self):
        df = load_data_yahoo("MSFT", start="2023-01-01", end="2023-03-01")
        df = preprocess_data(df)

        df["SMA_20"] = sma(df, 20)
        df["EMA_20"] = ema(df, 20)
        df = macd(df)
        df = ichimoku(df)
        df["volatility"] = rolling_volatility(df, 20)

        export_report(df, filename="test_report.xlsx")
        self.assertTrue(os.path.exists("reports/test_report.xlsx"))

if __name__ == '__main__':
    unittest.main()
