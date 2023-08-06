from requests_oauthlib import OAuth2Session
import json
from requests import post
from .upload import TwitterMedia
from .file import read, write

def print_response(r):
    if 'application/json' in r.headers.get('Content-Type', ''):
        return json.dumps(r.json(), indent=2)
    return r.text

class Tweet:
    def __init__(self, client_id=None, client_secret=None, callback_uri=None, token_saver=lambda x: write(file_path='../token.json', contents=x), token_fetcher=lambda: read('../token.json')):
        self.client_id = client_id
        self.client_secret = client_secret
        self.callback_uri = callback_uri
        self.token_saver = token_saver
        self.token_fetcher = token_fetcher
        self.__OAuth = None

    def tweet(self, text='', image_path=None):
        'TODO: only fetch new token if current is expired'
        'TODO: expose a save_token variable that lets consumers decide if they want the new token saved'
        token = self.refresh_token()
        payload = {}
        if text:
            payload["text"] = text
        if image_path:
            payload["media"] = {"media_ids": [self._upload_image(image_path)]}
        api_response = post(
            "https://api.twitter.com/2/tweets",
            json=payload,
            headers={
                "Authorization": f"Bearer {token['access_token']}",
                "Content-Type": "application/json",
            },
        )
        return api_response.status_code, print_response(api_response)
    
    def _upload_image(self, image_path):
        twitterMedia = TwitterMedia(image_path)
        twitterMedia.upload_init()
        twitterMedia.upload_append()
        twitterMedia.upload_finalize()
        return str(twitterMedia.media_id)

    @property
    def _OAuth(self):
        if self.__OAuth:
            return self.__OAuth
        self.__OAuth = OAuth2Session(self.client_id, redirect_uri=self.callback_uri, scope=["tweet.read", "users.read", "tweet.write", "offline.access"])
        return self.__OAuth

    def refresh_token(self):
        token = self.token_fetcher()
        token = self._OAuth.refresh_token(
            client_id=self.client_id,
            client_secret=self.client_secret,
            token_url="https://api.twitter.com/2/oauth2/token",
            refresh_token=token["refresh_token"],
        )
        self.token_saver(token)
        print("token refreshed and saved")
        return token
