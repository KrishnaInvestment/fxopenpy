from trades.open_position import Position


def open_market_position(symbol, amount, side, **kwargs):
    position = Position(symbol, amount, side)
    result = position.open_market_position(**kwargs)
    return result

def open_limit_position(symbol, amount, side, price, **kwargs):
    position = Position(symbol, amount, side)
    result = position.open_limit_position(price, **kwargs)
    return result
    
def open_stop_position(symbol, amount, side, stop_price, **kwargs):
    position = Position(symbol, amount, side)
    result = position.open_stop_position(stop_price, **kwargs)
    return result

def open_stop_limit_position(symbol, amount, side, price, stop_price, **kwargs):
    position = Position(symbol, amount, side)
    result = position.open_stop_limit_position(price, stop_price, **kwargs)
    return result

