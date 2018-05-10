#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FileName: 	zaim
# CreatedDate:  2017-12-04 19:10:34 +0900
# LastModified: 2018-05-10 18:27:22 +0900
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
from post import Post

# authorize
key_data = pd.read_csv("./key.csv")
consumer_key = key_data["consumer_key"].values[0]
consumer_secret = key_data["consumer_secret"].values[0]
access_token = key_data["access_token"].values[0]
access_secret = key_data["access_secret"].values[0]
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)


def main():
    # set option
    paresr = argparse.ArgumentParser(
        description="Visualize household accounts in zaim.net as graphs and lists.")
    paresr.add_argument('-p', '--place', action='store_true',
                        help='search for KEYWORD in place', default=False)
    paresr.add_argument('-i', '--input', action='store_true',
                        help='Input data', default=False)
    paresr.add_argument('-m', '--mode', action='store', choices=[
                        'payment', 'income', 'transfer'], help='choice kind of movement of money', default='payment')
    paresr.add_argument('-n', '--num', action='store',
                        type=int, help='decide the number of movement to display', default=10)
    paresr.add_argument('-g', '--graph', metavar='YYYY-MM', action='store',
                        type=str, help='select category and draw graph in a month', default=0)
    # graph option (type(int))
    args = paresr.parse_args()

    # variable
    Mdata = GetData("money", "money").loc[:, [
        'amount', 'date', 'mode', 'place', 'category_id', 'genre_id']]
    Cdata = GetData("category", "categories")
    Gdata = GetData("genre", "genres")
    # Vdata = verify()
    Adata = GetData("account", "accounts")
    PayStr = "payment"
    IncStr = "income"

    # input data
    if args.input:
        post = Post(Cdata, Gdata, Adata)
        post.MakeInputData()
        post.PostData(auth)
        sys.exit(1)

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

        # check category exist
        try:
            CategoryId = Cdata[Cdata["name"] == keyword]["id"].values[0]
        except IndexError:
            print("ERROR: category don't exist")
            sys.exit(1)

        # draw graph
        graph.DrawGraph(args.graph, CategoryId)
        sys.exit(1)

    # search for keyword in place
    if args.place:
        keyword = input("What is location KEYWORD?\n")
        Mdata = Mdata[Mdata["place"].str.contains(keyword)]

    # set movement of money
    Mdata = Mdata[Mdata["mode"].str.contains(
        args.mode)].reset_index(drop=True)
    Mdata = Mdata.replace('\ 00:00:00$', '')

    # replace category_id with category_name
    Ctmp = Mdata['category_id']
    Gtmp = Mdata['genre_id']
    Mdata = Mdata.drop(['category_id', 'genre_id'], axis=1)
    for i in range(0, len(Cdata.index)):
        Ctmp = Ctmp.replace(Cdata.loc[i, "id"], Cdata.loc[i, "name"])
    for i in range(0, len(Gdata.index)):
        Gtmp = Gtmp.replace(Gdata.loc[i, "id"], Gdata.loc[i, "name"])
    Mdata = pd.concat([Mdata, Ctmp, Gtmp], axis=1).rename(
        columns={"category_id": "category", "genre_id": "genre"})

    # output
    display(Mdata.loc[:(args.num - 1), :])


# def verify():
#     endpoint = "https://api.zaim.net/v2/home/user/verify"
#
#     r = requests.get(endpoint, auth=auth)
#     Vdata = pd.read_json(json.dumps(r.json()))
#
#     return Vdata


def GetData(Name, Group):
    endpoint = "https://api.zaim.net/v2/home/" + Name

    r = requests.get(endpoint, auth=auth)
    data = pd.read_json(json.dumps(r.json()[Group]))

    return data


if __name__ == "__main__":
    main()
