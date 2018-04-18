#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FileName: 	graph
# CreatedDate:  2018-04-13 14:12:23
#


import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import calendar
import re
from matplotlib import ticker
from datetime import datetime


class Graph():

    def __init__(self, Data):
        # read Data
        self.Data = Data
        self.Data['date'] = self.Data['date'].astype(datetime)
        self.Data = self.Data.set_index('date')

        # output path
        self.dir_path = os.path.dirname(os.path.abspath(__file__))
        self.output_path = os.path.join(self.dir_path, "data")

    def MakeList(self, DataType, Keyword, Month):
        NumofDays = calendar.monthrange(
            int(re.sub(r"-.*$", "", Month)), int(re.sub(r"^.*-", "", Month)))[1]
        DataList = self.Data[self.Data[DataType]
                             == Keyword].resample('D').sum()
        DataList = DataList[Month + '-01':Month + '-' + str(NumofDays)]
        DataList = DataList.fillna(0)
        return DataList

    def DrawGraph(self, month, name):
        # output path
        output_name = os.path.join(
            self.output_path, name + "_" + month + ".pdf")

        # arrange data
        SumList = self.MakeList("category", name, month)

        # draw graph
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')
        width = 0.3
        ax = plt.subplot()
        ax.bar(SumList.index, SumList['amount'], width=0.3)
        xfmt = mdates.DateFormatter("%y/%m/%d")
        xloc = mdates.DayLocator()
        ax.xaxis.set_major_locator(xloc)
        ax.xaxis.set_major_formatter(xfmt)
        ax.xaxis.set_tick_params(rotation=45)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(7))
        ax.grid(True)
        plt.xlabel(r"date", fontsize=16)
        plt.ylabel(r"money [yen]", fontsize=16)
        plt.tight_layout()
        plt.show()
        plt.savefig(output_name)

    def RelativePayment(self):
        # output path
        output_name = os.path.join(
            self.output_path, "RelativePayment" + ".pdf")
        AdRepayment = "立替金返済"

        # arrange data
        monthList = []
        y = 2017
        for m in range(9, 13):
            monthList.append(str(str(y) + "-" + str(m).zfill(2)))
        y = 2018
        for m in range(1, int(datetime.now().strftime("%m")) + 1):
            monthList.append(str(str(y) + "-" + str(m).zfill(2)))
        RelaPaymentList = []
        # paymentList = []
        RelaIncomeList = []
        for month in monthList:
            # AdRepayment calc
            SumList = self.MakeList("category", AdRepayment, month)

            # Payment calc
            PayList = self.MakeList("mode", "payment", month)

            # Income calc
            IncomeList = self.MakeList("mode", "income", month)

            RelaPayment = PayList["amount"].sum(
                axis=0) - SumList["amount"].sum(axis=0)
            RelaIncome = IncomeList["amount"].sum(
                axis=0) - SumList["amount"].sum(axis=0)
            # paymentList.append(PayList["amount"].sum(axis=0))
            RelaPaymentList.append(RelaPayment)
            RelaIncomeList.append(RelaIncome)

        # draw graph
        ran = np.arange(len(monthList))
        width = 0.3
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')
        ax = plt.subplot()
        ax.bar(ran, RelaPaymentList, width=width,
               color="blue", label="Relative Payment")
        ax.bar(ran + width, RelaIncomeList, width=width,
               color="red", label="Relative Income")
        plt.xlabel(r"month", fontsize=16)
        plt.ylabel(r"money [yen]", fontsize=16)
        plt.legend(loc="best")
        plt.xticks(ran + width / 2, monthList)
        plt.tight_layout()
        plt.savefig(output_name)
