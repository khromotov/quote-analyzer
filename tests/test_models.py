import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
import numpy as np
from preprocessing import load_data_yahoo, preprocess_data
from models import rolling_volatility, rolling_mean_reversion, black_litterman

class TestModels(unittest.TestCase):
    def setUp(self):
        df = load_data_yahoo("AAPL", start="2023-01-01", end="2023-03-01")
        self.df = preprocess_data(df)

    def test_volatility(self):
        self.df["vol"] = rolling_volatility(self.df, 10)
        self.assertIn("vol", self.df.columns)

    def test_z_score(self):
        self.df["z"] = rolling_mean_reversion(self.df, 10)
        self.assertIn("z", self.df.columns)

    def test_black_litterman(self):
        pi = np.array([0.05, 0.03])
        cov = np.array([[0.1, 0.02], [0.02, 0.08]])
        tau = 0.05
        P = np.array([[1, -1]])
        Q = np.array([0.01])
        omega = np.array([[0.02]])
        result = black_litterman(pi, cov, tau, P, Q, omega)
        self.assertEqual(len(result), 2)

if __name__ == '__main__':
    unittest.main()
