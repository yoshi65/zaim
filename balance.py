#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FileName: 	balance
# CreatedDate:  2018-05-17 11:04:39 +0900
# LastModified: 2018-05-17 12:12:22 +0900
#


import os
import sys
import numpy as np
import pandas as pd
import re


class Balance():
    def __init__(self, Data, Accounts):
        # read Data
        self.Data = Data
        self.Accounts = Accounts[Accounts["active"]
                                 == 1].reset_index(drop=True)
        self.Diff = pd.read_csv("./balance_diff.csv")

    def CalcBalance(self):
        BalanceList = []
        print("Balance")

        # calc
        for index in range(0, len(self.Accounts.index)):
            AccountId = self.Accounts.loc[index, "id"]
            Total = self.Data[self.Data["to_account_id"] == AccountId]["amount"].sum(
            ) - self.Data[self.Data["from_account_id"] == AccountId]["amount"].sum() - self.Diff[str(AccountId)].values[0]
            Name = self.Accounts.loc[index, "name"]

            # print
            if len(Name) < 4 or re.match("^[A-Z]{4,7}$", Name):
                print("{0}\t\t:{1}".format(Name, str(Total).rjust(8)))
            else:
                print("{0}\t:{1}".format(Name, str(Total).rjust(8)))

        print()
