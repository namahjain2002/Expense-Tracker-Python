'''
Denarii
'''

from tkinter import *
import sqlite3
from new_wallet import *
from db_ctrl import *
from wallet_frame import WalletFrame
from add_transaction import *
from all_transactions import *
from PIL import Image, ImageTk

#main class
class Main:
    '''
    Main app class
    '''
    def __init__(self,root):
        #window methods082a44
        #self.colors = ['#ffffff','#d0ded8','#85aa9b','#588b76','#18392b','#FF5E5E']
        self.colors = ['#082a44','#f47279','#2673cf','#ffd5d3','#fbe675','#FF5E5E']
        self.root = root
        self.root.configure(background=self.colors[0])
        self.root.resizable(0,0)
        self.root.title("Denarii - Your daily expense tracker")
        self.root.geometry("1024x576")
        photo = PhotoImage(file = "assets/icon.png")
        self.root.iconphoto(False, photo)
        self.db = DB_manager(self)
        self.font = 'Comic Sans MS'
        self.set_styles()
        splashscr = Image.open("assets/splash_screen.png")
        sprender = ImageTk.PhotoImage(splashscr, Image.ANTIALIAS)
        self.splash = Label(self.root, image = sprender, bg=self.colors[0])
        self.splash.img = sprender
        self.splash.place(x=0,y=0,relwidth=1, relheight=1)
        self.splash.bind("<Button-1>", self.showmain)
        self.mainFrame = Frame(self.root, bg=self.colors[1])
        # self.mainFrame.pack(fill=BOTH, expand = True)
        self.add_trans_frame = AddTransaction(self.root, self)
        self.wallet_frame = WalletFrame(self.root, self)
        self.new_wallet_frame = NewWalletFrame(self.root, self)
        self.all_trans_frame = AllTransactions(self.root ,self)
        bg = Image.open("assets/Dashboard.png")
        self.render = ImageTk.PhotoImage(bg, Image.ANTIALIAS) 
        self.makeHome()

    
    def set_styles(self):
        self.style = ttk.Style()
        self.style.configure("TCombobox", 
            selectbackground=self.colors[1],
            fieldbackground=self.colors[0],
            background=self.colors[0],
            foreground=self.colors[2],
            selectforeground = self.colors[2],
            borderwidth=0,
            height=450
        )
        self.style.configure("Treeview",
            background=self.colors[1],
            foreground=self.colors[4],
            fieldbackground=self.colors[1],            
            rowheight=30,
            borderwidth=0,
            bd=0,
            highlightthickness=0,
            font=(self.font, 12)
        )
        self.style.map("Treeview", 
            background=[('selected', self.colors[2])]
        )
        self.style.configure("Treeview.Heading",
            font=(self.font, 14),
            background=self.colors[3],
            foreground=self.colors[0],
            padding=5,
            bd=0,
            highlightthickness=0
        )
        
        self.style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        self.style.theme_use("default")
        self.root.option_add('*TCombobox*Listbox.background', self.colors[0])
        self.root.option_add('*TCombobox*Listbox.foreground', self.colors[3])
    def showmain(self, e):
        self.mainFrame.pack(fill=BOTH, expand = True)
        self.splash.place_forget()

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
            Label(self.bottomFrame, text='"You have no wallets :("', font=(self.font,24),padx=50,fg=self.colors[5],bg=self.colors[0]).pack(pady=100)

    def new_wallet(self):
        #new wallet form window
        self.mainFrame.pack_forget()
        self.new_wallet_frame.mainFrame.pack(fill=BOTH, expand=1)

    def rerender(self):
        #rerender all wallets
        self.mainFrame.pack(fill=BOTH, expand=1)

        for widget in self.bottomFrame.winfo_children():
            widget.destroy()
        self.background_label = Label(self.bottomFrame, image=self.render)
        self.background_label.img = self.render
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.showWallets()



    def makeHome(self):
        #ui for title
        self.topFrame = Frame(self.mainFrame,bg=self.colors[0],height=1000)
        Label(self.topFrame, text="Denarii",fg=self.colors[4],bg=self.colors[0],font=(self.font, 24),padx=15,pady=10).pack(side=LEFT)
        self.newTransaction = Button(self.topFrame,command=self.add_trans_frame.show,text=" + New Transactions",font=(self.font, 12, "bold"),bd=0, highlightthickness=0, padx=10,pady=10, bg=self.colors[3], fg=self.colors[0])
        self.newTransaction.pack(side=RIGHT,padx=10)
        self.addBtn = Button(self.topFrame,command=self.new_wallet,text=" + New Wallet",font=(self.font, 12, "bold"),bd=0, highlightthickness=0, padx=10,pady=10, bg=self.colors[3], fg=self.colors[0])
        self.addBtn.pack(side=RIGHT,padx=10)
        self.allTransactions = Button(self.topFrame,command=self.all_trans_frame.show,text="All Transactions",font=(self.font, 12, "bold"),bd=0, highlightthickness=0, padx=10,pady=10, bg=self.colors[3], fg=self.colors[0])
        self.allTransactions.pack(side=RIGHT,padx=10)

        self.topFrame.pack(side=TOP, fill=X)
        self.bottomFrame = Frame(self.mainFrame,bg=self.colors[1])
        self.background_label = Label(self.bottomFrame, image=self.render)
        self.background_label.img = self.render
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
        self.showWallets()
        self.bottomFrame.pack(fill=BOTH, expand=1)
        
#run
r = Tk()
m = Main(r)
r.mainloop()