from tkinter import *
from tkinter import ttk
import db_ctrl
import datetime
from PIL import Image, ImageTk

class AddTransaction:
    def __init__(self, root, main):
        self.main = main
        self.root = root
        self.trans_type = StringVar()
        self.trans_type.set('C')
        self.categories = self.main.db.get_categories()
        self.tFrame = Frame(self.root, bg=self.main.colors[0])
        self.topFrame = Frame(self.tFrame,bg=self.main.colors[0],height=1000)
        Label(self.topFrame, text="Add New Transaction",fg=self.main.colors[4],bg=self.main.colors[0],font=(self.main.font, 24),padx=15,pady=10).pack(side=LEFT)
        self.backbtn = Button(self.topFrame,text="Back",font=(self.main.font, 12, "bold"),bd=0, highlightthickness=0, padx=10,pady=10, bg=self.main.colors[3], fg=self.main.colors[0],command=self.showDashboard)
        self.backbtn.pack(side=RIGHT,padx=10)
        self.addbtn = Button(self.topFrame,text="Add",font=(self.main.font, 12, "bold"),bd=0, highlightthickness=0, padx=10,pady=10, bg=self.main.colors[3], fg=self.main.colors[0],command=self.add)
        self.addbtn.pack(side=RIGHT,padx=10)
        
        self.topFrame.pack(side=TOP, fill=X)

        self.bottomFrame = Frame(self.tFrame,bg=self.main.colors[1])
        bg = Image.open("assets/add_transaction.png")
        render = ImageTk.PhotoImage(bg, Image.ANTIALIAS)
        background_label = Label(self.bottomFrame, image=render)
        background_label.img = render
        background_label.place(x=0, y=0,relwidth=1, relheight=1)
        self.form = Frame(self.bottomFrame,bg=self.main.colors[0])
        
        Label(self.form,fg=self.main.colors[4],bg=self.main.colors[0], text="Amount ",font=(self.main.font,14)).grid(row=0, padx=40, column=0,pady=10,sticky=W)
        self.amt = Entry(self.form, bd=0,highlightthickness=0,fg=self.main.colors[2], bg=self.main.colors[3],font=(self.main.font,12))
        self.amt.grid(row=0,ipady=5, ipadx=5,column=1,pady=20,sticky=W)

        Radiobutton(self.form, text="Credit",bg=self.main.colors[0],bd=0,highlightthickness=0, variable=self.trans_type, value="C",font=(self.main.font,14),fg=self.main.colors[4]).grid(row=1,column=0, sticky=E)
        Radiobutton(self.form, text="Debit",bg=self.main.colors[0],bd=0,highlightthickness=0, variable=self.trans_type, value="D",font=(self.main.font,14),fg=self.main.colors[4]).grid(row=1,column=1, sticky=E)

        Label(self.form,fg=self.main.colors[4],bg=self.main.colors[0], text="Client Name",font=(self.main.font,14)).grid(row=2, padx=40, column=0,pady=10,sticky=W)
        self.personName = Entry(self.form, bd=0,highlightthickness=0,fg=self.main.colors[2], bg=self.main.colors[3],font=(self.main.font,12))
        self.personName.grid(row=2,ipady=5, ipadx=5,column=1,pady=20,sticky=W)
        
        Label(self.form,fg=self.main.colors[4],bg=self.main.colors[0], text="Client Contact",font=(self.main.font,14)).grid(row=3, padx=40, column=0,pady=10,sticky=W)
        self.clientContact = Entry(self.form, bd=0,highlightthickness=0,fg=self.main.colors[2], bg=self.main.colors[3],font=(self.main.font,12))
        self.clientContact.grid(row=3,ipady=5, ipadx=5,column=1,pady=20,sticky=W)
        
        Label(self.form,text="Wallet",bg=self.main.colors[0], font=(self.main.font,14),fg=self.main.colors[4]).grid(row=4,column=0,padx=40,pady=10,sticky=W)
        self.category = ttk.Combobox(self.form,font=(self.main.font,12), values=self.categories,height=5)
        if self.categories:
            self.category.current(0)
        self.category.grid(row=4,ipady=5,column=1,pady=20,sticky=W)
        

        self.form.pack(pady=80)

        self.bottomFrame.pack(fill=BOTH, expand=1)

    def add(self):
        amt = float(self.amt.get())
        name = self.personName.get()
        contact = self.clientContact.get()
        date = datetime.date.today()
        category = self.categories[self.category.current()][0]
        if amt > 0 and len(name) < 20 and len(contact) < 20:
            self.main.db.new_transaction(name, contact, self.trans_type.get(), amt, category, date)
            self.showDashboard()

    def show(self):
        self.main.mainFrame.pack_forget()
        self.tFrame.pack(fill=BOTH, expand = True)
        self.categories = self.main.db.get_categories() 
        self.category['values'] = self.categories       
        

    def showDashboard(self):
        self.tFrame.pack_forget()
        self.main.rerender()
