#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FileName: 	graph
# CreatedDate:  2018-04-13 14:12:23 +0900
# LastModified: 2020-05-25 08:56:21 +0900
#

import calendar
import datetime as dt
import json
import os
import re
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import ticker


class Graph():
    def __init__(self, Data, Categories):
        # read argument
        self.Data = Data
        self.Data = self.Data.set_index('date')
        self.Categories = Categories

        # set default dict
        self.IncDict = {
            "Income": [11],  # 給与所得
            "Relative Income": [12],  # 立替金返済
            "Bonus": [13],  # 賞与
            "Extraordinary Income": [14],  # 臨時収入
            "Business": [15],  # 事業所得
            "Others": [19]  # その他
        }
        self.PayDict = {
            "Food": [101],  # 食費
            "Daily Goods": [102],  # 日用雑貨
            "Transportation": [103],  # 交通
            "Medical・Insurance": [104],  # 医療・保険
            "Car": [105],  # クルマ
            "Utility": [106],  # 水道・光熱
            "Relationship": [107],  # 交際費
            "Entertainment": [108],  # エンタメ
            "Education": [109],  # 教育・教養
            "Telecommunications": [110],  # 通信
            "Beauty, Clothes": [111],  # 美容・衣服
            "Utility": [112],  # 住まい
            "Tax": [113],  # 税金
            "Large Spending": [114],  # 大型出費
            "Others": [199]  # その他
        }

        # read json file
        DataPath = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                "input/ModeDict.json")
        if os.path.isfile(DataPath):
            with open(DataPath) as f:
                ModeDict = json.load(f)
            self.IncDict = ModeDict['IncDict']
            self.PayDict = ModeDict['PayDict']

        # set monthList(default: one year period)
        self.monthList = []
        dt_now = datetime.now()
        y = dt_now.year - 1
        m = dt_now.month + 1

        def YM2str(year, month):
            return str(str(year) + "-" + str(month).zfill(2))

        for i in range(m, 13):
            self.monthList.append(YM2str(y, i))
        y += 1
        for i in range(1, m):
            self.monthList.append(YM2str(y, i))

        # setting matplotlib
        # plt.rc('text', usetex=True)
        plt.rc('font', family='IPAexGothic')
        plt.rc('xtick', direction='in')
        plt.rc('ytick', direction='in')

        # output path
        self.dir_path = os.path.dirname(os.path.abspath(__file__))
        self.output_path = os.path.join(self.dir_path, "output")

        # set output directory
        try:
            os.mkdir(self.output_path)
        except FileExistsError:
            pass

    def MakeList(self, Mode, CategoryId, Month):
        NumofDays = calendar.monthrange(int(re.sub(r"-.*$", "", Month)),
                                        int(re.sub(r"^.*-", "", Month)))[1]
        DataList = self.Data[self.Data["mode"] == Mode]
        if CategoryId is not None:
            DataList = DataList[DataList["category_id"] == CategoryId]
        DataList = DataList.resample('D').sum()[Month + '-01':Month + '-' +
                                                str(NumofDays)]
        DataList = DataList.fillna(0)
        return DataList

    def MakeModeList(self, Mode):
        # check mode
        if Mode == "income":
            ModeDict = self.IncDict
        elif Mode == "payment":
            ModeDict = self.PayDict
        else:
            print("ERROR: Mode don't exist")

        # variable
        ModeList = None

        # calc
        for month in self.monthList:
            ModeMonth = []
            for ModeCateList in ModeDict.values():
                Amount = 0
                for ModeCateId in ModeCateList:
                    Amount += self.MakeList(Mode, ModeCateId,
                                            month)["amount"].sum(axis=0)
                ModeMonth.append(Amount)
            if ModeList is None:
                ModeList = pd.DataFrame(list([ModeMonth]))
            else:
                ModeList = ModeList.append(list([ModeMonth]))

        # reset columns
        ModeList.columns = ModeDict.keys()

        return ModeList

    def DrawGraph(self, month, CategoryId):
        # variable
        if CategoryId is None:
            CategoryName = "all"
            Mode = "payment"
        else:
            CategoryName = self.Categories[self.Categories["id"] ==
                                           CategoryId]["name"].values[0]
            Mode = self.Categories[self.Categories["id"] ==
                                   CategoryId]["mode"].values[0]

        # output path
        output_name = os.path.join(self.output_path,
                                   "{0}_{1}.pdf".format(CategoryName, month))

        # arrange data
        SumList = self.MakeList(Mode, CategoryId, month)

        # draw graph
        width = 0.3
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.bar(SumList.index, SumList['amount'], width=width)
        xfmt = mdates.DateFormatter("%y/%m/%d")
        xloc = mdates.DayLocator()
        ax.xaxis.set_major_locator(xloc)
        ax.xaxis.set_major_formatter(xfmt)
        ax.xaxis.set_tick_params(rotation=45)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(7))
        # ax.grid(True)
        plt.xlabel("date", fontsize=16)
        plt.ylabel("money [yen]", fontsize=16)
        plt.tight_layout()
        plt.savefig(output_name)
        plt.close(fig)

    def RelativePayment(self):
        # variable
        output_name = os.path.join(self.output_path, "RelativePayment.pdf")
        AdRepaymentId = 12  # Category Id of "立替金返済"

        # arrange data
        RelaPaymentList = []
        RelaIncomeList = []
        for month in self.monthList:
            # AdRepayment calc
            SumList = self.MakeList("income", AdRepaymentId, month)

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
        ran = np.arange(len(self.monthList))
        width = 0.3
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.bar(ran,
               RelaIncomeList,
               width=width,
               color="red",
               label="Relative Income")
        ax.bar(ran + width,
               RelaPaymentList,
               width=width,
               color="blue",
               label="Relative Payment")
        plt.xlabel("month", fontsize=16)
        plt.ylabel("money [yen]", fontsize=16)
        plt.legend(loc="best")
        plt.xticks(ran + width / 2, self.monthList, rotation=45)
        plt.tight_layout()
        plt.savefig(output_name)
        plt.close(fig)

    def MonthlyCategoryGraph(self):
        # output path
        output_name = os.path.join(self.output_path,
                                   "MonthlyCategoryGraph" + ".pdf")

        # arrange data
        IncomeList = self.MakeModeList("income")
        PaymentList = self.MakeModeList("payment")

        # draw graph
        ran = np.arange(len(self.monthList))
        width = 0.3
        fig = plt.figure(figsize=(8, 5))
        ax = fig.add_subplot(1, 1, 1)

        # draw Income graph
        before = np.zeros(len(self.monthList))
        IncLabel = []
        for InKey in self.IncDict.keys():
            IncLabel.append(
                ax.bar(ran,
                       IncomeList[InKey],
                       width=width,
                       label=InKey,
                       bottom=before))
            before = before + IncomeList[InKey].values

        # draw Payment graph
        before = np.zeros(len(self.monthList))
        PayLabel = []
        for PayKey in self.PayDict.keys():
            PayLabel.append(
                ax.bar(ran + width,
                       PaymentList[PayKey],
                       width=width,
                       label=PayKey,
                       bottom=before))
            before = before + PaymentList[PayKey].values

        plt.title("Monthly Category Graph(income and payment)")
        plt.xlabel("month", fontsize=16)
        plt.ylabel("money [yen]", fontsize=16)
        leg1 = plt.legend(handles=IncLabel,
                          bbox_to_anchor=(1.05, 1),
                          loc="upper left",
                          title="income category")
        ax = plt.gca().add_artist(leg1)
        leg2 = plt.legend(handles=PayLabel,
                          bbox_to_anchor=(1.05, 0),
                          loc="lower left",
                          title="payment category")
        plt.xticks(ran + width / 2, self.monthList, rotation=45)
        plt.tight_layout()
        plt.savefig(output_name)
        plt.close(fig)
