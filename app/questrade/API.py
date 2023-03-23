"""Core module for Questrade API wrapper."""

import logging
from typing import Any, Dict, List, Optional, Union

import requests

log = logging.getLogger(__name__)

### Highly inspired from https://github.com/jborchma/qtrade
### As I'm using different auth strategy: Implicit OAuth Flow (versus Authorization Code Flow)
### I had to keep this class focused on wrapping the API (might push a PR in future)
class API:
    """Questrade baseclass.

    This class holds the methods to get access tokens, refresh access tokens as well as get
    stock quotes and portfolio overview. An instance of the class needs to be either initialized
    with an access_code or the path of a access token yaml file.

    Parameters
    ----------
    access_code: str, optional
        Access code from Questrade
    token_yaml: str, optional
        Path of the yaml-file holding the token payload
    save_yaml: bool, optional
        Boolean to indicate if the token payload will be saved in a yaml-file. Default True.
    """

    def __init__(
        self,
        access_token: str,
        api_server: str
    ):
        self.access_token = access_token
        self.api_server = api_server.rstrip('/')

        self.headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)

        self.account_id = None
        self.positions = None

    def _send_message(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        json: Optional[Dict] = None,
    ) -> Dict[str, Any]:  # pylint: disable=R0913
        """Send an API request.

        Parameters
        ----------
        method: str
            HTTP method (get, post, delete, etc.)
        endpoint: str
            Endpoint (to be added to base URL)
        params: dict, optional
            HTTP request parameters
        data: dict, optional
            JSON-encoded string payload for POST
        json: dict, optional
            Dictionary payload for POST

        Returns
        -------
        dict/list:
            JSON response
        """
        if self.access_token is not None:
            url = self.api_server + "/v1/" + endpoint
        else:
            log.error("Access token not set...")
            raise Exception("Access token not set...")
        resp = self.session.request(method, url, params=params, data=data, json=json, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_account_id(self) -> List[int]:
        """Get account ID.

        This method gets the accounts ID connected to the token.

        Returns
        -------
        list:
            List of account IDs.
        """
        log.info("Getting account ID...")
        response: Dict[str, List[Dict[str, int]]] = self._send_message("get", "accounts")

        account_id = []
        try:
            for account in response["accounts"]:
                account_id.append(account["number"])
        except Exception:
            log.error(response)
            raise Exception

        self.account_id = account_id  # type: ignore

        return account_id

    def get_account_positions(self, account_id: int) -> List[Dict]:
        """Get account positions.

        This method will get the positions for the account ID connected to the token.

        The returned data is a list where for each position, a dictionary with the following
        data will be returned:

        .. code-block:: python

            {'averageEntryPrice': 1000,
            'closedPnl': 0,
            'closedQuantity': 0,
            'currentMarketValue': 3120,
            'currentPrice': 1040,
            'isRealTime': False,
            'isUnderReorg': False,
            'openPnl': 120,
            'openQuantity': 3,
            'symbol': 'XYZ',
            'symbolId': 1234567,
            'totalCost': 3000}


        Parameters
        ----------
        account_id: int
            Account ID for which the positions will be returned.

        Returns
        -------
        list:
            List of dictionaries, where each list entry is a dictionary with basic position
            information.

        """
        log.info("Getting account positions...")
        response = self._send_message("get", "accounts/" + str(account_id) + "/positions")
        try:
            positions = response["positions"]
        except Exception:
            print(response)
            raise Exception

        self.positions = positions

        return positions

    def get_account_balances(self, account_id: int) -> Dict:
        """Get account balances.

        This method will get the account balance for a given account ID.

        Parameters
        ----------
        account_id: int
            Accound ID for which the activities will be returned.

        Returns
        -------
        dict:
            Dictionary holding balance information
        """
        log.info("Getting account activities...")
        response = self._send_message("get", "accounts/" + str(account_id) + "/balances")
        try:
            return response
        except Exception:
            print(response)
            raise Exception

    def get_account_activities(self, account_id: int, start_date: str, end_date: str) -> List[Dict]:
        """Get account activities.

        This method will get the account activities for a given account ID in a given time
        interval.

        This method will in general return a list of dictionaries, where each dictionary represents
        one trade/account activity. Each dictionary is of the form

        .. code-block:: python

            {'action': 'Buy',
            'commission': -5.01,
            'currency': 'CAD',
            'description': 'description text',
            'grossAmount': -1000,
            'netAmount': -1005.01,
            'price': 10,
            'quantity': 100,
            'settlementDate': '2018-08-09T00:00:00.000000-04:00',
            'symbol': 'XYZ.TO',
            'symbolId': 1234567,
            'tradeDate': '2018-08-07T00:00:00.000000-04:00',
            'transactionDate': '2018-08-09T00:00:00.000000-04:00',
            'type': 'Trades'}

        Parameters
        ----------
        account_id: int
            Accound ID for which the activities will be returned.
        startDate: str
            Start date of time period, format YYYY-MM-DD
        endDate: str
            End date of time period, format YYYY-MM-DD

        Returns
        -------
        list:
            List of dictionaries, where each list entry is a dictionary with basic order & dividend
            information.

        """
        payload = {
            "startTime": str(start_date) + "T00:00:00-05:00",
            "endTime": str(end_date) + "T00:00:00-05:00",
        }

        log.info("Getting account activities...")
        response = self._send_message(
            "get", "accounts/" + str(account_id) + "/activities", params=payload
        )

        try:
            activities = response["activities"]
        except Exception:
            print(response)
            raise Exception

        return activities

    def ticker_information(self, tickers: Union[str, List[str]]) -> Union[Dict, List[Dict]]:
        """Get ticker information.

        This function gets information such as a quote for a single ticker or a list of tickers.

        Parameters
        ----------
        tickers: str or [str]
            List of tickers or a single ticker

        Returns
        -------
        dict or [dict]
            Dictionary with ticker information or list of dictionaries with ticker information
        """
        if isinstance(tickers, str):
            tickers = [tickers]

        payload = {"names": ",".join(tickers)}

        log.info("Getting ticker data...")
        response = self._send_message("get", "symbols", params=payload)
        try:
            symbols = response["symbols"]
        except Exception:
            print(response)
            raise Exception

        if len(tickers) == 1:
            symbols = symbols[0]

        return symbols

    def get_quote(self, tickers: List[str]) -> Union[Dict, List[Dict]]:
        """Get quote.

        This function gets information such as a quote for a single ticker or a list of tickers.

        Parameters
        ----------
        tickers: [str]
            List of tickers

        Returns
        -------
        dict or [dict]
            Dictionary with quotes or list of dictionaries with quotes
        """
        if isinstance(tickers, str):
            tickers = [tickers]

        # translate tickers to IDs
        info = self.ticker_information(tickers)
        if len(tickers) == 1 and isinstance(info, dict):
            ids = [info["symbolId"]]
        else:
            ids = [stock["symbolId"] for stock in info]

        payload = {"ids": ",".join(map(str, ids))}

        log.info("Getting quote...")
        response = self._send_message("get", "markets/quotes", params=payload)
        try:
            quotes = response["quotes"]
        except Exception:
            print(response)
            raise Exception

        if len(ids) == 1:
            quotes = quotes[0]

        return quotes

    def get_historical_data(
        self, ticker: str, start_date: str, end_date: str, interval: str
    ) -> List:
        """Get historical ticker data.

        This method get gets historical data for a time interval and a defined time frequency.

        Parameters
        ----------
        ticker: str
            Ticker Symbol
        start_date: str
            Date in the format YYYY-MM-DD
        end_date: str
            Date in the format YYYY-MM-DD
        interval: str
            Time frequency, i.e. OneDay.

        Returns
        -------
        list:
            list of historical data for each interval. The list is ordered by date.
        """
        # translate tickers to IDs
        info = self.ticker_information(ticker)
        if isinstance(info, dict):
            ids = info["symbolId"]
        else:
            log.error(f"Something went wrong retrieving the symbol ID for ticker {ticker}...")
            raise Exception(f"Something went wrong retrieving the symbol ID for ticker {ticker}...")
        payload = {
            "startTime": str(start_date) + "T00:00:00-05:00",
            "endTime": str(end_date) + "T00:00:00-05:00",
            "interval": str(interval),
        }

        log.info(
            "Getting historical data for {0} from {1} to {2}".format(ticker, start_date, end_date)
        )

        response = self._send_message("get", "markets/candles/" + str(ids), params=payload)
        try:
            quotes = response["candles"]
        except Exception:
            print(response)
            raise Exception

        return quotes

    def submit_order(self, acct_id: int, order_dict: Dict[str, Union[int, bool, str]]) -> Dict:
        """Submit order.

        This method submits an order to Questrade. Note that currently only partner apps can submit
        orders to the Questrade API. The order information is provided in a dictionary of the form

        .. code-block:: python

            {'accountNumber': 1234567,
            'symbolId': 3925293,
            'quantity': 1,
            'icebergQuantity': 1,
            'limitPrice': 57.58,
            'isAllOrNone': True,
            'isAnonymous': False,
            'orderType': 'Limit',
            'timeInForce': 'GoodTillCanceled',
            'action': 'Buy',
            'primaryRoute': 'AUTO',
            'secondaryRoute': 'AUTO'}

        Parameters
        ----------
        acct_id: int
            Account ID for the account to which the order is to be submitted.
        order_dict: dict
            Dictionary with the necessary order entries.

        Returns
        -------
        dict
            Dictionary with the API response to the order submission.
        """
        uri = self.api_server + "/v1/accounts/" + str(acct_id) + "/orders"
        log.info("Posting order...")
        data = self.session.post(uri, json=order_dict)
        data.raise_for_status()
        response = self._send_message(
            "post", "accounts/" + str(acct_id) + "/orders", json=order_dict
        )

        return response

    def get_option_chain(self, ticker: str) -> Dict:
        """Retrieve an option chain for a particular underlying symbol.

        https://www.questrade.com/api/documentation/rest-operations/market-calls/symbols-id-options

        This method will return a dictionary of the form

        .. code-block:: python

            {
                "options": [
                {
                  "expiryDate": "2015-01-17T00:00:00.000000-05:00",
                  "description": "BANK OF MONTREAL",
                  "listingExchange": "MX",
                  "optionExerciseType": "American",
                  "chainPerRoot": [
                  {
                    "root": "BMO",
                    "chainPerStrikePrice": [
                    {
                      "strikePrice": 60,
                      "callSymbolId": 6101993,
                      "putSymbolId": 6102009
                    },
                    {
                      "strikePrice": 62,
                      "callSymbolId": 6101994,
                      "putSymbolId": 6102010
                    },
                    {
                      "strikePrice": 64,
                      "callSymbolId": 6101995,
                      "putSymbolId": 6102011
                    }],
                    "multiplier": 100
                  }]
                }]
            }

        Parameters
        ----------
        ticker: str
            Ticker symbol

        Returns
        -------
        dict:
            Dictionary of option chain information for a particular symbol.
        """
        log.info(f"Getting option chain for ticker {ticker} ...")
        info = self.ticker_information([ticker])
        if not isinstance(info, dict):
            log.error(f"Something went wrong retrieving the symbol ID for ticker {ticker}...")
            raise Exception(f"Something went wrong retrieving the symbol ID for ticker {ticker}...")
        symbol_id = info["symbolId"]
        response = self._send_message("get", "symbols/" + str(symbol_id) + "/options")
        return response

    def get_option_quotes(self, filters: List[Dict], option_ids: List[int]) -> Dict:
        """Retrieve a single Level 1 market quote and Greek data for one or more option symbols.

        www.questrade.com/api/documentation/rest-operations/market-calls/markets-quotes-options

        This method will return a dictionary of the form

        .. code-block:: python

            {"optionQuotes": [
                    {
                        "underlying": "MSFT",
                        "underlyingId": 27426,
                        "symbol": "MSFT20Jan17C70.00",
                        "symbolId": 7413503,
                        "bidPrice": 4.90,
                        "bidSize": 0,
                        "askPrice": 4.95,
                        "askSize": 0,
                        "lastTradePriceTrHrs": 4.93,
                        "lastTradePrice": 4.93,
                        "lastTradeSize": 0,
                        "lastTradeTick": "Equal",
                        "lastTradeTime": "2015-08-17T00:00:00.000000-04:00",
                        "volume": 0,
                        "openPrice": 0,
                        "highPricehighPrice": 4.93,
                        "lowPrice": 0,
                        "volatility": 52.374257,
                        "delta": 0.06985,
                        "gamma": 0.01038,
                        "theta": -0.001406,
                        "vega": 0.074554,
                        "rho": 0.04153,
                        "openInterest": 2292,
                        "delay": 0,
                        "isHalted": False,
                        "VWAP": 0,
                    }
                ]
            }

        Parameters
        ----------
        filters: List of dictionaries
            List of filters. For example

            .. code-block:: python

                [
                    {
                     "optionType": "Call",
                     "underlyingId": 27426,
                     "expiryDate": "2017-01-20T00:00:00.000000-05:00",
                     "minstrikePrice": 70,
                     "maxstrikePrice": 80
                     }
                 ]

         option_ids: [int]
             List of option IDs

        Returns
        -------
        dict:
             Dictionary of option quotes.
        """
        log.info(
            "Getting option quotes for filter {0} and option_ids {1} ...".format(
                filters, option_ids
            )
        )
        payload = dict()
        if filters is not None:
            payload["filters"] = filters
        if option_ids is not None:
            payload["optionIds"] = option_ids
        response = self._send_message("post", "markets/quotes/options", json=payload)
        return response

    def __del__(self):
        """Close session when class instance is deleted."""
        self.session.close()