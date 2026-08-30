def moving_averages(close):

    return {
        "MM20": close.rolling(20).mean().iloc[-1],
        "MM50": close.rolling(50).mean().iloc[-1],
        "MM200": close.rolling(200).mean().iloc[-1]
    }
