from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class Sale(Base):
    """ Sale """
    __tablename__ ="sales"

    id = Column(Integer, primary_key=True)
    title = Column(String(250),  nullable=False)
    store = Column(Integer, nullable=False)
    till_number = Column(Integer, nullable=False)
    transaction_number = Column(Integer, nullable=False)
    date = Column(String(10), nullable=False)
    sku = Column(Integer, nullable=False)
    name = Column(String(250), nullable=False)
    price = Column(String(10), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, title, store, till_number, transaction_number, date, sku, name, price):
        self.title = title
        self.store = store
        self.till_number = till_number
        self.transaction_number = transaction_number
        self.date = date
        self.sku = sku
        self.name = name
        self.price = price
        self.date_created = datetime.datetime.now() # Sets the date/time record is created

    def to_dict(self):
        """ Dictionary Representation of a sale transaction """
        dict = {}
        dict['id'] = self.id
        dict['title'] = self.title
        dict['gcid'] = {}
        dict['gcid']['store'] = self.store
        dict['gcid']['till_number'] = self.till_number
        dict['gcid']['transaction_number'] = self.transaction_number
        dict['gcid']['date'] = self.date
        dict['sale_product'] = {}
        dict['sale_product']['sku'] = self.sku
        dict['sale_product']['name'] = self.name
        dict['sale_product']['price'] = self.price
        dict['date_created'] = self.date_created

        return dict
