#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FileName: 	post
# CreatedDate:  2018-05-09 11:23:37 +0900
# LastModified: 2018-05-14 17:43:42 +0900
#


import os
import sys
import numpy as np
import pandas as pd
import requests
import re
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
        }

    def PostData(self, auth):
        url = self.BaseUrl + self.Mode
        r = requests.post(url, auth=auth, data=urlencode(self.Data))

        if r.status_code == 200:
            print("success!")
        else:
            print("failed")

    def MakeInputData(self):
        # amount
        Amount = input("How much?\n")
        if not re.match("^[1-9][0-9]*$", Amount):
            print("ERROR: number isn't suitable")
            sys.exit(1)
        self.Data['amount'] = Amount
        print()

        # date
        Date = input("When?\nFormat:YYYY-MM-DD\n")
        if not re.match("^20[0-9]{2}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])", Date):
            print("ERROR: date isn't suitable")
            sys.exit(1)
        self.Data['date'] = Date
        print()

        # mode
        self.Mode = input("Which is Mode?\npayment or income or transfer\n")
        print()
        if not re.match("(payment|income|transfer)", self.Mode):
            print("ERROR: mode don't exist")
            sys.exit(1)

        # account
        print("Account LIST")
        print(
            ' '.join(list(self.Accounts[self.Accounts["active"] == 1]['name'])))

        if re.match("(payment|transfer)", self.Mode):
            Account = input("What is from Account?\n")
            try:
                self.Data['from_account_id'] = self.Accounts[self.Accounts["name"]
                                                             == Account]["id"].values[0]
            except IndexError:
                print("ERROR: Account don't exist")
                sys.exit(1)
            print()

        if re.match("(income|transfer)", self.Mode):
            Account = input("What is to Account?\n")
            try:
                self.Data['to_account_id'] = self.Accounts[self.Accounts["name"]
                                                           == Account]["id"].values[0]
            except IndexError:
                print("ERROR: Account don't exist")
                sys.exit(1)
            print()

        if re.match("(payment|income)", self.Mode):
            # category
            print("{0} category LIST".format(self.Mode))
            print(
                ' '.join(list(self.Categories[self.Categories["mode"] == self.Mode]["name"])))
            Category = input("What is Category?\n")
            try:
                self.Data['category_id'] = self.Categories[self.Categories["name"]
                                                           == Category]["id"].values[0]
            except IndexError:
                print("ERROR: category don't exist")
                sys.exit(1)
            print()

            if self.Mode == 'payment':
                # genre
                print("{0} genre LIST".format(Category))
                print(' '.join(list(
                    self.Genres[self.Genres["category_id"] == self.Data['category_id']]['name'])))
                Genre = input("What is Genre?\n")
                try:
                    self.Data['genre_id'] = self.Genres[self.Genres["name"]
                                                        == Genre]["id"].values[0]
                except IndexError:
                    print("ERROR: genre don't exist")
                    sys.exit(1)
                print()

        for key in self.Data.keys():
            self.Data[key] = str(self.Data[key])
