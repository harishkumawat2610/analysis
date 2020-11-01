import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import numpy as np
import pandas as pd
import math
import csv

app = Flask(__name__)

df = []


@app.route("/")
def hello():
    return render_template("main_layout.html", show_hidden=False)


@app.route("/calculate", methods=['POST', 'GET'])
def calculate():
    if request.method == 'POST':
        f = request.files['myFile']
        global df
        df = pd.read_csv(request.files.get('myFile'))
        # f=request.form['myFile']
        # data=[]
        # with open(f) as file:
        #     csvfile=csv.reader(file)
        #     for row in csvfile:
        #         data.append(row)
        # df=pd.DataFrame(data)
        # df = csv.reader(f)
        # print(df)
        cash_deposite = math.ceil(df[df['Description'] == 'Deposited Cash']['Amount'].sum())
        cash_withdrew = (math.ceil(df[df['Description'] == 'Withdrew Cash']['Amount'].sum()) - math.ceil(
            df[df['Description'] == 'Withdraw Canceled']['Amount'].sum()))
        total = cash_withdrew - cash_deposite
        if total < 0:
            wa_lose = total
            wa_profit = 0
        else:
            wa_profit = total
            wa_lose = 0
        investment = math.ceil(df[df['Description'] == 'Joined A Contest']['Amount'].sum()) - math.ceil(
            df[df['Description'] == 'Refunded']['Amount'].sum())
        winnings = math.ceil(df[df['Description'] == 'Won A Contest']['Amount'].sum())
        total_in = winnings - investment
        if total_in < 0:
            in_lose = total_in
            in_profit = 0
        else:
            in_profit = total_in
            in_lose = 0
        tour_list = df['Tour'].value_counts().index.tolist()
        team_list = ["All team"]
        return render_template("main_layout.html", show_hidden=True, cd=cash_deposite, cw=cash_withdrew, i=investment,
                               wi=winnings, wa_lose=wa_lose, wa_profit=wa_profit, in_lose=in_lose, in_profit=in_profit,
                               tour_list=tour_list, team_list=team_list, wallate=True, invest=True)


@app.route("/filter", methods=['POST', 'GET'])
def filter():
    if request.method == 'POST':
    #time_priode = request.form.get('timepriode')
        time_priode=''
        tour_wise = request.form.get('alltour')
        select_match = request.form.get('allteam')
        print("Time : ", str(time_priode), len(time_priode))
        print("tour_wise : ", str(tour_wise), len(tour_wise))
        print("select_math : ", str(select_match), len(select_match))
        global df
        df3 = df.copy()
        df2 = df.copy()
        tour_list = df3['Tour'].value_counts().index.tolist()
        df2 = df2[df2['Tour'] == tour_wise]
        team_list = df2['Round'].value_counts().index.tolist()
        if select_match in team_list:
            pass
        else:
            select_match =''
        #if len(time_priode) == 0 and len(tour_wise) != 0 and len(select_match) == 0:
        if len(time_priode) == 0 and len(select_match) == 0:
            pass
            #df2 = df2[(df['Tour'] == tour_wise) & (df['Round'] == 'select_match')]
        elif len(time_priode) == 0 and len(select_match) != 0:
            df2 = df2[(df['Round'] == select_match)]
        elif len(time_priode) != 0 and len(select_match) == 0:
            df2 = df2[(df['TransactionDate'])]
        elif len(time_priode) != 0 and len(select_match) != 0:
            df2 = df2[(df['TransactionDate'])&(df['Round'] == select_match)]
        investment = math.ceil(df2[df2['Description'] == 'Joined A Contest']['Amount'].sum()) - math.ceil(
            df2[df2['Description'] == 'Refunded']['Amount'].sum())
        winnings = math.ceil(df2[df2['Description'] == 'Won A Contest']['Amount'].sum())
        total_in = winnings - investment
        if total_in < 0:
            in_lose = total_in
            in_profit = 0
        else:
            in_profit = total_in
            in_lose = 0
        print(tour_list)
        print(team_list)
        # if tour_list is not None:
        #     tour_list.remove((str(tour_wise)))
        # if team_list is not None:
        #     tour_list.remove((str(select_match)))
        if time_priode is None:
            time_priode = "Lifetime"
        if tour_wise is None:
            tour_wise = "All Tour"
        if select_match =='':
            select_match = "All teams"
        return render_template("main_layout.html", show_hidden=True, i=investment, wi=winnings, in_lose=in_lose,
                               in_profit=in_profit, wallate=False, invest=True, team_list=team_list,
                               tour_list=tour_list, time_priode=time_priode, tour_wise=tour_wise,
                               select_match=select_match, )


if __name__ == "__main__":
    app.run(debug=True)
