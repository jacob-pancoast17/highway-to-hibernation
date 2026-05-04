import json
import os
from scripts.utils import resource_path

def get_var():

    return {
        "default_settings" : {
        "volume" : 5,
        "skin" : 'Grizzly',
        "debug-mode" : False
        },
        "settings_file" : "settings.json"
    }


def load_file():

    if not os.path.exists(resource_path(get_var()['settings_file'])):

        print("No settings exist. Creating default settings file")

        with open(resource_path(get_var()['settings_file']), "w", encoding="utf-8") as file:

            json.dump(get_var()['default_settings'], file, indent = 4)


def retrieve_settings(force_reload = False):

    if not os.path.exists(resource_path(get_var()['settings_file'])):

        print("No settings exist. Creating default settings file")

        load_file()

    with open(resource_path(get_var()['settings_file']), "r", encoding = "utf-8") as file:

        content = json.load(file)

        print(content)

        return(content)

def update_settings(volume = retrieve_settings()['volume'],
                    skin = retrieve_settings()['skin'],
                    debug_mode = retrieve_settings()['debug-mode']):

    if not os.path.exists(resource_path(get_var()['settings_file'])):

        print("No settings exist. Creating default settings file")

        load_file()

    to_load = {
        'volume' : volume,
        'skin' : skin,
        'debug-mode' : debug_mode
    }

    print(to_load)

    with open(resource_path(get_var()['settings_file']), "w", encoding = "utf-8") as file:

        json.dump(to_load, file, indent = 4)