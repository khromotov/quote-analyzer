import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
from preprocessing import load_data_yahoo, preprocess_data
from analysis import sma, ema, macd, ichimoku

class TestAnalysis(unittest.TestCase):
    def setUp(self):
        df = load_data_yahoo("AAPL", start="2023-01-01", end="2023-03-01")
        self.df = preprocess_data(df)

    def test_sma(self):
        self.df["SMA"] = sma(self.df, 10)
        self.assertIn("SMA", self.df.columns)

    def test_ema(self):
        self.df["EMA"] = ema(self.df, 10)
        self.assertIn("EMA", self.df.columns)

    def test_macd(self):
        df = macd(self.df)
        self.assertIn("MACD", df.columns)

    def test_ichimoku(self):
        df = ichimoku(self.df)
        self.assertIn("tenkan", df.columns)
        self.assertIn("kijun", df.columns)

if __name__ == '__main__':
    unittest.main()
