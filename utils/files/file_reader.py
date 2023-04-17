from typing import TextIO


def read_and_return_loop(nom_fichier: str, i: int) -> int:
    with open(nom_fichier, 'r') as f:
        contenu = f.read()
        sequence = contenu.strip()
        if i < len(sequence):
            return int(sequence[i])
        else:
            return None
