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

    def __del__(self):
        """Close session when class instance is deleted."""
        self.session.close()