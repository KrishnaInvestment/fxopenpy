from utils.fxopenheaders import get_auth_headers
import trades.urls as trade_url
from trades.constant import TRADE_DATA
import json
import datetime
from utils.utils import RequstAPI, Price


class Position(RequstAPI):
    def __init__(self, symbol, amount, side):
        self.symbol = symbol
        self.amount = amount
        self.side = side
        self.base_payload = {"Symbol": symbol, "Amount": amount, "Side": side}
    
    def make_payload_key(self, string_value):
        list_value = string_value.split('_')
        list_with_titles = list(map(lambda element: element.title(),list_value))
        payload_key = ''.join(list_with_titles)
        return payload_key
        
    def get_value_type_of_parameter(self, parameter, value):
        parameter = self.make_payload_key(parameter)
        data_type = TRADE_DATA.get(parameter)
        if data_type=='number':
            Position.verify_number(value)
        elif data_type=='bool':
            Position.verify_boolean(value)
        return parameter

    def execute_position(self, payload):
        url = trade_url.GET_TRADE
        response_text = self.request_api(url, request_type="post", payload=payload)
        return response_text

    def get_stop_loss(self, side, stop_loss, price):
        Position.verify_number(stop_loss)
        if side == "Buy" and (stop_loss > 0):
            stop_loss = price * (1 - stop_loss / 100)

        elif side == "Sell" and (stop_loss > 0):
            stop_loss = price * (1 + stop_loss / 100)

        else:
            raise ValueError("Verification failed. Invalid StopLoss")
        return round(stop_loss, self.count_decimal_places(price))

    def get_target(self, side, target, price):
        Position.verify_number(target)
        if side == "Sell" and (target > 0):
            target = price * (1 - target / 100)

        elif side == "Buy" and (target > 0):
            target = price * (1 + target / 100)

        else:
            raise ValueError("Verification failed. Invalid Target")

        return round(target, self.count_decimal_places(price))

    def get_time_is_ms(self, minutes):
        Position.verify_number(minutes)
        time_now = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
        time_in_ms = int(time_now.timestamp()*1000)
        return time_in_ms
    
    @staticmethod
    def verify_number(number):
        is_number = isinstance(number, int) or isinstance(number, float)
        
        if not is_number:
            raise ValueError(
                "Verification failed. Expected a number, but received a non-numeric value"
            )
            
        if number<0:
            raise ValueError(
                "Verification failed. Expected a positive number, but received a negative value"
            )
            
    
    @staticmethod
    def verify_boolean(bool_value):
        is_bool = isinstance(bool_value, bool)
        
        if not is_bool:
            raise ValueError(
                "Verification failed. Expected a bool, but received a non-bool value"
            )
            
    @staticmethod
    def count_decimal_places(number):
        # Convert the number to a string
        number_str = str(number)

        # Check if the number contains a decimal point
        if "." in number_str:
            # Split the string by the decimal point
            decimal_part = number_str.split(".")[1]

            # Return the length of the decimal part
            return len(decimal_part)

        return 0  # Return 0 if the number has no decimal places

    
    def __make_payload(self, type, stop_loss=None,
                      target=None,
                      price=None,
                      stop_price=None,
                      **kwargs):
        
        payload = {"Type": type}

        if type not in ["Market", "Stop"]:
            Position.verify_number(price)
            payload["Price"] = price
            
        else:
            price = Price.get_price(self.symbol, self.side)
            if stop_price:
                price = stop_price
            
        if type in ['Stop', 'StopLimit']:
            Position.verify_number(stop_price)
            payload["StopPrice"] = stop_price 
            
        if kwargs.get('expiry'):
            payload['Expired'] = self.get_time_is_ms(kwargs.get('expiry'))
            
        if kwargs.get('trigger_time'):
            payload['TriggerTime'] = self.get_time_is_ms(kwargs.get('trigger_time'))

        if stop_loss:
            stop_loss = self.get_stop_loss(self.side, stop_loss, price)
            payload["StopLoss"] = stop_loss

        if target:
            target = self.get_target(self.side, target, price)
            payload["TakeProfit"] = target
            
        existed_keys = list(payload.keys())+list(self.base_payload.keys())
        for key,value in kwargs.items():
            parameter = self.get_value_type_of_parameter(key, value)
            if parameter not in existed_keys:
                payload[parameter] = value
        
        
        payload.update(self.base_payload)

        return payload
    
    def open_market_position(self, **kwargs):
        kwargs['type'] = 'Market'
        payload = self.__make_payload(**kwargs)
        result = self.execute_position(payload)
        return result
    
    def open_limit_position(self, price, **kwargs):
        kwargs['type'] = 'Limit'
        kwargs['price'] = price
        payload = self.__make_payload(**kwargs)
        result = self.execute_position(payload)
        return result
    
    def open_stop_position(self, stop_price, **kwargs):
        kwargs['type'] = 'Stop'
        kwargs['stop_price'] = stop_price
        payload = self.__make_payload(**kwargs)
        result = self.execute_position(payload)
        return result
    
    def open_stop_limit_position(self, price, stop_price, **kwargs):
        kwargs['type'] = 'StopLimit'
        kwargs['price'] = price
        kwargs['stop_price'] = stop_price
        payload = self.__make_payload(**kwargs)
        result = self.execute_position(payload)
        return result


