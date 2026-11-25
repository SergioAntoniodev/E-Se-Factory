import random

temas = [
    "E se a Lua desaparecesse?",
    "E se o Sol apagasse por 24 horas?",
    "E se os dinossauros voltassem?",
    "E se a humanidade ficasse sem internet?",
    "E se a gravidade deixasse de existir?",
    "E se todos os oceanos secassem?",
    "E se você pudesse parar o tempo?",
    "E se a Terra parasse de girar?"
]


def gerar_ideia():
    ideia = random.choice(temas)
    return ideia


if __name__ == "__main__":
    print("=== GERADOR DE IDEIAS E SE...? ===")
    print()
    print("Sua próxima ideia de vídeo:")
    print(gerar_ideia())