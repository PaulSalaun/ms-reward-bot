import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(dir_path, "profils_list.json")
with open(file_path, 'r') as f:
    data = json.load(f)


def get_email(index):
    selected_profil = data['profils'][index]
    return selected_profil['email']


def get_pass(index):
    selected_profil = data['profils'][index]
    return selected_profil['password']


def get_len():
    nombre_de_profils = len(data['profils'])
    return nombre_de_profils
