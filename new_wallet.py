from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import db_ctrl
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

class NewWalletFrame:
    '''
    Fontend code for new wallet form window
    '''
    def __init__(self, master, main):

        #window controls and ui layout
        self.main = main
        self.master = master

        self.mainFrame = Frame(self.master, bg=self.main.colors[1])
        # self.mainFrame.pack(fill=BOTH, expand = True)

        self.topFrame = Frame(self.mainFrame,bg=self.main.colors[0],height=1000)
        self.cancelBtn = Button(self.topFrame,text="X Cancel",font=(self.main.font, 12, "bold"),bd=0, highlightthickness=0, padx=10,pady=10, bg=self.main.colors[5], fg=self.main.colors[0],command=self.showDash)
        self.cancelBtn.pack(side=RIGHT,padx=10)
        self.addBtn = Button(self.topFrame,text="Done",font=(self.main.font, 12, "bold"),bd=0, highlightthickness=0, padx=10,pady=10, bg=self.main.colors[3], fg=self.main.colors[0],command=self.addWallet)
        self.addBtn.pack(side=RIGHT,padx=10)
        Label(self.topFrame, text="Create New Wallet",fg=self.main.colors[4],bg=self.main.colors[0],font=(self.main.font, 24),padx=15,pady=10).pack(side=LEFT)
        self.topFrame.pack(side=TOP, fill=X)

        self.bottomFrame = Frame(self.mainFrame,bg=self.main.colors[1])

        bg = Image.open("assets/new_wallet.png")
        render = ImageTk.PhotoImage(bg, Image.ANTIALIAS)
        background_label = Label(self.bottomFrame, image=render)
        background_label.img = render
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
        self.subF = Frame(self.bottomFrame,bg=self.main.colors[0])
        Label(self.subF, text="Category",fg=self.main.colors[4],bg=self.main.colors[0],font=(self.main.font,14,"bold")).grid(row=0, column=0,pady=10, padx=40,sticky=E)
        self.category = ttk.Combobox(self.subF,font=(self.main.font,12), values=categories,height=5)
        self.category.current(0)
        self.category.bind('<<ComboboxSelected>>', self.modifyCategory)
        self.category.grid(row=0, column=1, sticky=W)
        
        self.namelabel = Label(self.subF,fg=self.main.colors[4],bg=self.main.colors[0], text="Name ",font=(self.main.font,14,"bold"))
        
        self.name = Entry(self.subF, bd=0,highlightthickness=0,fg=self.main.colors[2], bg=self.main.colors[3],font=(self.main.font,12))

        Label(self.subF,fg=self.main.colors[4], text="Amount *",bg=self.main.colors[0],font=(self.main.font,14,"bold")).grid(row=1, padx=40, column=0,pady=10,sticky=E)
        self.amt = Entry(self.subF, bd=0,highlightthickness=0,fg=self.main.colors[2], bg=self.main.colors[3],font=(self.main.font,12))
        self.amt.grid(row=1,ipady=5, ipadx=5,column=1,pady=20,sticky=W)

        self.status = Label(self.subF, text="",fg=self.main.colors[5],bg=self.main.colors[0], font=(self.main.font,14))
        self.status.grid(row=5,columnspan=2,column=0)
        self.subF.pack(pady=130, padx=120)
        self.bottomFrame.pack(fill=BOTH, expand=1)

    #wallet validation and submition
    def addWallet(self):
        n = categories[self.category.current()]
        if n == categories[-1]:
            n = self.name.get()

        if len(n) > 20:
            self.status["text"] = "length of wallet name should be less than 20"
            return
        if len(n) == 0 or len(self.amt.get()) == 0:
            self.status["text"] = "wallet name and amount can't be empty"
            return
        amt = float(self.amt.get())

        for i in self.main.db.get_all_wallets():
            if n == i[1]:
                self.status["text"] = "wallet with that name already exists"
                return
        self.main.db.new_wallet(amt,n)
        self.mainFrame.pack_forget()
        self.main.rerender()

    def modifyCategory(self,e):
        if self.category.current() == len(categories) - 1:
            self.name.grid(row=2,ipady=5, ipadx=5,column=1,pady=20,sticky=W)
            self.namelabel.grid(row=2, padx=40, column=0,pady=10,sticky=E)
        else:
            self.name.grid_forget()
            self.namelabel.grid_forget()

    def showDash(self):
        self.mainFrame.pack_forget()
        self.main.mainFrame.pack(fill=BOTH, expand=1)