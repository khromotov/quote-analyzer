import pandas as pd
import numpy as np


def rolling_volatility(df: pd.DataFrame, window: int = 20, price_column: str = "close") -> pd.Series:
    """
    Расчёт скользящей стандартной девиации (волатильности).
    """
    return df[price_column].rolling(window=window).std()


def rolling_mean_reversion(df: pd.DataFrame, window: int = 20, price_column: str = "close") -> pd.Series:
    """
    Оценка степени отклонения от скользящего среднего.
    """
    mean = df[price_column].rolling(window=window).mean()
    std = df[price_column].rolling(window=window).std()
    z_score = (df[price_column] - mean) / std
    return z_score


def black_litterman(expected_returns: np.ndarray, cov_matrix: np.ndarray, 
                    tau: float, P: np.ndarray, Q: np.ndarray, omega: np.ndarray) -> np.ndarray:
    """
    Упрощённая реализация модели Блека-Литтермана.
    """
    # Рыночная оценка
    pi = expected_returns

    # Матрицы
    middle = np.linalg.inv(np.dot(np.dot(P, tau * cov_matrix), P.T) + omega)
    adj_return = pi + np.dot(np.dot(np.dot(tau * cov_matrix, P.T), middle), (Q - np.dot(P, pi)))
    
    return adj_return


if __name__ == "__main__":
    from preprocessing import load_data_yahoo, preprocess_data

    df = preprocess_data(load_data_yahoo("MSFT"))
    df["volatility"] = rolling_volatility(df)
    df["z_score"] = rolling_mean_reversion(df)

    print(df[["close", "volatility", "z_score"]].tail())
