from tkinter import *
import sqlite3
from new_wallet import *
from db_ctrl import *


#main class
class Main:
    '''
    Main app class
    '''
    def __init__(self,root):
        #window methods
        self.root = root
        self.root.resizable(0,0)
        self.root.title("Expense Tracker")
        self.root.geometry("1024x576")
        self.db = DB_manager(self)
        self.font = 'ubuntu'
        self.mainFrame = Frame(self.root, bg="#d0ded8")
        self.mainFrame.pack(fill=BOTH, expand = True)
        self.makeHome()

    def showWallets(self):
        #show wallets on the landing page
        for i in self.db.get_all_wallets():
            name = i[1]
            f = Frame(self.bottomFrame, bg="#ffffff", height=57, width=883)
            f.pack_propagate(0)
            Label(f, text=i[1], font=(self.font,16), bg="#ffffff",padx=50,fg="#18392b").pack(side=LEFT)
            Label(f, text="+"+str(i[0]), font=(self.font,12),padx=30, bg="#ffffff", fg="#588b76").pack(side=LEFT)
            Button(f,text="Open",font=(self.font, 12, "bold"),bd=0,highlightthickness=0, padx=25,pady=10, bg="#588B76", fg='#ffffff').pack(side=RIGHT,padx=5)
            Button(f,text="Delete",font=(self.font, 12, "bold"),bd=0, highlightthickness=0,command=lambda name=name: self.db.deleteWallet(name),padx=20,pady=10, bg="#FF5E5E", fg='#ffffff').pack(side=RIGHT,padx=5)
            f.pack(padx=70, pady=25, side=TOP)

    def new_wallet(self):
        #new wallet form window
        root = Tk()
        NewWallet(root,self)
        root.mainloop()

    def rerender(self):
        #rerender all wallets
        for widget in self.bottomFrame.winfo_children():
            widget.destroy()
        self.showWallets()    
        

    def makeHome(self):
        #ui for title 
        self.topFrame = Frame(self.mainFrame,bg="#85AA9B",height=1000)
        Label(self.topFrame, text="Expense Tracker",fg="#ffffff",bg="#85AA9B",font=(self.font, 24),padx=15,pady=10).pack(side=LEFT)
        self.addBtn = Button(self.topFrame,command=self.new_wallet,text=" + New Wallet",font=(self.font, 12, "bold"),bd=0, highlightthickness=0, padx=10,pady=10, bg="#588B76", fg='#ffffff')
        self.addBtn.pack(side=RIGHT,padx=10)
        
        self.topFrame.pack(side=TOP, fill=X)
        self.bottomFrame = Frame(self.mainFrame,bg="#d0ded8")
        self.showWallets()
        self.bottomFrame.pack(fill=BOTH)

#run 
r = Tk()
m = Main(r)
r.mainloop()