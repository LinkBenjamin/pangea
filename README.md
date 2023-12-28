# pangea

In order to use this, add a 'keys.py' file to your project directory (don't worry, it's .gitignored) and enter the following values:

NOTION_TOKEN = your notion api token
NOTION_DB = your notion database ID

PANGEA_TOKEN = your Pangea API token
PANGEA_DOMAIN = your Pangea domain value


You must also have a Notion DB setup with the following fields:
- IPAddress (plain text)
- Lat (number)
- Long (number)

Then you can run 

`python main.py`