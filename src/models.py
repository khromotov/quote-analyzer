def calculate_indicators(df):
    df = df.copy()
    # EMA/SMA
    df["EMA_20"] = df["Close"].ewm(span=20, adjust=False).mean()
    df["SMA_20"] = df["Close"].rolling(window=20).mean()

    # MACD
    df["EMA_12"] = df["Close"].ewm(span=12, adjust=False).mean()
    df["EMA_26"] = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = df["EMA_12"] - df["EMA_26"]
    df["MACD_Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

    # Ichimoku
    high_9 = df["High"].rolling(window=9).max()
    low_9 = df["Low"].rolling(window=9).min()
    df["tenkan"] = (high_9 + low_9) / 2

    high_26 = df["High"].rolling(window=26).max()
    low_26 = df["Low"].rolling(window=26).min()
    df["kijun"] = (high_26 + low_26) / 2

    df["ichimoku_signal"] = 0
    df.loc[df["tenkan"] > df["kijun"], "ichimoku_signal"] = 1
    df.loc[df["tenkan"] < df["kijun"], "ichimoku_signal"] = -1

    # Volatility
    df["volatility"] = df["Close"].rolling(window=20).std()

    # Z-score
    rolling_mean = df["Close"].rolling(window=20).mean()
    rolling_std = df["Close"].rolling(window=20).std()
    df["z_score"] = (df["Close"] - rolling_mean) / rolling_std

    return df


def generate_alerts(df):
    df = df.copy()
    alerts = []

    for i in range(1, len(df)):
        row = df.iloc[i]
        try:
            ichi = float(row["ichimoku_signal"])
            macd = float(row["MACD"])
            macd_sig = float(row["MACD_Signal"])
            ema = float(row["EMA_20"])
            price = float(row["Close"])
            vol = float(row["volatility"])
            z = float(row["z_score"])
        except:
            alerts.append("NONE")
            continue

        # Основные сигналы + математические фильтры
        if (
            ichi == 1 and
            macd > macd_sig and
            price > ema and
            vol < 10 and
            abs(z) < 2
        ):
            alerts.append("BUY")
        elif (
            ichi == -1 and
            macd < macd_sig and
            price < ema and
            vol < 10 and
            abs(z) < 2
        ):
            alerts.append("SELL")
        else:
            alerts.append("NONE")

    df = df.iloc[1:].copy()
    df["alert"] = alerts
    return df[[
        "Close", "EMA_20", "MACD", "MACD_Signal", "tenkan", "kijun",
        "ichimoku_signal", "volatility", "z_score", "alert"
    ]]