# encode : utf-8
# Python 3.10
# ----------------------------------------------------------------------------

import os
import dotenv

from src.core.client import Angels


def main():

    client = Angels()
    client_token = dotenv.get_key(
        dotenv_path=dotenv.find_dotenv(), key_to_get="CLIENT_TOKEN", encoding="utf-8"
    )

    if client_token:
        client.run(client_token)


if __name__ == "__main__":
    main()
