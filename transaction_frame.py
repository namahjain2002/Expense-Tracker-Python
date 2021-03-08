from tkinter import *
from tkinter import ttk
import db_ctrl
import datetime

categories = [
    'Food',
    'Stationary',
    'Transportation',
    'Utilities',
    'Insurance',
    'Medical & Healthcare',
    'Investment',
    'Debt',
    'Saving',
    'Personal',
    'Entertainment',
    'Miscellaneous'
]


class TransactionFrame:
    def __init__(self, root, main):
        self.main = main
        self.root = root
        self.trans_type = StringVar()
        self.trans_type.set('C')
        self.tFrame = Frame(self.root, bg=self.main.colors[1])
        self.name = 'name'
        self.topFrame = Frame(self.tFrame,bg=self.main.colors[2],height=1000)
        self.wallet_name = Label(self.topFrame, text="",fg=self.main.colors[0],bg=self.main.colors[2],font=(self.main.font, 24),padx=15,pady=10)
        self.wallet_name.pack(side=LEFT)
        self.backbtn = Button(self.topFrame,text="Back",font=(self.main.font, 12, "bold"),bd=0, highlightthickness=0, padx=10,pady=10, bg=self.main.colors[3], fg=self.main.colors[0],command=self.showDashboard)
        self.backbtn.pack(side=RIGHT,padx=10)
        self.topFrame.pack(side=TOP, fill=X)

        self.bottomFrame = Frame(self.tFrame,bg=self.main.colors[1],padx=15,pady=10)
        self.sidepane = Frame(self.bottomFrame, bg=self.main.colors[1])
        Label(self.sidepane,text="Value", font=(self.main.font,14),fg=self.main.colors[4]).grid(row=0,column=0, sticky=W)
        self.trans_val = Entry(self.sidepane,fg=self.main.colors[2],font=(self.main.font,12),bd=0,highlightthickness=0)
        self.trans_val.grid(row=0,column=1, padx=10, pady=10, sticky=W)

        Label(self.sidepane,text="Category", font=(self.main.font,14),fg=self.main.colors[4]).grid(row=1,column=0, sticky=W)
        self.category = ttk.Combobox(self.sidepane,font=(self.main.font,12), values=categories,height=5)
        self.category.current(len(categories)-1)
        self.category.grid(row=1,column=1, padx=10, pady=10, sticky=W)

        self.creditR = Radiobutton(self.sidepane, text="Credit", variable=self.trans_type, value="C",font=(self.main.font,14),fg=self.main.colors[4])
        self.creditR.grid(row=2,column=0, sticky=W)
        self.creditR = Radiobutton(self.sidepane, text="Debit", variable=self.trans_type, value="D",font=(self.main.font,14),fg=self.main.colors[4])
        self.creditR.grid(row=2,column=1, sticky=W)
        self.transactionBtn = Button(self.sidepane,text="Add Transaction",font=(self.main.font, 12, "bold"),bd=0, highlightthickness=0, padx=50,pady=10, bg="#588B76", fg='#ffffff',command=self.addtrans)
        self.transactionBtn.grid(row=3, column=0,columnspan=2,sticky=W,pady=20)
        self.sidepane.pack(fill=BOTH, side=LEFT)
        
        self.treeV = ttk.Treeview(self.bottomFrame)
        self.treeV['columns'] = ("Amount", "Type", "Category", "Date")
        self.treeV.column("#0", width=0, stretch=NO)
        self.treeV.column("Amount", anchor=W)
        self.treeV.column("Type", anchor=W)
        self.treeV.column("Category", anchor=W)
        self.treeV.column("Date", anchor=W)
        self.treeV.heading("Amount",text="Amount", anchor=W)
        self.treeV.heading("Type",text="Type",anchor=W)
        self.treeV.heading("Category",text="Category",anchor=W)
        self.treeV.heading("Date",text="Date",anchor=W)
        # self.main.db.refresh_treev(self.treeV)
        self.treeV.pack(fill=BOTH, expand=1)
        self.bottomFrame.pack(fill=BOTH)
        self.set_styles()

    def addtrans(self):
        amt = int(self.trans_val.get())
        category = categories[self.category.current()]
        typ = self.trans_type.get()
        if amt > 0:
            self.main.db.new_transaction(self.name, typ, amt, category, datetime.date.today())
            self.trans_val.delete(0, END)
            self.main.db.refresh_treev(self.treeV, self.name)
        

    def set_styles(self):
        self.style = ttk.Style()
        self.style.configure("TCombobox", 
            selectbackground=self.main.colors[1],
            fieldbackground=self.main.colors[0],
            background=self.main.colors[0],
            foreground=self.main.colors[2],
            selectforeground = self.main.colors[2],
            borderwidth=0,
            height=450
        )
        self.style.configure("Treeview",
            background=self.main.colors[0],
            foreground=self.main.colors[4],
            fieldbackground=self.main.colors[1],
            rowheight=30,
            borderwidth=0
        )
        self.style.map("Treeview", 
            background=[('selected', self.main.colors[2])]
        )
        self.root.option_add('*TCombobox*Listbox.font', (self.main.font,12))
        self.root.option_add('*TCombobox*Listbox.background', self.main.colors[0])
        self.root.option_add('*TCombobox*Listbox.foreground', self.main.colors[2])
    

    def show(self):
        self.main.wallet_frame.tFrame.pack_forget()
        self.tFrame.pack(fill=BOTH, expand = True)
        self.wallet_name['text'] = self.name
        self.main.db.refresh_treev(self.treeV, self.name)
        

    def showDashboard(self):
        self.tFrame.pack_forget()
        self.main.wallet_frame.show(self.name)