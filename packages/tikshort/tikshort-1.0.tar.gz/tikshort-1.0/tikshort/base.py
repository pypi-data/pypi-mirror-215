import requests
import json

class TikShorten():
    def short(link):
        url = "https://www.tiktok.com/shorten/?target={}&belong=tiktok_tv_short_url".format(link)
        response = requests.post(url)
        try:
            vardxg = response.json()
            if 'message' in vardxg and vardxg['message'] == "error":
                return print("\n Link Cannot be empty.")
            else:
                return print("\n Shorten Url >>> \033[92m{}\033[0m".format(vardxg['data']))
        except json.JSONDecodeError:
            print("\n There is A error in the request try again.")