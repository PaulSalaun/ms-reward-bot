import json
import os
from datetime import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(dir_path, "profils_list.json")
with open(file_path, 'r') as f:
    data = json.load(f)


def get_email(index: int):
    selected_profil = data['profils'][index]
    return selected_profil['email']


def get_pass(index: int):
    selected_profil = data['profils'][index]
    return selected_profil['password']


def get_reward(index: int):
    selected_profil = data['profils'][index]
    return selected_profil['rewards']


def set_reward(index: int, value: str):
    data['profils'][index]["rewards"] = value
    try:
        data["profils"][index]["rewards"] = data["profils"][index]["rewards"].replace("\u202f", "")
    except:
        pass
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


def get_streak(index: int):
    selected_profil = data['profils'][index]
    return selected_profil['streak']


def set_streak(index: int, value: str):
    data['profils'][index]["streak"] = value
    try:
        data["profils"][index]["rewards"] = data["profils"][index]["rewards"].replace("\u202f", "")
    except:
        pass
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


def get_len():
    nombre_de_profils = len(data['profils'])
    return nombre_de_profils
