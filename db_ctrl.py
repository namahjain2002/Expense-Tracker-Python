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
        c.execute("create table if not exists transactions(type VARCHAR(20), amount NUMERIC, category VARCHAR(20), desc TEXT)")
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
        conn.commit()
        c.close()
        conn.close()        
        self.main.rerender()
        
    #add a new transaction
    def new_transaction(self,Type,amount,category,desc):
        conn = sqlite3.connect("Main.db")
        c = conn.cursor()
        c.execute("insert into transactions values('{}',{},'{}','{}')".format(Type,amount,category,desc))
        conn.commit()
        c.close()
        conn.close()
        
    #return all wallets as list of tuples
    def get_all_wallets(self):
        conn = sqlite3.connect("Main.db")
        c = conn.cursor()
        c.execute("select * from wallets")
        return c.fetchall() 
