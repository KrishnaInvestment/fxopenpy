import datetime
import requests
import pandas as pd
from dateutil import parser
from utils.fxopenheaders import get_auth_headers
import historical_data.urls as hist_urls
import json
from utils.constants import TIME_INTERVAL


class HistoricalCurrencyData:
    def __init__(self):
        self.symbol = None
        self.periodicity = None
        self.data_type = None

    def get_periodicities(self, symbol):
        url = hist_urls.GET_PERIODCITIES % symbol
        response = requests.get(url, headers=get_auth_headers(url))
        return json.loads(response.text)

    def get_currency_data_by_time(
        self, symbol, periodicity, data_type, start_time, end_time=None
    ):
        self.symbol, self.periodicity, self.data_type = symbol, periodicity, data_type
        end, start = self._get_timestamp(symbol, periodicity, data_type)
        start_time = self._validate_start_time(start_time, start)
        end_time = self._validate_end_time(end_time, end)

        all_data = self._fetch_historical_data(start_time, end_time, periodicity)
        df = pd.concat(all_data)
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="ms")
        df = df[
            (df["Timestamp"] >= start_time) & (df["Timestamp"] <= end_time)
        ].sort_values("Timestamp")

        return df

    def get_currency_data_by_bars(
        self, symbol, periodicity, data_type, original_bars, end_time=None
    ):
        self.symbol, self.periodicity, self.data_type = symbol, periodicity, data_type
        no_of_bars = int(original_bars * 1.50)
        end, _ = self._get_timestamp(symbol, periodicity, data_type)
        end_time = self._validate_end_time(end_time, end)
        time_period_seconds = TIME_INTERVAL.get(periodicity)
        epoch_time_seconds = int(end_time.timestamp())

        all_data = []
        while no_of_bars > 0:
            total_bars = min(no_of_bars, 1000)
            epoch_time_seconds = epoch_time_seconds - total_bars * time_period_seconds
            all_data.append(
                self._get_historical_data_df(epoch_time_seconds * 1000, total_bars)
            )
            no_of_bars -= len(all_data[-1])
            epoch_time_seconds = int(all_data[-1]["Timestamp"].iloc[0] / 1000)

        df = pd.concat(all_data)
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="ms")
        df = (
            df[df["Timestamp"] <= end_time]
            .drop_duplicates("Timestamp")
            .sort_values("Timestamp")
        )
        return df[-original_bars:]

    def _validate_start_time(self, start_time, start):
        start_time = parser.parse(start_time)
        return max(start_time, start)

    def _validate_end_time(self, end_time, end):
        end_time = parser.parse(end_time) if end_time else end
        return end_time

    def _fetch_historical_data(self, start_time, end_time, periodicity):
        time_difference = (end_time - start_time).total_seconds()
        time_period_seconds = TIME_INTERVAL.get(periodicity)
        all_data = []

        while time_difference > 0:
            epoch_time_milliseconds = int(start_time.timestamp() * 1000)
            no_of_bars = min(int(time_difference / time_period_seconds), 1000)

            all_data.append(
                self._get_historical_data_df(epoch_time_milliseconds, no_of_bars)
            )
            start_time += datetime.timedelta(
                seconds=TIME_INTERVAL.get(periodicity) * 1000
            )
            time_difference = (end_time - start_time).total_seconds()

        return all_data

    def _get_historical_data_df(self, epoch_time_milliseconds, no_of_bars):
        url = hist_urls.QUOTEHISTORY_DATA % (
            self.symbol,
            self.periodicity,
            self.data_type,
        )
        url += f"?timestamp={epoch_time_milliseconds}&count={no_of_bars}"
        response = requests.get(url, headers=get_auth_headers(url))
        response_text = json.loads(response.text)
        return pd.DataFrame(response_text.get("Bars"))

    def _get_timestamp(self, symbol, periodicity, trade_type):
        url = hist_urls.QUOTEHISTORY % (symbol, periodicity, trade_type)
        response = requests.get(url, headers=get_auth_headers(url))
        response_text = json.loads(response.text)
        end_time = datetime.datetime.fromtimestamp(
            response_text.get("AvailableTo") / 1000
        )
        start_time = datetime.datetime.fromtimestamp(
            response_text.get("AvailableFrom") / 1000
        )
        return end_time, start_time
