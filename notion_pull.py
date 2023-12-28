from notion_client import Client
from pprint import pprint

from keys import NOTION_TOKEN
from keys import NOTION_DB
from keys import NOTION_PAGE

import pandas as pd
import json 

class Notion_Puller():

    def __init__(self):
        self.notion_token = NOTION_TOKEN
        self.notion_database_id = NOTION_DB
        self.notion_page_id = NOTION_PAGE
        self.client = Client(auth=self.notion_token)


    def write_text(self,page_id, text, type):
        self.client.blocks.children.append(
            block_id=page_id,
            children=[
                {
                    "object": "block",
                    "type":type,
                    type: {
                        "rich_text": [
                            {
                                "type":"text",
                                "text": {
                                    "content": text
                                }
                            }
                        ]
                    }
                }
                
            ]
        )

    def safe_get(self, data, dot_chained_keys):
        keys = dot_chained_keys.split('.')
        for key in keys:
            try:
                if isinstance(data, list):
                    data=data[int(key)]
                else:
                    data=data[key]
            except(KeyError,TypeError,IndexError):
                return None
        return data
    
    def write_row_to_database(self, ip_address, latitude, longitude):
        new_row = {
            "IPAddress": ip_address,
            "Lat": latitude,
            "Long": longitude,
            # Add other properties as needed
        }

        # Add the new row to the Visitors database
        new_row_response = self.client.pages.create(
            parent={"database_id": self.notion_database_id},
            properties={
                "IPAddress": {"type": "title", "title": [{"type": "text", "text": {"content": ip_address}}]},
                "Lat": {"type": "number", "number": latitude},
                "Long": {"type": "number", "number": longitude},
                # Add other properties as needed
            }
        )

        # Optional: Print the response for debugging
        pprint(new_row_response)

    def write_dict_to_file_as_json(self, content, file_name):
        content_as_json_str = json.dumps(content)
        with open(file_name, 'w') as f:
            f.write(content_as_json_str)

    def read_text(self, page_id):
        response = self.client.blocks.children.list(block_id=page_id)
        return response['results']

    def get_data(self):
        db_info = self.client.databases.retrieve(database_id=self.notion_database_id)

        db_rows = self.client.databases.query(database_id=self.notion_database_id)

        return_value = []

        for row in db_rows['results']:
            ipaddress = self.safe_get(row, 'properties.IPAddress.title.0.plain_text')
            lat = self.safe_get(row, "properties.Lat.number")
            long = self.safe_get(row, "properties.Long.number")
            stamp = self.safe_get(row, "properties.Created time.created_time")

            return_value.append(
                {
                    "lat": lat,
                    "lon": long
                }
            )

        # Convert the list of dictionaries to a DataFrame
        coordinates_df = pd.DataFrame(return_value)

        return coordinates_df