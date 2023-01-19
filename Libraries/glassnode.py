import pandas as pd
from requests import RequestException, get


class GlassNode:
    BASE_URL = 'https://api.glassnode.com/v1/metrics'

    def __init__(self, api: str):
        self.api = api

    def _headers(self):
        return {
            "X-Api-Key": self.api
        }

    def get(self, path, params=None):
        if params is None:
            params = {}
        headers = self._headers()
        url = self.BASE_URL + path
        try:
            resp = get(url=url, headers=headers, params=params, verify=True)
            data = resp.json()
            data = pd.DataFrame(data=data)
            data.t = pd.DatetimeIndex(pd.to_datetime(data['t'], unit='s', yearfirst=True)).tz_localize(
                'UTC').tz_convert('Asia/Tehran')
            return data
        except RequestException as e:
            print(e)

    def sopr(self, symbol: str):
        res = self.get(path='/blockchain/utxo_created_value_sum', params={'a': symbol})
        print(res)


# gl = GlassNode(api='24MvA2KSAeUdyyRRlf7bSgXJ9wR')
# gl.sopr(symbol='eth')
