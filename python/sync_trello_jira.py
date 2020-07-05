
api_key = "1c3ed551a3eb7530af8f351f70b58513"
oauth_secret = "1da522e210be669f01e0121c15cb75872d59453dc277a36f040e1c1ccb696077"
token = "b386da3396227d7cc6c67ab6eecbbfbab4c1ba615784ec8994c20143861ff315"

"""api_key and token
https://developers.trello.com/reference#introduction

https://api.trello.com/1/members/me/?key={yourAPIKey}&token={yourAPIToken}

## list all cards
list_json_url = "https://api.trello.com/1/lists/replace_this_with_ur_list_id?cards=all&key=replace_this_with_ur_api_key&token=replace_this_with_your_token
with urllib.request.urlopen(list_json_url) as fj:
    data = json.load(fj)

"""
from trello import TrelloClient

API_KEY = "XXXXXXX"
API_TOKEN = "XXXXXXXXXX"
client = TrelloClient(api_key=API_KEY, token=API_TOKEN)

for board in client.list_boards():
    for l in board.list_lists():
        if l.id = "ur_list_id":
          #do your list analysis here
