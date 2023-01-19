import json
import time
from datetime import datetime
import requests


def _nonce():
    # Returns a nonce
    # Used in authentication
    return int(round(time.time() * 10000))


class Fava:
    BASE_URL = "https://restdoc.algotrader.com/"

    def __init__(self, public: str, secret: str):
        self.KEY = public
        self.SECRET = secret

    def req(self, path, params=None, is_post: bool = True):
        if params is None:
            params = {}
        body = params
        raw_body = json.dumps(body)
        print(raw_body)
        headers = self._headers()
        url = self.BASE_URL + path
        resp = requests.post(url, headers=headers, data=raw_body, verify=True) \
            if is_post else requests.get(url, headers=headers, data=raw_body, verify=True)
        return resp

    def get_account(self):
        # Fetch active orders
        response = self.req('rest/account', is_post=False)
        if response.status_code == 200:
            return response.json()
        else:
            print('error, status_code = ', response.status_code)
            return ''

    def _headers(self):
        return {
            "X-API-Key": self.KEY,
            "X-API-Secret": self.SECRET,
            "content-type": "application/json"
        }

    def suggest_order(self, position: str):
        """
        {"id":38,"name":"Okcoin_Account","active":false,"primaryForTrading":false,"primaryForMarketData":false,
        "primaryForReferenceData":true,"primaryForAccountData":true,"providerId":37,
        "connectorDescriptor":{"descriptor":"Okcoin"},"sessionQualifier":null,"extAccount":null,
        "extAccountGroup":null,"extAllocationProfile":null,"extClearingAccount":null,
        "rfqSupported":false,"objectType":"Account
        Example value parameter
        {
              "accountId": 0,
              "customPropertiesCustomizedOrder":
              {
                    "additionalProp1": {},
                    "additionalProp2": {},
                    "additionalProp3": {}
              },
              "customPropertiesInternal":
              {
                    "additionalProp1": {},
                    "additionalProp2": {},
                    "additionalProp3": {}
              },
              "dateTime": "2022-01-19T09:03:09.104Z",
              "exchangeId": 0,
              "exchangeOrder": true,
              "extId": "string",
              "id": 0,
              "intId": "string",
              "lastStatus": "CANCELED",
              "parentIntId": "string",
              "parentOrderId": 0,
              "portfolioId": 0,
              "quantity": 0,
              "securityId": 0,
              "side": "BUY",
              "tif": "ATC",
              "tifDateTime": "2022-01-19T09:03:09.104Z",
              "@class": "ch.algotrader.entity.trade.MarketOrderVO"
        }
        :param position:
        :return:
        """
        params = {
              "accountId": 0,
              "customPropertiesCustomizedOrder":
              {
                    "additionalProp1": {},
                    "additionalProp2": {},
                    "additionalProp3": {}
              },
              "customPropertiesInternal":
              {
                    "additionalProp1": {},
                    "additionalProp2": {},
                    "additionalProp3": {}
              },
              "dateTime": str(datetime.now()),
              "exchangeId": 0,
              "exchangeOrder": True,
              "extId": "string",
              "id": 0,
              "intId": "string",
              "lastStatus": "CANCELED",
              "parentIntId": "string",
              "parentOrderId": 0,
              "portfolioId": 0,
              "quantity": 0,
              "securityId": 0,
              "side": position,
              "tif": "ATC",
              "tifDateTime": "2022-01-19T09:03:09.104Z",
              "@class": "ch.algotrader.entity.trade.MarketOrderVO"
        }
        response = self.req('rest/execution/suggestOrder', is_post=True,
                            params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print('error, status_code = ', response.status_code)
            return ''
