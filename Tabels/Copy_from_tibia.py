import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TibiaHuntApp.settings")
django.setup()
import requests, re, json
from bs4 import BeautifulSoup
from Tabels.models import Character, Servers
import time

start = time.time()
from django import db
db.connections.close_all()

def get_page_content(world):
    page = requests.get(f'https://www.tibia.com/community/?subtopic=worlds&world={world}')
    content = page.content
    return content


# def get_characters_info(content):
#     soup = BeautifulSoup(content, 'html.parser')
#     main_content_odd = soup.select(" tr.Odd td a ")
#     main_content_even = soup.select(" tr.Even td a ")
#     names_odd = [name.get_text() for name in main_content_odd]
#     names_even = [name.get_text() for name in main_content_even]
#     names = [name.replace("\xa0", " ") for name in names_odd + names_even]
#     names = sorted(names)
#     for name in names:
#         if names[0] == '':
#             del names[0]
#     return names
Servers.objects.all().delete()
Character.objects.all().delete()

def get_world_info():
    jsonfile = requests.get('https://api.tibiadata.com/v1/worlds.json')
    todos = json.loads(jsonfile.text)
    Servers.objects.bulk_create([
        Servers(name=item['name'], players_online=item['online']) for item in todos['worlds']['allworlds']]
    )

    list_of_servers = [server.name for server in Servers.objects.all()] #--> Czytanie z bazy danych szybsze o 1 sek niż czytanie z jsona
   # list_of_servers = [server['name'] for server in todos['worlds']['allworlds']]
   # print([server.name for server in Servers.objects.all()])
    return list_of_servers

def save_characters(response):
    todos = json.loads(response.text)
    print(response.url)
    server_name = todos['world']['world_information']['name']
    characters = [
        Character(
            name=player_data['name'],
            vocation=player_data['vocation'],
            level=player_data['level'],
            server_name=server_name
        ) for player_data in todos['world']['players_online']
    ]
    print(server_name)
    Character.objects.bulk_create(characters)

def get_characters_info(list_of_servers):
    # all_characters = []
    import grequests
    import gevent.monkey
    gevent.monkey.patch_all()

    async_list = []
    for server in list_of_servers:
        # jsonfile = requests.get('https://api.tibiadata.com/v2/world/'+server+'.json')
        action_item = grequests.get('https://api.tibiadata.com/v2/world/'+server+'.json', hooks=dict(response=save_characters))
        job = grequests.send(action_item, grequests.Pool(1))
        # todos = json.loads(jsonfile.text)
        # server_name = todos['world']['world_information']['name']
        # characters = [
        #     Character(
        #         name=player_data['name'],
        #         vocation=player_data['vocation                                                    '],
        #         level=player_data['level'],
        #         server_name=server_name
        #     ) for player_data in todos['world']['players_online']
        # ]

        # all_characters.extend(characters)
        #
    # Character.objects.bulk_create(all_characters)
    # print(grequests.map(async_list))

list_of_servers = get_world_info()
get_characters_info(list_of_servers)


end = time.time()

print(end - start)


