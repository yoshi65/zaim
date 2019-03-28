#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FileName: 	balance
# CreatedDate:  2018-05-17 11:04:39 +0900
# LastModified: 2019-03-28 12:34:52 +0900
#

import os
import re
import sys
from datetime import datetime

import numpy as np
import pandas as pd


class Balance():
    def __init__(self, Data, Accounts):
        # varibale
        self.diff_file = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "input/balance_diff.csv")
        if os.path.isfile(self.diff_file):
            self.Diff = pd.read_csv(self.diff_file)
        else:
            self.Diff = pd.DataFrame(
                np.zeros([1, len(Accounts.index)], dtype=int),
                columns=[str(x) for x in list(Accounts["local_id"])])

        # read Data
        self.Data = Data
        self.Data = self.Data[self.Data['date'] < datetime.now()]
        self.Accounts = Accounts[Accounts["active"] == 1].reset_index(
            drop=True)

    def CalcBalance(self):
        print("Balance")

        # calc
        for index in range(0, len(self.Accounts.index)):
            AccountId = self.Accounts.loc[index, "id"]
            Total = self.Data[self.Data["to_account_id"] == AccountId][
                "amount"].sum() - self.Data[
                    self.Data["from_account_id"] == AccountId]["amount"].sum(
                    ) - self.Diff[str(AccountId)].values[0]
            Name = self.Accounts.loc[index, "name"]

            # print
            if len(Name) < 4 or re.match("^[A-Z]{4,7}$", Name):
                print("{0}\t\t:{1}".format(Name, str(Total).rjust(8)))
            else:
                print("{0}\t:{1}".format(Name, str(Total).rjust(8)))

    def MakeBalanceDiff(self):
        BalanceList = []
        print("Actual balance check")

        # check
        for index in range(0, len(self.Accounts.index)):
            AccountId = self.Accounts.loc[index, "id"]
            Total = self.Data[self.Data["to_account_id"] == AccountId][
                "amount"].sum() - self.Data[
                    self.Data["from_account_id"] == AccountId]["amount"].sum(
                    ) - self.Diff[str(AccountId)].values[0]
            Name = self.Accounts.loc[index, "name"]

            # input
            diff = input("how much is actual balance of {}?\n".format(Name))
            if not re.match("^-*[0-9][0-9]*$", diff):
                print("ERROR: ")
                sys.exit(1)

            # calc
            BalanceList.append(Total - int(diff))

        # make diff
        BalanceDiff = pd.DataFrame(
            [BalanceList],
            columns=[str(x) for x in list(self.Accounts["local_id"])])

        # output
        BalanceDiff.to_csv(self.diff_file, index=False)
