import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
from preprocessing import load_data_yahoo, preprocess_data

class TestPreprocessing(unittest.TestCase):
    def test_load_data(self):
        df = load_data_yahoo("AAPL", start="2023-01-01", end="2023-02-01")
        self.assertFalse(df.empty)
        self.assertIn("close", df.columns)

    def test_preprocess(self):
        df = load_data_yahoo("AAPL", start="2023-01-01", end="2023-02-01")
        clean_df = preprocess_data(df)
        self.assertFalse(clean_df.isnull().values.any())

if __name__ == '__main__':
    unittest.main()
