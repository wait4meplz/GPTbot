from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric, CheckConstraint, select,column
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base




class botBD:

    def trysql2(self):

        try:
            self.engine = create_engine('sqlite:///data.db')

            self.engine.connect()
            self.Session = sessionmaker(bind=self.engine)
            self.session = self.Session()

            print('ok')
        except:
            print("dber")



    def insertBD(self):
        self.mytable = Table('users', self.metadata, autoload=True)
        print(self.mytable)


botBD().trysql2()
