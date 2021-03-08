'''
Denarii
'''

from tkinter import *
import sqlite3
from new_wallet import *
from db_ctrl import *
from wallet_frame import WalletFrame
from transaction_frame import *

#main class
class Main:
    '''
    Main app class
    '''
    def __init__(self,root):
        #window methods
        self.colors = ['#ffffff','#d0ded8','#85aa9b','#588b76','#18392b','#FF5E5E']
        self.root = root
        self.root.resizable(0,0)
        self.root.title("Expense Tracker")
        self.root.geometry("1024x576")
        self.db = DB_manager(self)
        self.font = 'ubuntu'
        self.mainFrame = Frame(self.root, bg=self.colors[1])
        self.mainFrame.pack(fill=BOTH, expand = True)
        self.trans_frame = TransactionFrame(self.root, self)
        self.wallet_frame = WalletFrame(self.root, self)
        self.new_wallet_frame = NewWalletFrame(self.root, self)
        self.makeHome()

    def showWallets(self):
        #show wallets on the landing page
        wallets = self.db.get_all_wallets()
        if wallets:

            for i in wallets:
                name = i[1]
                f = Frame(self.bottomFrame, bg=self.colors[0], height=57, width=883)
                f.pack_propagate(0)
                Label(f, text=i[1], font=(self.font,16), bg=self.colors[0],padx=50,fg=self.colors[4]).pack(side=LEFT)
                Label(f, text="+"+str(self.db.get_bal(i[1])), font=(self.font,12),padx=30, bg=self.colors[0], fg=self.colors[3]).pack(side=LEFT)
                Button(f,text="Open",font=(self.font, 12, "bold"),bd=0,highlightthickness=0, padx=25,pady=10, bg=self.colors[3], fg=self.colors[0],command = lambda name=name: self.wallet_frame.show(name) ).pack(side=RIGHT,padx=5)
                Button(f,text="Delete",font=(self.font, 12, "bold"),bd=0, highlightthickness=0,command=lambda name=name: self.db.deleteWallet(name),padx=20,pady=10, bg=self.colors[5], fg=self.colors[0]).pack(side=RIGHT,padx=5)
                f.pack(padx=70, pady=25, side=TOP)
        else:
            Label(self.bottomFrame, text='"You have no wallets :("', font=(self.font,24),padx=50,fg=self.colors[5]).pack(pady=100)

    def new_wallet(self):
        #new wallet form window
        self.mainFrame.pack_forget()
        self.new_wallet_frame.mainFrame.pack(fill=BOTH, expand=1)

    def rerender(self):
        #rerender all wallets
        self.mainFrame.pack(fill=BOTH, expand=1)
        for widget in self.bottomFrame.winfo_children():
            widget.destroy()
        self.showWallets()


    def makeHome(self):
        #ui for title
        self.topFrame = Frame(self.mainFrame,bg=self.colors[2],height=1000)
        Label(self.topFrame, text="Expense Tracker",fg=self.colors[0],bg=self.colors[2],font=(self.font, 24),padx=15,pady=10).pack(side=LEFT)
        self.addBtn = Button(self.topFrame,command=self.new_wallet,text=" + New Wallet",font=(self.font, 12, "bold"),bd=0, highlightthickness=0, padx=10,pady=10, bg=self.colors[3], fg=self.colors[0])
        self.addBtn.pack(side=RIGHT,padx=10)

        self.topFrame.pack(side=TOP, fill=X)
        self.bottomFrame = Frame(self.mainFrame,bg=self.colors[1])
        self.showWallets()
        self.bottomFrame.pack(fill=BOTH)

#run
r = Tk()
m = Main(r)
r.mainloop()