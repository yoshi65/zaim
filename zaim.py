#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FileName: 	zaim
# CreatedDate:  2017-12-04 19:10:34
#


import os
import sys
import json
import numpy as np
import pandas as pd
import requests
from requests_oauthlib import OAuth1
import argparse
import pandas.plotting._converter as pandacnv
from IPython.display import display

# myfunc
import graph
pandacnv.register()

# authorize
key_data = pd.read_csv("./key.csv")
consumer_key = key_data["consumer_key"].values[0]
consumer_secret = key_data["consumer_secret"].values[0]
access_token = key_data["access_token"].values[0]
access_secret = key_data["access_secret"].values[0]
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)


def main():
    # set option
    paresr = argparse.ArgumentParser(description="analyze zaim from CUI")
    paresr.add_argument('-p', '--place', action='store_true',
                        help='search for KEYWORD in place', default=False)
    paresr.add_argument('-m', '--mode', action='store', choices=[
                        'payment', 'income', 'transfer'], help='choice kind of movement of money', default='payment')
    paresr.add_argument('-n', '--num', action='store',
                        type=int, help='decide drawing number of movement', default=10)
    paresr.add_argument('-g', '--graph', action='store',
                        type=str, help='select category and draw graph in a month (ex. -g 2018-01)', default=0)
    # graph option (type(int))
    args = paresr.parse_args()

    # variable
    m_data = money()
    tmp = m_data['category_id']
    m_data = money().loc[:, ['amount', 'date', 'mode', 'place']]
    c_data = category()
    v_data = verify()
    # m_data = m_data.set_index('date')

    # replace category_id with category_name
    for i in range(0, len(c_data.index)):
        tmp = tmp.replace(c_data.loc[i, "id"], c_data.loc[i, "name"])
    m_data = pd.concat([m_data, tmp], axis=1).rename(
        columns={"category_id": "category"})

    # draw graph
    if not args.graph == 0:
        keyword = input("What is CATEGORY?\n")
        graph.draw_graph(m_data, args.graph, keyword)
        sys.exit(1)
    graph.RelativePayment(m_data)

    # check option
    # search for keyword in place
    if args.place:
        keyword = input("What is KEYWORD?\n")
        m_data = m_data[m_data["place"].str.contains(keyword)]
    # set movement of money
    m_data = m_data[m_data["mode"].str.contains(
        args.mode)].reset_index(drop=True)

    # output
    display(m_data.loc[:(args.num - 1), :])


def verify():
    endpoint = "https://api.zaim.net/v2/home/user/verify"

    r = requests.get(endpoint, auth=auth)
    v_data = pd.read_json(json.dumps(r.json()))

    return v_data


def category():
    endpoint = "https://api.zaim.net/v2/home/category"

    r = requests.get(endpoint, auth=auth)
    c_data = pd.read_json(json.dumps(r.json()["categories"]))

    return c_data


def money():
    endpoint = "https://api.zaim.net/v2/home/money"

    r = requests.get(endpoint, auth=auth)
    m_data = pd.read_json(json.dumps(r.json()["money"]))

    return m_data


if __name__ == "__main__":
    main()
