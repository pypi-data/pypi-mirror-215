import logging
from pruebaFesteban import poke_request

logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    idx = 1
    logging.info(
        f"Executing the request to the pokemon api with the id #{idx}")
    pokemon_data = poke_request(idx)
    logging.info(pokemon_data.__doc__)
    print(pokemon_data["name"])
