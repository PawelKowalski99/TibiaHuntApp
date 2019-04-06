import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TibiaHuntApp.settings")
django.setup()
import requests, re, json
from bs4 import BeautifulSoup
from Tabels.models import Character, Servers



def get_characters_info():
    jsonfile = requests.get('https://api.tibiadata.com/v2/world/Antica.json')
    todos = json.loads(jsonfile.text)
    online_players = int(todos['world']['world_information']['players_online'])
    for i in range(online_players):
        nickname = todos['world']['players_online'][i]['name']
        vocation = todos['world']['players_online'][i]['vocation']
        level = todos['world']['players_online'][i]['level']
        server_name = todos['world']['world_information']['name']

        character = Character(name=nickname, vocation=vocation, level=level, server_name=server_name)
        character.save()
        print(nickname)

get_characters_info()