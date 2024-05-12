# coding : utf-8
# Python 3.10
# ----------------------------------------------------------------------------
# IN CASE OF EMERGENCY ONLY
# ----------------------------------------------------------------------------

import requests
import dotenv


path = dotenv.find_dotenv()

application_id = dotenv.get_key(
    dotenv_path=path, key_to_get="APPLICATION_ID", encoding="utf-8"
)
bot_token = dotenv.get_key(
    dotenv_path=path, key_to_get="CLIENT_TOKEN", encoding="utf-8"
)

url = f"https://discord.com/api/v10/applications/{application_id}/commands"
headers = {
    "Authorization": f"Bot {bot_token}",
}

def unload_application_commands():

    response = requests.get(url, headers=headers)

    for data in response.json():
        result = requests.delete(
            url = (
                f"https://discord.com/api/v10/applications/{application_id}"
                + f"/commands/{data['id']}"
            ),
            headers = headers,
        )
