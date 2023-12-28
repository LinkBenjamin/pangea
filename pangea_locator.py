import miniupnpc
import pangea.exceptions as pangea
from pangea.config import PangeaConfig
from pangea.services import IpIntel
from pprint import pprint

from keys import PANGEA_TOKEN
from keys import PANGEA_DOMAIN

class Pangea_Locator():
    def __init__(self):
        self.pangea_token = PANGEA_TOKEN
        self.pangea_domain = PANGEA_DOMAIN
        self.pangea_config = PangeaConfig(domain=self.pangea_domain)
        self.intel = IpIntel(self.pangea_token, config=self.pangea_config)

    def locate(self, ipaddresses):

        response = self.intel.geolocate_bulk(
            ips=ipaddresses,
            provider="digitalelement",
        )

        format_response = {
            'latitude': response.result.data[ipaddresses[0]].latitude,
            'longitude': response.result.data[ipaddresses[0]].longitude
        }

        return format_response
