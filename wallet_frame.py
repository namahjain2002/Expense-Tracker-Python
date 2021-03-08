from tkinter import *
import db_ctrl
from matplotlib import pyplot as plt 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure


class WalletFrame:
    def __init__(self, root, main):
        self.main = main
        self.name = ''
        self.root = root
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
        
        self.bottomFrame.pack(fill=BOTH)

    def tplot(self):
        data = self.main.db.get_dncate(self.name)
        fig = Figure(figsize = (5, 5), 
                 dpi = 100) 
  
        # list of squares 
        y = [i**2 for i in range(101)] 
    
        # adding the subplot 
        plot1 = fig.add_subplot(111) 
    
        # plotting the graph 
        plot1.plot(y) 
    
        # creating the Tkinter canvas 
        # containing the Matplotlib figure 
        canvas = FigureCanvasTkAgg(fig, 
                                master = self.bottomFrame)   
        canvas.draw() 
    
        # placing the canvas on the Tkinter window 
        canvas.get_tk_widget().pack() 
    
        # creating the Matplotlib toolbar 
        toolbar = NavigationToolbar2Tk(canvas, 
                                    self.main\ \) 
        toolbar.update()
    
        # placing the toolbar on the Tkinter window 
        canvas.get_tk_widget().pack()
    
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