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


def date_now():
    return datetime.now().strftime("%Y-%m-%d")


def draw_graph(data, month, name):
    # output path
    dir_path = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(dir_path, "data")
    output_name = os.path.join(output_path, name + "_" + month + ".pdf")

    # arrange data
    NumofDays = calendar.monthrange(
        int(re.sub(r"-.*$", "", month)), int(re.sub(r"^.*-", "", month)))[1]
    # date_list = pd.date_range(start=month + "-01", periods=NumofDays, freq='D')
    data['date'] = data['date'].astype(datetime)
    data = data.set_index('date')
    sum_list = data[data['category'] == name].resample('D').sum()
    sum_list = sum_list[month + '-01':month + '-' + str(NumofDays)]
    sum_list = sum_list.fillna(0)
    print(str(sum_list["amount"].sum(axis=0)))

    # draw graph
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    ax = plt.subplot()
    ax.plot(sum_list.index, sum_list['amount'], label=name)
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
    plt.savefig(output_name)


def RelativePayment(data):
    # output path
    dir_path = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(dir_path, "data")
    output_name = os.path.join(output_path, "RelativePayment" + ".pdf")
    AdRepayment = "立替金返済"

    # arrange data
    month_list = ["2017-09", "2017-10", "2017-11", "2017-12", "2018-01", "2018-02", "2018-03"]
    RelaPayment_list = []
    payment_list = []
    data['date'] = data['date'].astype(datetime)
    data = data.set_index('date')
    for month in month_list:
        # setting date
        NumofDays = calendar.monthrange(
            int(re.sub(r"-.*$", "", month)), int(re.sub(r"^.*-", "", month)))[1]

        # AdRepayment calc
        sum_list = data[data['category'] == AdRepayment].resample('D').sum()
        sum_list = sum_list[month + '-01':month + '-' + str(NumofDays)]
        sum_list = sum_list.fillna(0)

        # Payment calc
        pay_list = data[data["mode"] == "payment"].resample('D').sum()
        pay_list = pay_list[month + '-01':month + '-' + str(NumofDays)]
        pay_list = pay_list.fillna(0)

        RelaPayment = pay_list["amount"].sum(
            axis=0) - sum_list["amount"].sum(axis=0)
        payment_list.append(pay_list["amount"].sum(axis=0))
        RelaPayment_list.append(RelaPayment)

    # draw graph
    ran = np.arange(len(month_list))
    width = 0.3
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    ax = plt.subplot()
    ax.bar(ran, RelaPayment_list, width=width, color="blue", label="Relative Payment")
    ax.bar(ran + width, payment_list, width=width, color="red", label="payment")
    plt.xlabel(r"month", fontsize=16)
    plt.ylabel(r"money [yen]", fontsize=16)
    plt.legend(loc="best")
    plt.xticks(ran + width / 2, month_list)
    plt.tight_layout()
    plt.savefig(output_name)
