import sqlite3


class DB_manager:
    '''
    Manages all database operations
    '''
    #initialise and setup tables
    def __init__(self, main):
        self.main = main
        conn = sqlite3.connect("Main.db")
        c = conn.cursor()
        c.execute("create table if not exists wallets(amount NUMERIC, name VARCHAR(20), desc TEXT)")
        c.execute("create table if not exists transactions(wallet_name VARCHAR(20), type VARCHAR(20), amount NUMERIC, category VARCHAR(20), date DATE)")
        conn.commit()
        c.close()
        conn.close()

    #create a new wallet
    def new_wallet(self,amt,n,desc):
        conn = sqlite3.connect("Main.db")
        c = conn.cursor()
        c.execute("insert into wallets values({},'{}','{}')".format(amt,n,desc))
        conn.commit()
        c.close()
        conn.close()

    #delete a wallet with given name
    def deleteWallet(self, name):
        conn = sqlite3.connect("Main.db")
        c = conn.cursor()
        c.execute("delete from wallets where name='{}'".format(name))
        c.execute("delete from transactions where wallet_name='{}'".format(name))
        conn.commit()
        c.close()
        conn.close()        
        self.main.rerender()
        
    #add a new transaction
    def new_transaction(self,wallet,Type,amount,category,date):
        conn = sqlite3.connect("Main.db")
        c = conn.cursor()
        c.execute("insert into transactions values('{}','{}',{},'{}','{}')".format(wallet,Type,amount,category,date))
        conn.commit()
        c.close()
        conn.close()
        
    #return all wallets as list of tuples
    def get_all_wallets(self):
        conn = sqlite3.connect("Main.db")
        c = conn.cursor()
        c.execute("select * from wallets")
        return c.fetchall() 

    #get all transactions from a wallet
    def get_all_transactions(self, name):
        conn = sqlite3.connect("Main.db")
        c = conn.cursor()
        c.execute("select * from transactions where wallet_name='{}'".format(name))
        return c.fetchall() 

    #get the current balance in a wallet
    def get_bal(self, n):
        amt = self.get_wallet(n)[0][0]
        c,d = self.get_cnd(n)
        return amt+c - d

    #fill out the tree view
    def refresh_treev(self, treev, name):
        # print(name)
        treev.delete(*treev.get_children())
        data = self.get_all_transactions(name)
        for i in range(len(data)):
            if data[i][0] == name:
                treev.insert(parent='', index='end', iid=i,text='', values=(data[i][2],data[i][1],data[i][3],data[i][4]))

    def get_dncate(self, name):
        conn = sqlite3.connect("Main.db")
        c = conn.cursor()
        c.execute("select category, amount from transactions where wallet_name='{}' and type='D'".format(name))
        data = c.fetchall()
        c.close()
        conn.close()
        return data
    
    #get sum of all debits and credits from a wallet
    def get_cnd(self, name):
        conn = sqlite3.connect("Main.db")
        c = conn.cursor()
        c.execute("select total(amount) from transactions where wallet_name='{}' and type='C'".format(name))
        creds = c.fetchone()[0]
        c.execute("select total(amount) from transactions where wallet_name='{}' and type='D'".format(name))
        debts = c.fetchone()[0]
        c.close()
        conn.close()
        return (creds, debts)


    #get a single wallet record
    def get_wallet(self, name):
        conn = sqlite3.connect("Main.db")
        c = conn.cursor()
        c.execute("select * from wallets where name='{}'".format(name))
        return c.fetchall()
