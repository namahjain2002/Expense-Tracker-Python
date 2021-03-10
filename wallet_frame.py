from tkinter import *
import db_ctrl
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import datetime

plot_colors = [
    '#58c876',
    '#85aa9B',
    '#85c89b',
    '#d2f7de',
    '#b8d4c1',
    '#72b086',
    '#a1a1a1',
    '#bed1bf'
]

class WalletFrame:
    def __init__(self, root, main):
        self.main = main
        self.name = ''
        self.root = root
        matplotlib.rcParams.update({"font.family":self.main.font, "font.size": 12, "font.weight": "medium"})
        self.tFrame = Frame(self.root, bg=self.main.colors[0])
        self.topFrame = Frame(self.tFrame,bg=self.main.colors[0],height=1000)
        self.wallet_name = Label(self.topFrame, text="",fg=self.main.colors[4],bg=self.main.colors[0],font=(self.main.font, 24),padx=15,pady=10)
        self.wallet_name.pack(side=LEFT)
        self.dashbtn = Button(self.topFrame,text="Dashboard",font=(self.main.font, 12, "bold"),bd=0, highlightthickness=0, padx=10,pady=10, bg=self.main.colors[5], fg=self.main.colors[0],command=self.showDashboard)
        self.dashbtn.pack(side=RIGHT,padx=10)
        self.topFrame.pack(side=TOP, fill=X)

        self.bottomFrame = Frame(self.tFrame,bg=self.main.colors[0],padx=15,pady=10)
        self.topf = Frame(self.bottomFrame, bg=self.main.colors[0])
        self.currentBal = Label(self.topf, font=(self.main.font, 30, 'bold'),fg=self.main.colors[4],text="+3000",bg=self.main.colors[0])
        self.currentBal.pack(side=LEFT)

        self.expenseLabel = Label(self.topf, text="-2000",fg=self.main.colors[5],bg=self.main.colors[0],font=(self.main.font, 18),pady=10)
        self.expenseLabel.pack(side=LEFT, padx=40)
        self.credits = Label(self.topf, text="4000",fg=self.main.colors[3],bg=self.main.colors[0],font=(self.main.font, 18),padx=50,pady=10)
        self.credits.pack(side=LEFT)

        self.topf.pack(side=TOP,fill=X, expand=1)
        
        self.line = Frame(self.bottomFrame,bg=self.main.colors[4],pady=3,padx=3).pack(side=TOP, pady=5, fill=X)

        self.botf = Frame(self.bottomFrame, bg=self.main.colors[0])
        #canvas and transaction table
        
        self.fig = Figure(figsize = (7, 5),dpi = 100)
        self.fig.set_facecolor(self.main.colors[0])
        self.ax = self.fig.add_subplot(111)
        self.chartcanv = FigureCanvasTkAgg(self.fig, self.botf)
        self.canv = self.chartcanv.get_tk_widget()
        self.canv.pack(side=RIGHT, fill=BOTH, expand=1)
        self.canv['bd'] = 0
        self.canv['highlightthickness'] = 0
        self.canv['bg'] = self.main.colors[0]
        self.botf.pack(side=BOTTOM, fill=BOTH, expand=1)
        self.bottomFrame.pack(fill=BOTH,side=TOP)

    def tplot(self):
        self.fig.clear(True)
        data = self.main.db.get_amtanddate(self.name)
        raw_dates1 = [i[1] for i in data[1]]
        values1 = [i[0] for i in data[1]]
        dates1 = [datetime.datetime.strptime(date, '%Y-%m-%d').date() for date in raw_dates1]
        raw_dates2 = [i[1] for i in data[0]]
        values2 = [i[0] for i in data[0]]
        dates2 = [datetime.datetime.strptime(date, '%Y-%m-%d').date() for date in raw_dates1]
        print(dates2, dates1)
        self.ax = self.fig.add_subplot(111)
        self.ax.plot(dates1,values1,color='r')
        # self.ax.plot(dates2,values2,color='g')
        
        #self.ax.plot(dates2,values2)


    def show(self, name):
        self.main.mainFrame.pack_forget()
        self.tFrame.pack(fill=BOTH, expand = True)
        self.wallet_name['text'] = name
        self.name = name
        wDetails = self.main.db.get_wallet(name)
        (creds, debts) = self.main.db.get_cnd(name)
        self.credits["text"] = '+'+str(wDetails[0][0] + creds)
        self.currentBal['text'] = str(wDetails[0][0] + creds - debts)
        self.expenseLabel['text'] = '-'+str(debts)
        self.tplot()

    def showDashboard(self):
        self.tFrame.pack_forget()
        self.main.mainFrame.pack(fill=BOTH, expand=1)