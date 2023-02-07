import requests
import json
from config import keys


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(iz: str, w: str, sk: str):
        if iz == w:
            raise APIException(f'Невозможно переводить одинаковые валюты "{iz}"')

        try:
            iz_ticker = keys[iz]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{iz}"')

        try:
            w_ticker = keys[w]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{w}"')

        try:
            sk = float(sk)
        except ValueError:
            raise APIException(f'Неверно прописано количество {sk}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={iz_ticker}&tsyms={w_ticker}')
        total_base = json.loads(r.content)[keys[w]]
        return total_base
