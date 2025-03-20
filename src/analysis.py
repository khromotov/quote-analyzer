import pandas as pd


def sma(df: pd.DataFrame, window: int = 14, price_column: str = "close") -> pd.Series:
    return df[price_column].rolling(window=window).mean()


def ema(df: pd.DataFrame, span: int = 14, price_column: str = "close") -> pd.Series:
    return df[price_column].ewm(span=span, adjust=False).mean()


def macd(df: pd.DataFrame, short_span: int = 12, long_span: int = 26, signal_span: int = 9, price_column: str = "close") -> pd.DataFrame:
    short_ema = ema(df, span=short_span, price_column=price_column)
    long_ema = ema(df, span=long_span, price_column=price_column)
    macd_line = short_ema - long_ema
    signal_line = macd_line.ewm(span=signal_span, adjust=False).mean()
    histogram = macd_line - signal_line

    df["MACD"] = macd_line
    df["Signal"] = signal_line
    df["MACD_Hist"] = histogram
    return df


def ichimoku(df: pd.DataFrame, tenkan_period=9, kijun_period=26, senkou_span_b_period=52) -> pd.DataFrame:
    high = df["high"]
    low = df["low"]
    close = df["close"]

    df["tenkan"] = (high.rolling(tenkan_period).max() + low.rolling(tenkan_period).min()) / 2
    df["kijun"] = (high.rolling(kijun_period).max() + low.rolling(kijun_period).min()) / 2
    df["senkou_a"] = ((df["tenkan"] + df["kijun"]) / 2).shift(kijun_period)
    df["senkou_b"] = (high.rolling(senkou_span_b_period).max() + low.rolling(senkou_span_b_period).min()) / 2
    df["senkou_b"] = df["senkou_b"].shift(kijun_period)
    df["chikou"] = close.shift(-kijun_period)

    return df


if __name__ == "__main__":
    from preprocessing import load_data_yahoo, preprocess_data

    df = preprocess_data(load_data_yahoo("AAPL"))
    df = macd(df)
    df = ichimoku(df)
    print(df[["MACD", "Signal", "tenkan", "kijun"]].tail())
