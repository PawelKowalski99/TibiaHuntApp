import django
import os
import time
import requests
import json


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TibiaHuntApp.settings")
django.setup()
from django import db
from Tabels.models import Character, Servers

start = time.time()
db.connections.close_all()


Servers.objects.all().delete()
Character.objects.all().delete()


def get_world_info():
    jsonfile = requests.get('https://api.tibiadata.com/v1/worlds.json')
    todos = json.loads(jsonfile.text)
    #jsonfile_guilds = requests.get('https://api.tibiadata.com/v2/guilds/' + server + '.json')
    Servers.objects.bulk_create([
        Servers(name=item['name'],
                players_online=item['online']
                ) for item in todos['worlds']['allworlds']]
    )

    list_of_servers = [server.name for server in
                       Servers.objects.all()]  # --> Czytanie z bazy danych szybsze o 1 sek niż czytanie z jsona
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
    all_characters = []
    for server in list_of_servers:
        jsonfile_server = requests.get('https://api.tibiadata.com/v2/world/' + server + '.json')
        todos = json.loads(jsonfile_server.text)
        server_name = todos['world']['world_information']['name']
        print(server)
        for player_data in todos['world']['players_online']:
            print(server)
            characters = [
                Character(
                    name=player_data['name'],
                    vocation=player_data['vocation'],
                    level=player_data['level'],
                    server_name=server,
                )
        ]
        # characters = [
        #     Character(
        #         name=player_data['name'],
        #         vocation=player_data['vocation'],
        #         level=player_data['level'],
        #         server_name=server_name,
        #         guild_name=
        #     ) for player_data in todos['world']['players_online']
        # ]

        all_characters.extend(characters)

    Character.objects.bulk_create(all_characters)


list_of_servers = get_world_info()
get_characters_info(list_of_servers)

end = time.time()

print(end - start)
