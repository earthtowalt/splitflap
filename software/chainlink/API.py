import yfinance as yf

NUM_FLAPS = 6

def get_quote(ticker):
    # Fetching data using yfinance
    sp500_data = yf.download(ticker, period="1d", interval="1d")

    # Displaying the most recent data
    if not sp500_data.empty:
        current_sp500_level = sp500_data['Close'][-1]

        def space_pad(s):
            if len(s) < NUM_FLAPS:
                s = ' ' * (NUM_FLAPS - len(s)) + s
            return s

        # if one decimal would cause over NUM_FLAPS chars, do no decimals...
        if len(f"{current_sp500_level:.1f}") > NUM_FLAPS:
            return space_pad(str(int(current_sp500_level)))
        
        return space_pad(f"{current_sp500_level:.1f}")

def get_sp500():
    return get_quote('^GSPC')
    