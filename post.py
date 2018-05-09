#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FileName: 	post
# CreatedDate:  2018-05-09 11:23:37 +0900
# LastModified: 2018-05-09 14:52:32 +0900
#


import os
import sys
import numpy as np
import pandas as pd
import requests
import json
from urllib.parse import urlencode


class Post():
    def __init__(self, Categories, Genres, Accounts):
        # read Data
        self.Categories = Categories
        self.Genres = Genres
        self.Accounts = Accounts

        # variable
        self.BaseUrl = 'https://api.zaim.net/v2/home/money/'
        self.Mode = None
        self.Data = {
            'mapping': '1',
            'category_id': '',
            'genre_id': '',
            'amount': '',
            'date': '',
            'from_account_id': '',
            'comment': '',
            'name': '',
            'place': ''
        }

    def PostData(self, auth):
        url = self.BaseUrl + self.Mode
        r = requests.post(url, auth=auth, data=urlencode(self.Data))
        print(r.status_code)
        if r.status_code == 200:
            print("success!")
        else:
            print("failed")

    def MakeInputData(self):
        # amount
        Amount = input("How much?\n")
        self.Data['amount'] = Amount
        print()

        # date (match?)
        Date = input("When?\nFormat:YYYY-MM-DD\n")
        self.Data['date'] = Date
        print()

        # mode
        self.Mode = input("Which is Mode?\npayment or income\n")
        print()

        # category
        print("{0} LIST".format(self.Mode))
        print(
            ' '.join(list(self.Categories[self.Categories["mode"] == self.Mode]["name"])))
        Category = input("What is Category?\n")
        self.Data['category_id'] = self.Categories[self.Categories["name"]
                                       == Category]["id"].values[0]
        print()

        # genre
        print("{0} LIST".format(Category))
        print(' '.join(list(
            self.Genres[self.Genres["category_id"] == self.Data['category_id']]['name'])))
        Genre = input("What is Genre?\n")
        self.Data['genre_id'] = self.Genres[self.Genres["name"]
                                                == Genre]["id"].values[0]
        print()

        # account
        print("Account LIST")
        print(
            ' '.join(list(self.Accounts[self.Accounts["active"] == 1]['name'])))
        Account = input("What is Account?\n")
        self.Data['from_account_id'] = self.Accounts[self.Accounts["name"]
                                                         == Account]["id"].values[0]
        print()

        for key in self.Data.keys():
            self.Data[key] = str(self.Data[key])

        # print test
        print(self.Data)
