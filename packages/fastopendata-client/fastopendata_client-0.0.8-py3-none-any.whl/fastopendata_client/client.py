import logging
import pprint
import requests

FASTOPENDATA_URL = "http://localhost:8000"
SAMPLE_PARAMS = {"free_form_query": "1984 Lower Hawthorne Trail"}


class FastOpenData:
    """
    The client for interacting with the FastOpenData service.
    """

    def __init__(
        self, ip_address: str = "localhost", port: int = 8000, scheme: str = "http"
    ) -> None:
        self.ip_address = ip_address
        self.port = str(port)
        self.scheme = scheme
        self.url = f'{self.scheme}://{self.ip_address}:{self.port}'

    def request(self, free_form_query: str = None, city: str = None, state: str = None, address: str = None, zip_code: str = None) -> dict:
        '''
        Make a request from the FastOpenData service.
        '''
        response = requests.get(self.url, params={'free_form_query': free_form_query})
        return response.json()


logging.basicConfig(level=logging.DEBUG)
#response = requests.get(FASTOPENDATA_URL, params=SAMPLE_PARAMS)

#data = response.json()
session = FastOpenData()
data = session.request('1984 Lower Hawthorne Trail')
pprint.pprint(data)
