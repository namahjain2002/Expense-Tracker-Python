from tkinter import *
import db_ctrl

class NewWallet:
    '''
    Fontend code for new wallet form window
    '''
    def __init__(self, master, main):

        #window controls and ui layout
        self.main = main
        self.master = master
        self.master.title("New Wallet")
        self.master.geometry("614x579")
        self.master.resizable(0,0)
        self.font = 'ubuntu'
        self.db = db_ctrl.DB_manager(self.main)

        self.mainFrame = Frame(self.master, bg="#d0ded8")
        self.mainFrame.pack(fill=BOTH, expand = True)

        self.topFrame = Frame(self.mainFrame,bg="#85AA9B",height=1000)
        self.cancelBtn = Button(self.topFrame,text="X Cancel",font=(self.font, 12, "bold"),bd=0, highlightthickness=0, padx=10,pady=10, bg="#FF5E5E", fg='#ffffff',command=self.master.destroy)
        self.cancelBtn.pack(side=RIGHT,padx=10)
        self.addBtn = Button(self.topFrame,text="Done",font=(self.font, 12, "bold"),bd=0, highlightthickness=0, padx=10,pady=10, bg="#588B76", fg='#ffffff',command=self.addWallet)
        self.addBtn.pack(side=RIGHT,padx=10)
        Label(self.topFrame, text="Create New Wallet",fg="#ffffff",bg="#85AA9B",font=(self.font, 24),padx=15,pady=10).pack(side=LEFT)
        self.topFrame.pack(side=TOP, fill=X)

        self.bottomFrame = Frame(self.mainFrame,bg="#d0ded8")
        
        Label(self.bottomFrame, text="Wallet Name *",fg="#18392b" ,font=(self.font,16,"bold")).grid(row=0, column=0,pady=10, padx=40,sticky=E)
        self.name = Entry(self.bottomFrame,bd=0,highlightthickness=0,fg="#85aa9b", bg="#ffffff",font=(self.font,14))
        self.name.grid(row=0, column=1,pady=10,ipady=5, ipadx=5,sticky=W)

        Label(self.bottomFrame,fg="#18392b", text="Amount *",font=(self.font,16,"bold")).grid(row=1, padx=40, column=0,pady=10,sticky=E)
        self.amt = Entry(self.bottomFrame, bd=0,highlightthickness=0,fg="#85aa9b", bg="#ffffff",font=(self.font,14))
        self.amt.grid(row=1,ipady=5, ipadx=5,column=1,pady=20,sticky=W)
        
        Label(self.bottomFrame,fg="#18392b", text="Description ",font=(self.font,16,"bold")).grid(row=2, padx=40, column=0,sticky=E)
        self.desc = Text(self.bottomFrame, bd=0,height=12,width=32,highlightthickness=0,font=(self.font,14),fg="#85aa9b",padx=5,pady=5)
        self.desc.grid(row=2,column=1,pady=20,sticky=W)

        self.status = Label(self.bottomFrame, text="",fg="#FF5E5E", font=(self.font,14))
        self.status.grid(row=3,columnspan=2,column=0)
        self.bottomFrame.pack(fill=BOTH)

    #wallet validation and submition
    def addWallet(self):
        n = self.name.get()
        desc = self.desc.get("1.0", END)

        if len(n) > 20:
            self.status["text"] = "length of wallet name should be less than 20"
            return
        if len(n) == 0 or len(self.amt.get()) == 0 or len(desc) == 0:
            self.status["text"] = "wallet name and amount can't be empty"
            return
        amt = float(self.amt.get())

        for i in self.db.get_all_wallets():
            if n == i[1]:
                self.status["text"] = "wallet with that name already exists"
                return
        self.db.new_wallet(amt,n,desc)
        self.main.rerender()
        self.master.destroy()
