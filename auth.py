#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FileName: 	auth
# CreatedDate:  2017-12-04 14:56:58
#

import urllib.parse as urlparse
import requests
import pandas as pd
from requests_oauthlib import OAuth1

# authorize
key_data = pd.read_csv("./key.csv")
consumer_key = key_data["consumer_key"].values[0]
consumer_secret = key_data["consumer_secret"].values[0]

request_token_url = "https://api.zaim.net/v2/auth/request"
authorize_url = "https://auth.zaim.net/users/auth"
access_token_url = "https://api.zaim.net/v2/auth/access"
callback_uri = "https://www.zaim.net/"


def main():
    # request token
    auth = OAuth1(consumer_key, consumer_secret, callback_uri=callback_uri)
    r = requests.post(request_token_url, auth=auth)
    request_token = dict(urlparse.parse_qsl(r.text))

    # authorize
    print("auth link")
    print(authorize_url + "?oauth_token=" + request_token["oauth_token"])

    oauth_verifier = input("What is the PIN?\n")

    auth = OAuth1(consumer_key,
                  consumer_secret,
                  request_token["oauth_token"],
                  request_token["oauth_token_secret"],
                  verifier=oauth_verifier)
    r = requests.post(access_token_url, auth=auth)

    access_token = dict(urlparse.parse_qsl(r.text))

    key_data["access_token"] = access_token["oauth_token"]
    key_data["access_secret"] = access_token["oauth_token_secret"]

    key_data.to_csv("./key_tmp.csv", index=False)

    return access_token


if __name__ == "__main__":
    print(main())
