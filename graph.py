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

    def __init__(self, Data, Categories):
        # read Data
        self.Data = Data
        self.Data['date'] = self.Data['date'].astype(datetime)
        self.Data = self.Data.set_index('date')
        self.Categories = Categories
        self.PaymentCategories = list(
            self.Categories[self.Categories["mode"] == "payment"]["name"])
        self.IncomeCategories = list(
            self.Categories[self.Categories["mode"] == "income"]["name"])

        # trans category
        self.IncDict = {
            "Income" : ["給与所得"],
            "Relative Income" : ["立替金返済"],
            "Remittance" : ["仕送り"],
            "Extraordinary Income" : ["臨時収入"],
            "Others" : ["賞与", "事業所得", "その他"]
        }
        self.PayDict = {
            "Food" : ["食費"],
            "Daily Goods" : ["日用雑貨"],
            "Transportation" : ["交通"],
            "Relationship" : ["交際費"],
            "Entertainment" : ["エンタメ"],
            "Education" : ["教育・教養"],
            "Beauty, Clothes" : ["美容・衣服"],
            "Large Spending" : ["大型出費"],
            "Utility" : ["医療・保険", "クルマ", "水道・光熱", "通信", "住まい"],
            "Others" : ["税金", "その他"]
        }

        # setting matplotlib
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')

        # output path
        self.dir_path = os.path.dirname(os.path.abspath(__file__))
        self.output_path = os.path.join(self.dir_path, "data")

    def MakeList(self, Mode, Category, Month):
        NumofDays = calendar.monthrange(
            int(re.sub(r"-.*$", "", Month)), int(re.sub(r"^.*-", "", Month)))[1]
        DataList = self.Data[self.Data["mode"] == Mode]
        if not Category is None:
            DataList = DataList[DataList["category"] == Category]
        DataList = DataList.resample('D').sum()[Month + '-01':Month + '-' + str(NumofDays)]
        DataList = DataList.fillna(0)
        return DataList

    def DrawGraph(self, month, name):
        # output path
        output_name = os.path.join(
            self.output_path, name + "_" + month + ".pdf")

        # arrange data
        SumList = self.MakeList("category", name, month)

        # draw graph
        width = 0.3
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
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
        plt.close(fig)

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
            SumList = self.MakeList("income", AdRepayment, month)

            # Payment calc
            PayList = self.MakeList("payment", None, month)

            # Income calc
            IncomeList = self.MakeList("income", None, month)

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
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
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
        plt.close(fig)

    def MonthlyCategoryGraph(self):
        # output path
        output_name = os.path.join(
            self.output_path, "MonthlyCategoryGraph" + ".pdf")

        # set monthList
        monthList = []
        y = 2017
        for m in range(9, 13):
            monthList.append(str(str(y) + "-" + str(m).zfill(2)))
        y = 2018
        for m in range(1, int(datetime.now().strftime("%m")) + 1):
            monthList.append(str(str(y) + "-" + str(m).zfill(2)))

        # arrange data
        IncomeList = None
        PaymentList = None
        for month in monthList:
            # calc Income
            IncomeMonth = []
            for InCateList in self.IncDict.values():
                Amount = 0
                for InCate in InCateList:
                    Amount += self.MakeList("income", InCate, month)["amount"].sum(axis=0)
                IncomeMonth.append(Amount)
            if IncomeList is None:
                IncomeList = pd.DataFrame(list([IncomeMonth]))
            else:
                IncomeList = IncomeList.append(list([IncomeMonth]))

            # calc Payment
            PaymentMonth = []
            for PayCateList in self.PayDict.values():
                Amount = 0
                for PayCate in PayCateList:
                    Amount += self.MakeList("payment", PayCate, month)["amount"].sum(axis=0)
                PaymentMonth.append(Amount)
            if PaymentList is None:
                PaymentList = pd.DataFrame(list([PaymentMonth]))
            else:
                PaymentList = PaymentList.append(list([PaymentMonth]))

        IncomeList.columns = self.IncDict.keys()
        PaymentList.columns = self.PayDict.keys()

        # draw graph
        ran = np.arange(len(monthList))
        width = 0.3
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        # draw Income graph
        before = np.zeros(len(monthList))
        for InKey in self.IncDict.keys():
            ax.bar(ran + width, IncomeList[InKey], width=width, label=InKey, bottom=before)
            if before.sum() == 0:
                before = IncomeList[InKey]
            else:
                before = before.add(IncomeList[InKey])

        # draw Payment graph
        before = np.zeros(len(monthList))
        for PayKey in self.PayDict.keys():
            ax.bar(ran, PaymentList[PayKey], width=width, label=PayKey, bottom=before)
            if before.sum() == 0:
                before = PaymentList[PayKey]
            else:
                before = before.add(PaymentList[PayKey])

        plt.xlabel(r"month", fontsize=16)
        plt.ylabel(r"money [yen]", fontsize=16)
        plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.xticks(ran + width / 2, monthList)
        plt.tight_layout()
        plt.savefig(output_name)
        plt.close(fig)
