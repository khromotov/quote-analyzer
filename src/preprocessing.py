import pandas as pd
import numpy as np
import yfinance as yf


def load_data_yahoo(ticker: str, start: str = "2020-01-01", end: str = "2024-12-31", interval: str = "1d") -> pd.DataFrame:
    """
    Загрузка исторических данных с Yahoo Finance.
    """
    df = yf.download(ticker, start=start, end=end, interval=interval)
    df = df.rename(columns={
        "Open": "open", "High": "high", "Low": "low",
        "Close": "close", "Adj Close": "adj_close", "Volume": "volume"
    })
    df = df.dropna()
    df.index = pd.to_datetime(df.index)
    return df


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Предобработка: удаление пропусков, удаление выбросов (по z-оценке).
    """
    df = df.dropna()
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        z_score = (df[col] - df[col].mean()) / df[col].std()
        df = df[(z_score > -3) & (z_score < 3)]
    return df


if __name__ == "__main__":
    data = load_data_yahoo("AAPL")
    clean_data = preprocess_data(data)
    print(clean_data.head())
