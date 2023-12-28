from pangea_locator import Pangea_Locator
from pprint import pprint

p = Pangea_Locator()

r = p.locate(ipaddresses=['12.12.13.14'])

pprint(r)