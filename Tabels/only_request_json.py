
import requests, re, json
import time

start = time.time()


def get_world_info():
    jsonfile = requests.get('https://api.tibiadata.com/v1/worlds.json')
    todos = json.loads(jsonfile.text)
    list_of_servers =  [item['name'] for item in todos['worlds']['allworlds']]
    print(list_of_servers)
    return list_of_servers


def get_characters_info(list_of_servers):
    for server in list_of_servers:
        jsonfile = requests.get('https://api.tibiadata.com/v2/world/'+server+'.json')
        todos = json.loads(jsonfile.text)


list_of_servers = get_world_info()
get_characters_info(list_of_servers)

end = time.time()

print(end - start)
