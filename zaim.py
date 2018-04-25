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
from IPython.display import display

# myfunc
from graph import Graph

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
    Mdata = money()
    tmp = Mdata['category_id']
    Mdata = money().loc[:, ['amount', 'date', 'mode', 'place']]
    Cdata = category()
    Vdata = verify()
    PayStr = "payment"
    IncStr = "income"

    # replace category_id with category_name
    for i in range(0, len(Cdata.index)):
        tmp = tmp.replace(Cdata.loc[i, "id"], Cdata.loc[i, "name"])
    Mdata = pd.concat([Mdata, tmp], axis=1).rename(
        columns={"category_id": "category"})

    # constructor
    graph = Graph(Mdata, Cdata)

    # draw relative payment graph
    graph.RelativePayment()

    # draw monthly category graph
    graph.MonthlyCategoryGraph()

    # check option
    # draw category graph
    if not args.graph == 0:
        # write category list
        print("CATEGORY LIST")
        print(PayStr)
        print(' '.join(list(Cdata[Cdata["mode"] == PayStr]["name"])))
        print(IncStr)
        print(' '.join(list(Cdata[Cdata["mode"] == IncStr]["name"])))
        print()
        keyword = input("What is CATEGORY?\n")
        graph.DrawGraph(args.graph, keyword)
        sys.exit(1)

    # search for keyword in place
    if args.place:
        keyword = input("What is location KEYWORD?\n")
        Mdata = Mdata[Mdata["place"].str.contains(keyword)]

    # set movement of money
    Mdata = Mdata[Mdata["mode"].str.contains(
        args.mode)].reset_index(drop=True)
    Mdata = Mdata.replace('\ 00:00:00$', '')

    # output
    display(Mdata.loc[:(args.num - 1), :])


def verify():
    endpoint = "https://api.zaim.net/v2/home/user/verify"

    r = requests.get(endpoint, auth=auth)
    Vdata = pd.read_json(json.dumps(r.json()))

    return Vdata


def category():
    endpoint = "https://api.zaim.net/v2/home/category"

    r = requests.get(endpoint, auth=auth)
    Cdata = pd.read_json(json.dumps(r.json()["categories"]))

    return Cdata


def money():
    endpoint = "https://api.zaim.net/v2/home/money"

    r = requests.get(endpoint, auth=auth)
    Mdata = pd.read_json(json.dumps(r.json()["money"]))

    return Mdata


if __name__ == "__main__":
    main()
