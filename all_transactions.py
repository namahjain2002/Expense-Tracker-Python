from tkinter import *
from tkinter import ttk
import db_ctrl
import datetime
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure


class AllTransactions:
    def __init__(self, root, main):
        self.main = main
        self.root = root
        self.set_styles()
        matplotlib.rcParams.update({"font.family":self.main.font, "font.size": 10, "text.color":"white"})
        self.tFrame = Frame(self.root, bg=self.main.colors[0])
        self.topFrame = Frame(self.tFrame,bg=self.main.colors[0],height=1000)
        Label(self.topFrame, text="All Transactions",fg=self.main.colors[4],bg=self.main.colors[0],font=(self.main.font, 24),padx=15,pady=10).pack(side=LEFT)
        self.backbtn = Button(self.topFrame,text="Back",font=(self.main.font, 12, "bold"),bd=0, highlightthickness=0, padx=10,pady=10, bg=self.main.colors[1], fg=self.main.colors[0],command=self.showDashboard)
        self.backbtn.pack(side=RIGHT,padx=10)
        self.topFrame.pack(side=TOP, fill=X)

        self.bottomFrame = Frame(self.tFrame,bg=self.main.colors[0],padx=15,pady=10)
        
        self.treeV = ttk.Treeview(self.bottomFrame)
        self.treeV['columns'] = ("Amount", "Type", "Category", "Date","Client", "Contact")
        self.treeV.column("#0", width=0, stretch=NO)
        self.treeV.column("Amount", anchor=W, width=150)
        self.treeV.column("Type", anchor=W, width=40)
        self.treeV.column("Category", anchor=W, width=130)
        self.treeV.column("Date", anchor=W, width=60)
        self.treeV.column("Client", anchor=W)
        self.treeV.column("Contact", anchor=W,width=50)
        self.treeV.heading("Amount",text="Amount", anchor=W)
        self.treeV.heading("Type",text="Type",anchor=W)
        self.treeV.heading("Category",text="Wallet",anchor=W)
        self.treeV.heading("Date",text="Date",anchor=W)
        self.treeV.heading("Client",text="Client",anchor=W)
        self.treeV.heading("Contact",text="Contact",anchor=W)
        self.treeV.pack(fill=BOTH, expand=1, side=TOP)
        self.line = Frame(self.bottomFrame,bg=self.main.colors[4],pady=3,padx=3).pack(side=TOP, pady=5, fill=X)
        self.ef = Frame(self.bottomFrame,bg=self.main.colors[0])
        self.fig = Figure(figsize = (7, 5),dpi = 100)
        self.fig.set_facecolor(self.main.colors[0])
        self.ax = self.fig.add_subplot(111)
        self.chartcanv = FigureCanvasTkAgg(self.fig, self.ef)
        self.canv = self.chartcanv.get_tk_widget()
        self.canv.pack(side=LEFT, expand=1)
        self.canv['bd'] = 0
        self.canv['highlightthickness'] = 0
        self.canv['bg'] = self.main.colors[0]
        Label(self.ef, font=(self.main.font, 18),fg=self.main.colors[4],text="Search by client",bg=self.main.colors[0]).pack(side=LEFT)
        self.search_by_client = Entry(self.ef, bd=0,highlightthickness=0,fg=self.main.colors[2], bg=self.main.colors[3],font=(self.main.font,16))
        self.search_by_client.bind("<KeyRelease>", self.checkMatch)
        self.search_by_client.pack(side=LEFT, padx=20)

        self.ef.pack(side=BOTTOM)
        self.bottomFrame.pack(fill=BOTH, expand=1)
        self.tplot()

    def checkMatch(self,e):
        typed = self.search_by_client.get()
        if typed=='':
            data = self.main.db.get_all_transactions()
        else:
            data = []
            for i in self.main.db.get_all_transactions():
                if typed.lower() in i[4].lower() or typed.lower() in i[3].lower():
                    data.append(i)
        
        self.treeV.delete(*self.treeV.get_children())
        for i in range(len(data)):
            self.treeV.insert(parent='', index='end', iid=i,text='', values=(data[i][1],data[i][0],data[i][2],data[i][3],data[i][4],data[i][5]))


    def tplot(self):
        data = self.main.db.getAmtAndDate()
        sizes = [i[0] for i in data]
        labels = [i[1] for i in data]
        print(sizes, labels)
        self.ax.clear()
        self.ax.pie(sizes, labels = labels, autopct="%1.1f%%", colors=self.main.colors, radius=1.4)
        self.chartcanv.draw_idle()

    def add(self):
        amt = float(self.amt.get())
        name = self.personName.get()
        contact = self.clientContact.get()
        date = datetime.date.today()
        category = self.categories[self.category.current()][0]
        if amt > 0 and len(name) < 20 and len(contact) < 20:
            self.main.db.new_transaction(name, contact, self.trans_type.get(), amt, category, date)
            self.showDashboard()
        

    def set_styles(self):
        self.style = ttk.Style()
        self.style.configure("Treeview",
            background=self.main.colors[0],
            foreground=self.main.colors[3],
            fieldbackground=self.main.colors[1],
            rowheight=25,
            height=100,
            borderwidth=0,
            bd=0,
            highlightthickness=0,
            font=(self.main.font, 12)
        )
        self.style.map("Treeview", 
            background=[('selected', self.main.colors[2])]
        )
        self.style.configure("Treeview.Heading",
        font=(self.main.font, 12),
        background=self.main.colors[3],
        foreground=self.main.colors[0],
        padding=5,
        bd=0,
        highlightthickness=0,
        )
        
        self.style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

    def show(self):
        self.main.mainFrame.pack_forget()
        self.tFrame.pack(fill=BOTH, expand = True)   

        self.main.db.refresh_treev(self.treeV)
        self.tplot() 

    def showDashboard(self):
        self.tFrame.pack_forget()
        self.main.mainFrame.pack(fill=BOTH, expand=1)