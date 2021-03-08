from tkinter import *
import db_ctrl
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

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
        self.tFrame = Frame(self.root, bg=self.main.colors[1])
        self.topFrame = Frame(self.tFrame,bg=self.main.colors[2],height=1000)
        self.wallet_name = Label(self.topFrame, text="",fg=self.main.colors[0],bg=self.main.colors[2],font=(self.main.font, 24),padx=15,pady=10)
        self.wallet_name.pack(side=LEFT)
        self.dashbtn = Button(self.topFrame,text="Dashboard",font=(self.main.font, 12, "bold"),bd=0, highlightthickness=0, padx=10,pady=10, bg="#588B76", fg='#ffffff',command=self.showDashboard)
        self.dashbtn.pack(side=RIGHT,padx=10)
        self.editbtn = Button(self.topFrame,text="Edit",font=(self.main.font, 12, "bold"),bd=0, highlightthickness=0, padx=10,pady=10, bg="#588B76", fg='#ffffff')
        self.editbtn.pack(side=RIGHT,padx=10)
        self.topFrame.pack(side=TOP, fill=X)


        self.bottomFrame = Frame(self.tFrame,bg=self.main.colors[1],padx=15,pady=10)
        self.leftbf = Frame(self.bottomFrame, bg=self.main.colors[1],width=650)
        self.currentBal = Label(self.leftbf, font=(self.main.font, 50, 'bold'),fg=self.main.colors[4],text="+3000",bg=self.main.colors[1])
        self.currentBal.grid(row=0, column=0, sticky=W)

        labelf = Frame(self.leftbf, padx=10)
        self.expenseLabel = Label(labelf, text="-2000",fg=self.main.colors[5],bg=self.main.colors[1],font=(self.main.font, 18),pady=10)
        self.expenseLabel.pack(side=LEFT)
        self.credits = Label(labelf, text="4000",fg=self.main.colors[3],bg=self.main.colors[1],font=(self.main.font, 18),padx=50,pady=10)
        self.credits.pack()
        labelf.grid(row=1,column=0, sticky=W)

        self.transactionBtn = Button(self.leftbf,text="View Transactions",font=(self.main.font, 12, "bold"),bd=0, highlightthickness=0, padx=50,pady=10, bg="#588B76", fg='#ffffff', command =self.main.trans_frame.show)
        self.transactionBtn.grid(row=2, column=0, sticky=W,pady=20)

        self.descLabel = Label(self.leftbf, text='', font=(self.main.font,14), fg=self.main.colors[3])
        self.descLabel.grid(sticky=W, row=3, column=0)

        self.leftbf.pack(side=LEFT,fill=BOTH, expand=1)

        self.rightbf = Frame(self.bottomFrame, bg=self.main.colors[1])

        self.rightbf.pack(side=RIGHT)
        self.fig = Figure(figsize = (7, 5),
                 dpi = 100)
        self.fig.set_facecolor(self.main.colors[1])
        self.ax = self.fig.add_subplot(111)
        self.chartcanv = FigureCanvasTkAgg(self.fig, self.bottomFrame)
        self.canv = self.chartcanv.get_tk_widget()
        self.canv.pack(side=RIGHT, fill=BOTH, expand=1)
        self.canv['bd'] = 0
        self.canv['highlightthickness'] = 0
        self.canv['bg'] = self.main.colors[1]
        self.bottomFrame.pack(fill=BOTH)

    def tplot(self):
        self.fig.clear(True)
        data = self.main.db.get_dncate(self.name)
        print(data)
        names = [i[0] for i in data]
        values = [i[1] for i in data]
        self.ax = self.fig.add_subplot(111)
        self.ax.pie(values, radius=1, labels=names,autopct='%0.2f%%', colors=plot_colors)
        #self.ax.bar(names,values, color=plot_colors, ecolor=self.main.colors[-1], edgecolor = plot_colors)


    def show(self, name):
        self.main.mainFrame.pack_forget()
        self.tFrame.pack(fill=BOTH, expand = True)
        self.wallet_name['text'] = name
        self.name = name
        wDetails = self.main.db.get_wallet(name)
        (creds, debts) = self.main.db.get_cnd(name)
        self.credits["text"] = '+'+str(wDetails[0][0] + creds)
        self.descLabel['text'] = str(wDetails[0][2])
        self.currentBal['text'] = str(wDetails[0][0] + creds - debts)
        self.expenseLabel['text'] = '-'+str(debts)
        self.main.trans_frame.name = name
        self.tplot()

    def showDashboard(self):
        self.tFrame.pack_forget()
        self.main.mainFrame.pack()